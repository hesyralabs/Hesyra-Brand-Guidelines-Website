"""
End-to-end pipeline with full verbose inspection mode:
Scrape -> Evaluate Candidates (Laya / Jev) -> Accept/Reject Breakdown -> Rank -> Save.
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from .config import OUTPUT_JSON_PATH, OUTPUT_REPORT_PATH
from .scraper import KeywordScraper
from .decision_engine import DecisionEngineManager

def calculate_priority_score(decision: Dict[str, Any], query: str) -> int:
    """Computes a 1-10 SEO value score based on intent, category, and terms."""
    score = 5
    intent = decision.get("intent", "")
    if intent == "commercial_b2b":
        score += 3
    elif intent == "clinical_informational":
        score += 1
    elif intent == "spam_or_irrelevant":
        score -= 4

    q = query.lower()
    if "nagpur" in q:
        score += 2
    if any(k in q for k in ["lab", "manufacturer", "cost", "price", "turnaround"]):
        score += 1
    if "zirconia" in q or "aligner" in q:
        score += 1

    return max(1, min(10, score))

def run_pipeline(max_candidates: int = 40, engine_preference: str = "auto", verbose: bool = True) -> Dict[str, Any]:
    print("=" * 70)
    print("  Hesyra Labs - Real-Time Keyword Decision Trace")
    print("  Scraper: Live Google Suggest / Search Autocomplete")
    print(f"  Decision Engine: Laya (Local System-1) + Jev ({engine_preference})")
    print("=" * 70)

    print("")
    print("[STEP 1] LIVE SCRAPING FROM SEARCH ENGINES")
    print("-" * 70)
    scraper = KeywordScraper()
    raw_candidates = scraper.scrape_all_candidates(max_per_category=max(4, max_candidates // 4))
    print(f"-> Scraped {len(raw_candidates)} candidate queries from live search.\n")

    print("[STEP 2] LIVE DECISION EVALUATION (What works vs What gets rejected)")
    print("-" * 70)
    manager = DecisionEngineManager(preferred_engine=engine_preference)

    accepted_keywords: List[Dict[str, Any]] = []
    rejected_keywords: List[Dict[str, Any]] = []

    for idx, item in enumerate(raw_candidates, 1):
        q = item["raw_query"]
        decision = manager.evaluate(q)
        is_relevant = decision.get("is_relevant_to_hesyra", False)
        category = decision.get("category", "irrelevant")
        intent = decision.get("intent", "unclassified")

        if is_relevant:
            priority = calculate_priority_score(decision, q)
            accepted_keywords.append({
                "keyword": q,
                "category": category,
                "intent": intent,
                "priority_score": priority,
                "engine": decision.get("engine", "laya")
            })
            if verbose:
                print(f"[{idx:02d}] ACCEPTED -> \"{q}\"")
                print(f"     | Category: {category} | Intent: {intent} | Priority: {priority}/10")
                print(f"     | Why it works: Matches Hesyra B2B clinical domain & high search value\n")
        else:
            rejected_keywords.append({
                "keyword": q,
                "category": category,
                "intent": intent,
                "reason": "Not relevant to B2B lab operations or low commercial fit"
            })
            if verbose:
                print(f"[{idx:02d}] REJECTED -> \"{q}\"")
                print(f"     | Category: {category} | Intent: {intent}")
                print(f"     | Why rejected: Consumer/patient query, outside product catalog, or non-commercial\n")

    print("[STEP 3] SELECTION SUMMARY & CLUSTERING")
    print("-" * 70)
    accepted_keywords.sort(key=lambda x: x["priority_score"], reverse=True)
    print(f"Total Scraped:     {len(raw_candidates)}")
    print(f"Accepted (Works):  {len(accepted_keywords)}")
    print(f"Rejected (Noise):  {len(rejected_keywords)}")

    categorized: Dict[str, List[Dict[str, Any]]] = {}
    for kw in accepted_keywords:
        cat = kw["category"]
        categorized.setdefault(cat, []).append(kw)

    now = datetime.now()
    date_str = now.strftime("%B %Y")

    output_payload = {
        "generated_at": now.isoformat(),
        "month_label": date_str,
        "total_keywords": len(accepted_keywords),
        "total_evaluated": len(raw_candidates),
        "total_rejected": len(rejected_keywords),
        "top_keywords": accepted_keywords[:25],
        "by_category": categorized
    }

    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    generate_markdown_report(output_payload, rejected_keywords, OUTPUT_REPORT_PATH)
    print(f"\n[STEP 4] ARTIFACTS UPDATED")
    print(f"-> Website JSON: {OUTPUT_JSON_PATH}")
    print(f"-> Review Report: {OUTPUT_REPORT_PATH}\n")

    return output_payload

def generate_markdown_report(data: Dict[str, Any], rejected: List[Dict[str, Any]], filepath) -> None:
    lines = [
        f"# Hesyra Labs — Monthly Keyword Intelligence Report",
        f"**Month:** {data['month_label']}  ",
        f"**Generated:** {data['generated_at']}  ",
        f"**Candidate Pool Evaluated:** {data.get('total_evaluated', 0)}  ",
        f"**Accepted Keywords:** {data['total_keywords']}  ",
        f"**Rejected Candidates:** {data.get('total_rejected', 0)}",
        "",
        "## Top Qualified Keywords (What Works)",
        "| Rank | Keyword | Category | Intent | Score | Engine |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, kw in enumerate(data["top_keywords"][:15], 1):
        lines.append(f"| {idx} | **{kw['keyword']}** | `{kw['category']}` | `{kw['intent']}` | **{kw['priority_score']}/10** | `{kw['engine']}` |")

    lines.append("")
    lines.append("## Rejected Candidates (What Was Filtered Out)")
    lines.append("| Candidate | Category Assigned | Intent | Filter Reason |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for r in rejected[:15]:
        lines.append(f"| {r['keyword']} | `{r['category']}` | `{r['intent']}` | {r['reason']} |")

    lines.append("")
    lines.append("## Breakdown by Category")
    for cat, items in data["by_category"].items():
        lines.append(f"### {cat.replace('_', ' ').title()} ({len(items)} terms)")
        for item in items[:8]:
            lines.append(f"- **{item['keyword']}** (Score: {item['priority_score']}/10, Intent: {item['intent']})")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))