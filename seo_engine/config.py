"""
Configuration & Expanded Dental Seeds for Deep Web Scraping.
"""

from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent

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

SEED_TOPICS: List[Dict[str, Any]] = [
    {
        "category": "zirconia_crowns",
        "seeds": [
            "zirconia crown",
            "zirconia bridge",
            "monolithic zirconia",
            "multilayer zirconia crown",
            "zirconia crown lab",
            "zirconia tooth cap",
            "bruxzir zirconia crown",
            "zirconia milling center",
            "dental crown lab price india",
            "anterior zirconia crown"
        ]
    },
    {
        "category": "clear_aligners",
        "seeds": [
            "clear aligners b2b",
            "invisible aligners lab",
            "clear aligner manufacturer india",
            "orthodontic aligner fabrication",
            "white label clear aligners",
            "aligners for dentists b2b",
            "custom clear aligner lab",
            "clear aligner sheets manufacturing",
            "invisalign alternative lab india"
        ]
    },
    {
        "category": "dentures_cadcam",
        "seeds": [
            "cad cam dentures",
            "flexible denture lab",
            "3d printed dentures lab",
            "cast partial denture manufacturer",
            "digital complete denture",
            "lucitone digital print dentures",
            "removable partial denture lab",
            "implant supported overdenture lab"
        ]
    },
    {
        "category": "local_b2b_lab",
        "seeds": [
            "dental lab nagpur",
            "digital dental laboratory nagpur",
            "best dental lab in vidarbha",
            "dental laboratory maharashtra",
            "cad cam milling nagpur",
            "dental prosthetics nagpur",
            "dental lab 48 hour delivery",
            "dental lab near me b2b",
            "dental clinic lab supplier"
        ]
    }
]

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
OUTPUT_DASHBOARD_PATH = BASE_DIR / "deploy" / "seo-dashboard.html"
