"""
Multi-source keyword scraper pulling real-time search queries and search suggestions.
"""

import urllib.request
import urllib.parse
import json
import string
import re
from typing import List, Set, Dict, Any
from .config import SEED_TOPICS

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

class KeywordScraper:
    """Scrapes Google autocomplete & search suggest queries without API keys."""

    def __init__(self, user_agent: str = USER_AGENT):
        self.user_agent = user_agent

    def fetch_google_suggest(self, query: str) -> List[str]:
        """Fetch live queries from Google Suggest API."""
        encoded_query = urllib.parse.quote(query)
        url = f"http://suggestqueries.google.com/complete/search?client=chrome&q={encoded_query}&hl=en&gl=in"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if len(payload) > 1 and isinstance(payload[1], list):
                    return [str(item).strip().lower() for item in payload[1]]
        except Exception as e:
            # Silently handle transient network issues
            pass
        return []

    def expand_query(self, seed: str, include_alphabetic: bool = True) -> Set[str]:
        """Expands a seed query with alphabet modifiers and intent prefixes."""
        queries: Set[str] = set()

        # Direct suggest
        queries.update(self.fetch_google_suggest(seed))

        # Intent modifiers
        modifiers = ["best", "cost", "price", "manufacturer", "lab", "nagpur", "b2b"]
        for mod in modifiers:
            queries.update(self.fetch_google_suggest(f"{seed} {mod}"))
            queries.update(self.fetch_google_suggest(f"{mod} {seed}"))

        # Alphabet soup expansion (a-z)
        if include_alphabetic:
            for char in string.ascii_lowercase[:10]:  # Top 10 letters for speed
                queries.update(self.fetch_google_suggest(f"{seed} {char}"))

        return queries

    def scrape_all_candidates(self, max_per_category: int = 40) -> List[Dict[str, Any]]:
        """Scrapes across all seed categories and returns cleaned candidates."""
        candidates: List[Dict[str, Any]] = []
        seen_terms: Set[str] = set()

        for group in SEED_TOPICS:
            cat_name = group["category"]
            cat_candidates: Set[str] = set()

            for seed in group["seeds"]:
                expanded = self.expand_query(seed, include_alphabetic=True)
                for term in expanded:
                    # Clean punctuation and short tokens
                    cleaned = re.sub(r"\s+", " ", term).strip()
                    if len(cleaned) > 3 and cleaned not in seen_terms:
                        seen_terms.add(cleaned)
                        cat_candidates.add(cleaned)
                        if len(cat_candidates) >= max_per_category:
                            break
                if len(cat_candidates) >= max_per_category:
                    break

            for term in cat_candidates:
                candidates.append({
                    "raw_query": term,
                    "seed_category": cat_name
                })

        return candidates
