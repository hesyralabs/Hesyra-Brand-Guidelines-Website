"""
Laya and Jev Decision Engine for fast non-autoregressive keyword evaluation.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional
from .config import BRAND_CONTEXT, KEYWORD_SCHEMA

class LayaEngine:
    """Local or in-process Laya decision model runner (~33ms per inference)."""

    def __init__(self, model_id: str = "convaiinnovations/laya", device: str = "cpu"):
        self.model_id = model_id
        self.device = device
        self.agent = None
        self._load_agent()

    def _load_agent(self):
        try:
            import laya
            print(f"[Laya] Loading model {self.model_id} on {self.device}...")
            self.agent = laya.load(self.model_id, device=self.device)
            print("[Laya] Decision agent ready.")
        except Exception as e:
            print(f"[Laya] Notice: Could not load local laya agent directly ({e}). Falling back to rule scoring.")
            self.agent = None

    def decide(self, keyword: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates keyword against typed schema using Laya."""
        if self.agent is not None:
            import laya
            state = {
                "keyword": keyword,
                "business": context.get("brand_name"),
                "location": context.get("location"),
                "products": ", ".join(context.get("primary_products", []))
            }
            try:
                res = laya.decide(self.agent, state=state, schema=KEYWORD_SCHEMA)
                if isinstance(res, dict):
                    return res
            except Exception as e:
                pass
        
        # Heuristic fallback if local model throws or isn't loaded
        return self._heuristic_fallback(keyword)

    def _heuristic_fallback(self, keyword: str) -> Dict[str, Any]:
        kw = keyword.lower()
        is_relevant = any(w in kw for w in ["zirconia", "aligner", "crown", "denture", "lab", "dental", "nagpur", "bridge", "cad cam"])
        
        category = "irrelevant"
        if "zirconia" in kw or "crown" in kw or "bridge" in kw:
            category = "zirconia_crowns"
        elif "aligner" in kw:
            category = "clear_aligners"
        elif "denture" in kw:
            category = "dentures_cadcam"
        elif "nagpur" in kw or "lab" in kw:
            category = "local_b2b_lab"

        intent = "commercial_b2b"
        if any(w in kw for w in ["what is", "how to", "symptoms", "causes"]):
            intent = "clinical_informational"
        elif any(w in kw for w in ["cheap", "diy", "home", "shopee"]):
            intent = "spam_or_irrelevant"

        return {
            "category": category,
            "intent": intent,
            "is_relevant_to_hesyra": is_relevant and (category != "irrelevant")
        }


class JevEngine:
    """TypeSafe AI Jev Managed Decision API client."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("JEV_API_KEY")
        self.endpoint = "https://api.typesafe.ai/v1/decide"

    @property
    def is_available(self) -> bool:
        return bool(self.api_key)

    def decide(self, keyword: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Calls Jev Decision API with structured schema."""
        if not self.is_available:
            return None

        payload = {
            "state": {
                "keyword": keyword,
                "business": context.get("brand_name"),
                "location": context.get("location")
            },
            "schema": KEYWORD_SCHEMA
        }

        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Hesyra-SEO-Pipeline"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("decision")
        except Exception:
            return None


class DecisionEngineManager:
    """Orchestrates Laya and Jev with automatic failover."""

    def __init__(self, preferred_engine: str = "auto"):
        self.preferred = preferred_engine
        self.jev = JevEngine()
        self.laya = LayaEngine()

    def evaluate(self, keyword: str) -> Dict[str, Any]:
        # 1. Try Jev if preferred or available
        if (self.preferred == "jev" or self.preferred == "auto") and self.jev.is_available:
            result = self.jev.decide(keyword, BRAND_CONTEXT)
            if result:
                result["engine"] = "jev"
                return result

        # 2. Use local Laya model
        result = self.laya.decide(keyword, BRAND_CONTEXT)
        result["engine"] = "laya"
        return result
