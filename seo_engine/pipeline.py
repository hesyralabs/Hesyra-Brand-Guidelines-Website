"""
End-to-end pipeline: Scrape -> Filter & Score (Laya / Jev) -> Rank -> Save outputs.
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

    # Intent weighting
    intent = decision.get("intent", "")
    if intent == "commercial_b2b":
        score += 3
    elif intent == "clinical_informational":
        score += 1
    elif intent == "spam_or_irrelevant":
        score -= 4

    # High-value clinical keywords
    q = query.lower()
    if "nagpur" in q:
        score += 2
    if any(k in q for k in ["lab", "manufacturer", "cost", "price", "turnaround"]):
        score += 1
    if "zirconia" in q or "aligner" in q:
        score += 1

    return max(1, min(10, score))


def run_pipeline(max_candidates: int = 60, engine_preference: str = "auto") -> Dict[str, Any]:
    """Runs complete scraping and decision pipeline."""
    print("==================================================")
    print("  Hesyra Labs - Monthly SEO Keyword Engine")
    print("  Scraper: Google Suggest Live Query Expansion")
    print(f"  Decision Engine: Laya (Local System-1) + Jev ({engine_preference})")
    print("==================================================")

    # 1. Scraping
    print("[1/4] Scraping live search queries...")
    scraper = KeywordScraper()
    raw_candidates = scraper.scrape_all_candidates(max_per_category=max_candidates // 4)
    print(f"      Scraped {len(raw_candidates)} candidate queries.")

    # 2. Decision Engine Evaluation
    print(f"[2/4] Evaluating candidates through Decision Engine...")
    manager = DecisionEngineManager(preferred_engine=engine_preference)
    
    scored_keywords: List[Dict[str, Any]] = []

    for item in raw_candidates:
        q = item["raw_query"]
        decision = manager.evaluate(q)

        # Retain relevant keywords
        if decision.get("is_relevant_to_hesyra", False):
            priority = calculate_priority_score(decision, q)
            scored_keywords.append({
                "keyword": q,
                "category": decision.get("category", "general"),
                "intent": decision.get("intent", "commercial_b2b"),
                "priority_score": priority,
                "engine": decision.get("engine", "laya")
            })

    # 3. Sort and deduplicate
    print("[3/4] Ranking and clustering keywords...")
    scored_keywords.sort(key=lambda x: x["priority_score"], reverse=True)

    # Cluster by category
    categorized: Dict[str, List[Dict[str, Any]]] = {}
    for kw in scored_keywords:
        cat = kw["category"]
        categorized.setdefault(cat, []).append(kw)

    now = datetime.now()
    month_str = now.strftime("%Y-%m")
    date_str = now.strftime("%B %Y")

    output_payload = {
        "generated_at": now.isoformat(),
        "month_label": date_str,
        "total_keywords": len(scored_keywords),
        "top_keywords": scored_keywords[:25],
        "by_category": categorized
    }

    # 4. Save JSON for web usage
    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)
    print(f"[4/4] Saved website JSON bundle -> {OUTPUT_JSON_PATH}")

    # Save Markdown report
    generate_markdown_report(output_payload, OUTPUT_REPORT_PATH)
    print(f"      Saved review report -> {OUTPUT_REPORT_PATH}")

    return output_payload


def generate_markdown_report(data: Dict[str, Any], filepath) -> None:
    """Generates a structured human-readable Markdown summary."""
    lines = [
        f"# Hesyra Labs — Monthly Keyword Intelligence Report",
        f"**Month:** {data['month_label']}  ",
        f"**Generated:** {data['generated_at']}  ",
        f"**Total Qualified Keywords:** {data['total_keywords']}",
        "",
        "## Top 15 Priority Keywords for Website & SEO",
        "| Rank | Keyword | Category | Intent | Score | Engine |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, kw in enumerate(data["top_keywords"][:15], 1):
        lines.append(f"| {idx} | **{kw['keyword']}** | `{kw['category']}` | `{kw['intent']}` | **{kw['priority_score']}/10** | `{kw['engine']}` |")

    lines.append("")
    lines.append("## Breakdown by Category")
    for cat, items in data["by_category"].items():
        lines.append(f"### {cat.replace('_', ' ').title()} ({len(items)} terms)")
        for item in items[:8]:
            lines.append(f"- **{item['keyword']}** (Score: {item['priority_score']}/10, Intent: {item['intent']})")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))