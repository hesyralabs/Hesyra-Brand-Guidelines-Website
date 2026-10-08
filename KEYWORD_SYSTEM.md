# Hesyra Labs — SEO Keyword Intelligence Engine
### Powered by Laya (System-1 On-Device) & Jev (TypeSafe Decision API)

---

## 1. System Overview

This system scrapes real-time search queries and uses **non-autoregressive decision models (Laya & Jev)** to filter, classify, and rank the highest-value keywords for **Hesyra Labs** (Nagpur B2B Digital Dental Laboratory).

```
   [Google Search Suggest / SERP]
                 │
                 ▼
     [seo_engine/scraper.py]
    (Query Expansion & Cleaning)
                 │
                 ▼
  [seo_engine/decision_engine.py]
  ├── Laya Engine (Local ~33ms System-1)
  └── Jev Engine  (TypeSafe Cloud API)
                 │
                 ▼
     [seo_engine/pipeline.py]
  (Category Clustering & 1-10 Scoring)
                 │
        ┌────────┴────────┐
        ▼                 ▼
[deploy/keywords.json]   [deploy/keywords_report.md]
  (Website Ingestion)      (Human Audit Report)
```

---

## 2. Why Laya & Jev instead of Traditional LLMs?

Traditional LLMs (GPT-4, Claude) generate tokens one by one:
- **Slow:** 1.5s - 4.0s per keyword.
- **Expensive:** Scraping 500 keywords costs significant token credits.
- **Unreliable Parsing:** Requires regex or JSON markdown extraction.

**Laya & Jev** are non-autoregressive "System-1" decision models:
- **Ultra-fast:** Single forward pass (~33ms inference on CPU).
- **Direct Typed Output:** Returns strict typed JSON (booleans, enums, confidence values).
- **Zero Hallucination:** Computes calibrated probabilities across schemas rather than hallucinating text.
- **Local & Offline:** Laya runs completely locally without external network dependencies.

---

## 3. Directory Structure

```
Hesyra Brand Guidelines Website/
├── seo_engine/
│   ├── __init__.py
│   ├── config.py           # Brand context, seed queries, strict JSON schema
│   ├── scraper.py          # Real-time search query scraper & alphabet expansion
│   ├── decision_engine.py  # Dual Laya (Local) & Jev (API) orchestrator
│   └── pipeline.py         # End-to-end scraper -> scorer -> JSON/Markdown exporter
├── run_seo.py              # CLI entry point
├── KEYWORD_SYSTEM.md       # Technical documentation
└── deploy/
    ├── keywords.json       # Ingested by website frontend
    └── keywords_report.md  # Detailed monthly keyword report
```

---

## 4. Decision Engine Schema

Every candidate keyword is evaluated against this schema:

```json
{
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
```

### Priority Scoring Formula (1 - 10)
- **Base Score:** 5
- **Intent Boost:** `+3` for `commercial_b2b`, `+1` for `clinical_informational`, `-4` for `spam_or_irrelevant`
- **Location Boost:** `+2` if keyword includes `nagpur` or `maharashtra`
- **Commercial Modifiers:** `+1` for terms like `lab`, `manufacturer`, `cost`, `turnaround`
- **Primary Product Match:** `+1` for `zirconia`, `aligner`, `denture`

---

## 5. How to Run the Pipeline

### Quick Run (Default Settings):
```bash
python run_seo.py
```

### Custom Sample Size:
```bash
python run_seo.py --samples 80
```

### Engine Selection:
```bash
# Force local Laya model:
python run_seo.py --engine laya

# Force TypeSafe Jev API (requires JEV_API_KEY environment variable):
set JEV_API_KEY=your_key_here
python run_seo.py --engine jev

# Auto mode (prefers Jev if API key present, otherwise falls back to Laya):
python run_seo.py --engine auto
```

---

## 6. Website Integration

The website reads `deploy/keywords.json` dynamically to keep meta tags and SEO attributes fresh without needing code changes:

### In `deploy/index.html` or `deploy/support.js`:
```javascript
// Automatically update SEO meta tags from monthly keywords.json
fetch('./keywords.json')
  .then(response => response.json())
  .then(data => {
    if (data.top_keywords && data.top_keywords.length > 0) {
      // 1. Update meta keywords
      let metaKw = document.querySelector('meta[name="keywords"]');
      if (!metaKw) {
        metaKw = document.createElement('meta');
        metaKw.name = 'keywords';
        document.head.appendChild(metaKw);
      }
      metaKw.content = data.top_keywords.map(k => k.keyword).join(', ');

      console.log(`[SEO] Updated ${data.top_keywords.length} monthly keywords (${data.month_label})`);
    }
  })
  .catch(err => console.warn('[SEO] Could not load keywords.json', err));
```

---

## 7. Next Step: Automation Setup (When Ready)

When you want to automate this monthly:
1. **GitHub Actions Workflow (`.github/workflows/monthly-seo.yml`)**:
   - Cron trigger: `0 0 1 * *` (1st of every month at midnight UTC).
   - Runs `python run_seo.py --samples 100`.
   - Auto-commits updated `deploy/keywords.json` and pushes to `main`.
2. **Render Static Site**:
   - Automatically detects the git push and rebuilds the site with new keywords.
