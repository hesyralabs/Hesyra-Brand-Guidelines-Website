"""
Ultra-fast High-Yield Multi-Engine Search Scraper:
Pulls 150-300+ real search suggestions across Google and Bing in ~3 seconds.
"""

import urllib.request
import urllib.parse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Set, Dict, Any
from .config import SEED_TOPICS

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

class KeywordScraper:
    def __init__(self, user_agent: str = USER_AGENT):
        self.user_agent = user_agent

    def fetch_google_suggest(self, query: str) -> List[str]:
        encoded = urllib.parse.quote(query)
        url = f"http://suggestqueries.google.com/complete/search?client=chrome&q={encoded}&hl=en&gl=in"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if len(data) > 1 and isinstance(data[1], list):
                    return [str(x).strip().lower() for x in data[1]]
        except Exception:
            pass
        return []

    def fetch_bing_suggest(self, query: str) -> List[str]:
        encoded = urllib.parse.quote(query)
        url = f"http://api.bing.com/osjson.aspx?query={encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if len(data) > 1 and isinstance(data[1], list):
                    return [str(x).strip().lower() for x in data[1]]
        except Exception:
            pass
        return []

    def scrape_all_candidates(self, target_count: int = 150) -> List[Dict[str, Any]]:
        # High yield probe generation: ~4 probes per seed across 36 seeds = 144 fast calls
        probes = []
        for cat_obj in SEED_TOPICS:
            cat = cat_obj["category"]
            for s in cat_obj["seeds"]:
                probes.append((cat, s))
                probes.append((cat, f"{s} cost"))
                probes.append((cat, f"{s} manufacturer"))
                probes.append((cat, f"{s} nagpur"))
                probes.append((cat, f"{s} lab"))

        all_candidates: List[Dict[str, Any]] = []
        seen: Set[str] = set()

        def query_probe(item):
            c, q = item
            results = []
            for kw in self.fetch_google_suggest(q):
                results.append((c, kw))
            for kw in self.fetch_bing_suggest(q):
                results.append((c, kw))
            return results

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(query_probe, p) for p in probes]
            for f in as_completed(futures):
                try:
                    for c, kw in f.result():
                        cleaned = re.sub(r"\s+", " ", kw).strip()
                        if len(cleaned) >= 4 and cleaned not in seen:
                            seen.add(cleaned)
                            all_candidates.append({
                                "raw_query": cleaned,
                                "seed_category": c
                            })
                            if len(all_candidates) >= target_count:
                                break
                except Exception:
                    pass

                if len(all_candidates) >= target_count:
                    break

        return all_candidates
