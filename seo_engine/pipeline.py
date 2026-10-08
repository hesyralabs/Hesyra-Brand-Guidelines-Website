"""
End-to-end pipeline: Deep Scraper -> Decision Engine (Laya / Jev) -> Rank -> JSON, Report & Dashboard.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from .config import OUTPUT_JSON_PATH, OUTPUT_REPORT_PATH, OUTPUT_DASHBOARD_PATH
from .scraper import KeywordScraper
from .decision_engine import DecisionEngineManager

def calculate_priority_score(decision: Dict[str, Any], query: str) -> int:
    score = 5

    intent = decision.get("intent", "")
    if intent == "commercial_b2b":
        score += 3
    elif intent == "clinical_informational":
        score += 1
    elif intent == "spam_or_irrelevant":
        score -= 4

    q = query.lower()
    if "nagpur" in q or "maharashtra" in q:
        score += 2
    if any(k in q for k in ["lab", "manufacturer", "suppliers", "cost", "price", "turnaround", "b2b"]):
        score += 1
    if "zirconia" in q or "aligner" in q or "denture" in q:
        score += 1

    return max(1, min(10, score))


def run_pipeline(max_candidates: int = 150, engine_preference: str = "auto", verbose: bool = False) -> Dict[str, Any]:
    print("=" * 70)
    print("  Hesyra Labs - High-Volume Keyword Intelligence Pipeline")
    print(f"  Scraper: Multi-Engine Real-Time Search (Target: {max_candidates}+ Candidates)")
    print(f"  Decision Engine: Laya (Local System-1) + Jev ({engine_preference})")
    print("=" * 70)

    # 1. Scraping Step
    print(f"\n[STEP 1] MULTI-ENGINE SCRAPING (Google + Bing + DuckDuckGo)...")
    scraper = KeywordScraper()
    raw_candidates = scraper.scrape_all_candidates(target_count=max_candidates)
    print(f"-> Successfully scraped {len(raw_candidates)} candidate queries from live search.\n")

    # 2. Decision Engine Step
    print(f"[STEP 2] DECISION EVALUATION ON {len(raw_candidates)} QUERIES...")
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
            reason = "Direct fit for Hesyra B2B lab catalog & commercial intent"
            if "nagpur" in q:
                reason = "High-priority local geo-demand for dental lab in Nagpur"
            elif "manufacturer" in q or "lab" in q:
                reason = "Direct clinic-to-laboratory manufacturing partner search"

            accepted_keywords.append({
                "keyword": q,
                "category": category,
                "intent": intent,
                "status": "ACCEPTED",
                "priority_score": priority,
                "score": priority,
                "engine": decision.get("engine", "laya"),
                "reason": reason
            })
            if verbose:
                print(f"[{idx:03d}] [ACCEPTED] {q} -> Score: {priority}/10 ({category})")
        else:
            reason = "Consumer/patient query, non-commercial, or outside lab scope"
            if any(w in q for w in ["hospital", "clinic"]):
                reason = "Clinic/hospital facility search, not laboratory manufacturing"
            elif any(w in q for w in ["ppt", "course", "college"]):
                reason = "Academic / student lecture inquiry"
            elif any(w in q for w in ["diy", "home"]):
                reason = "Consumer DIY home product, zero clinical value"

            rejected_keywords.append({
                "keyword": q,
                "category": category,
                "intent": intent,
                "status": "REJECTED",
                "priority_score": 3,
                "score": 3,
                "engine": decision.get("engine", "laya"),
                "reason": reason
            })
            if verbose:
                print(f"[{idx:03d}] [REJECTED] {q} -> Reason: {reason}")

    # 3. Clustering
    accepted_keywords.sort(key=lambda x: x["priority_score"], reverse=True)
    pass_rate = round((len(accepted_keywords) / max(1, len(raw_candidates))) * 100, 1)

    print(f"\n[STEP 3] EVALUATION SUMMARY")
    print(f"Total Candidates Scraped: {len(raw_candidates)}")
    print(f"Accepted (High-Value):    {len(accepted_keywords)} ({pass_rate}% Pass Rate)")
    print(f"Rejected (Noise Filtered): {len(rejected_keywords)}")

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
        "top_keywords": accepted_keywords,
        "by_category": categorized
    }

    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    generate_markdown_report(output_payload, rejected_keywords, OUTPUT_REPORT_PATH)

    all_evaluated = accepted_keywords + rejected_keywords
    update_dashboard_json(all_evaluated, len(raw_candidates), len(accepted_keywords), len(rejected_keywords), OUTPUT_DASHBOARD_PATH)

    print(f"\n[STEP 4] ARTIFACTS UPDATED")
    print(f"-> Website JSON: {OUTPUT_JSON_PATH}")
    print(f"-> Review Report: {OUTPUT_REPORT_PATH}")
    print(f"-> Interactive Dashboard: {OUTPUT_DASHBOARD_PATH}\n")

    return output_payload


def generate_markdown_report(data: Dict[str, Any], rejected: List[Dict[str, Any]], filepath) -> None:
    lines = [
        f"# Hesyra Labs - Monthly Keyword Intelligence Report",
        f"**Month:** {data['month_label']}  ",
        f"**Generated:** {data['generated_at']}  ",
        f"**Candidate Pool Evaluated:** {data.get('total_evaluated', 0)}  ",
        f"**Accepted High-Value Keywords:** {data['total_keywords']}  ",
        f"**Rejected Filtered Out:** {data.get('total_rejected', 0)}",
        "",
        "## Top Qualified Keywords (Sample of Winners)",
        "| Rank | Keyword | Category | Intent | Score | Engine |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, kw in enumerate(data["top_keywords"][:25], 1):
        lines.append(f"| {idx} | **{kw['keyword']}** | `{kw['category']}` | `{kw['intent']}` | **{kw['priority_score']}/10** | `{kw['engine']}` |")

    lines.append("")
    lines.append("## Filtered Candidates Sample")
    lines.append("| Candidate | Category Assigned | Intent | Filter Reason |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for r in rejected[:20]:
        lines.append(f"| {r['keyword']} | `{r['category']}` | `{r['intent']}` | {r['reason']} |")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def update_dashboard_json(candidates: List[Dict[str, Any]], total: int, accepted: int, rejected: int, filepath: Path) -> None:
    if not filepath.exists():
        return
    html = filepath.read_text(encoding="utf-8")
    
    # Update DATA constant in JS
    start_token = "const DATA = "
    end_token = "];"
    s_idx = html.find(start_token)
    if s_idx != -1:
        e_idx = html.find(end_token, s_idx)
        if e_idx != -1:
            json_str = json.dumps(candidates)
            html = html[:s_idx + len(start_token)] + json_str + html[e_idx + 1:]
    
    # Update metric counters
    import re
    html = re.sub(r'id="metricTotal">\d+', f'id="metricTotal">{total}', html)
    html = re.sub(r'id="metricAccepted">\d+', f'id="metricAccepted">{accepted}', html)
    html = re.sub(r'id="metricRejected">\d+', f'id="metricRejected">{rejected}', html)
    
    filepath.write_text(html, encoding="utf-8")
