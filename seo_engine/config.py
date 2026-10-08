from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
"""
Configuration & Schema definitions for Hesyra SEO Keyword Engine.
"""

from typing import Dict, Any, List

# Target brand profile context used for Laya / Jev decision scoring
BRAND_CONTEXT: Dict[str, Any] = {
    "brand_name": "Hesyra Labs",
    "location": "Nagpur, Maharashtra, India",
    "business_model": "B2B Digital Dental Laboratory (servicing dentists, orthodontists, clinics)",
    "primary_products": [
        "Monolithic & Multilayer Zirconia Crowns and Bridges",
        "Clear Aligners (direct lab manufacturing)",
        "Precision CAD/CAM Dentures (flexible, cast partial, 3D printed)",
        "Dental Implants & Hybrid Prosthetics"
    ],
    "value_propositions": [
        "48-hour rapid turnaround",
        "Sub-10 micron digital margin accuracy",
        "Direct-from-lab B2B pricing",
        "Digital scan file integration (STL, PLY, OBJ)"
    ]
}

# Seed query buckets for scraping
SEED_TOPICS: List[Dict[str, Any]] = [
    {
        "category": "zirconia_crowns",
        "seeds": [
            "zirconia crown",
            "zirconia bridge",
            "monolithic zirconia cost",
            "multilayer zirconia crown india",
            "dental lab zirconia price"
        ]
    },
    {
        "category": "clear_aligners",
        "seeds": [
            "clear aligners b2b",
            "invisible aligners lab manufacturer",
            "dental aligner lab india",
            "orthodontic aligner manufacturing"
        ]
    },
    {
        "category": "dentures_cadcam",
        "seeds": [
            "cad cam dentures",
            "flexible denture lab",
            "3d printed dentures lab india",
            "dental prosthesis manufacturer"
        ]
    },
    {
        "category": "local_b2b_lab",
        "seeds": [
            "dental lab nagpur",
            "digital dental laboratory maharashtra",
            "best dental lab for doctors india",
            "dental lab 48 hour turnaround"
        ]
    }
]

# Strict schema for Laya & Jev decision evaluation
KEYWORD_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["zirconia_crowns", "clear_aligners", "dentures_cadcam", "local_b2b_lab", "irrelevant"]
        },
        "intent": {
            "type": "string",
            "enum": ["commercial_b2b", "clinical_informational", "patient_consumer", "spam_or_irrelevant"]
        },
        "is_relevant_to_hesyra": {
            "type": "boolean"
        }
    },
    "required": ["category", "intent", "is_relevant_to_hesyra"]
}

OUTPUT_JSON_PATH = BASE_DIR / "deploy" / "keywords.json"
OUTPUT_REPORT_PATH = BASE_DIR / "deploy" / "keywords_report.md"
