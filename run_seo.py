"""
CLI Runner for Hesyra Monthly SEO Keyword Pipeline.
Usage:
    python run_seo.py
    python run_seo.py --samples 80 --engine laya
"""

import argparse
from seo_engine.pipeline import run_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hesyra SEO Scraper & Laya/Jev Decision Pipeline")
    parser.add_argument("--samples", type=int, default=50, help="Max candidate pool size")
    parser.add_argument("--engine", choices=["auto", "laya", "jev"], default="auto", help="Decision engine to prioritize")
    args = parser.parse_args()

    result = run_pipeline(max_candidates=args.samples, engine_preference=args.engine)
    print("\nPipeline completed successfully! Top 5 keywords:")
    for kw in result["top_keywords"][:5]:
        print(f"  [{kw['priority_score']}/10] {kw['keyword']} ({kw['category']})")
