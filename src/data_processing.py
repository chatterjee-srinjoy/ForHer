"""
Data Processing Layer - Rule-based filtering before LLM.
Categorizes, prioritizes, and filters recommendations.
"""

import re
from typing import Any

import pandas as pd

# Vaccine keywords for categorization
VACCINE_KEYWORDS = ["vaccine", "vaccination", "hpv", "tdap", "flu", "mmr", "immunization", "shot"]
SCREENING_KEYWORDS = ["screen", "test", "check", "pap", "mammogram", "blood pressure", "cholesterol"]
VISIT_KEYWORDS = ["visit", "checkup", "well-woman", "wellness", "annual"]
LIFESTYLE_KEYWORDS = ["mental health", "stress", "exercise", "diet", "smoking", "alcohol"]


def _extract_first_section_text(sections: Any) -> str:
    """Extract plain text from first section content (strip HTML)."""
    if not sections or not isinstance(sections, dict):
        return ""
    sec_list = sections.get("section")
    if not sec_list:
        return ""
    if isinstance(sec_list, dict):
        sec_list = [sec_list]
    first = sec_list[0] if sec_list else {}
    content = first.get("Content", "")
    if not content:
        return ""
    # Strip HTML tags
    return re.sub(r"<[^>]+>", " ", content).strip()[:500]


def process_recommendations(
    raw_recs: list[dict],
    completed_vaccines: list[str],
    unsure_items: list[str],
) -> pd.DataFrame:
    """
    Process raw API recommendations into clean structured data.
    - Remove completed vaccines
    - Flag unsure items
    - Categorize and assign priority
    """
    rows = []
    for r in raw_recs:
        title = r.get("Title") or r.get("MyHFTitle", "")
        categories_raw = r.get("Categories") or r.get("MyHFCategory", "")
        desc = _extract_first_section_text(r.get("Sections", {}))

        # Skip if this is a completed vaccine
        title_lower = title.lower()
        completed_lower = [v.lower() for v in completed_vaccines]
        vaccine_match = next(
            (v for v in ["hpv", "tdap", "flu", "mmr"] if v in title_lower),
            None,
        )
        if vaccine_match and vaccine_match in completed_lower:
            continue

        # Assign category
        cat_lower = (str(categories_raw) + " " + title_lower).lower()
        if any(k in cat_lower for k in VACCINE_KEYWORDS):
            category = "Vaccinations"
        elif any(k in cat_lower for k in SCREENING_KEYWORDS):
            category = "Screenings"
        elif any(k in cat_lower for k in VISIT_KEYWORDS):
            category = "Preventive Visits"
        elif any(k in cat_lower for k in LIFESTYLE_KEYWORDS):
            category = "Lifestyle & Mental Health"
        else:
            category = r.get("MyHFCategory") or "Screenings"

        # Assign priority
        if "vaccine" in cat_lower or "cervical" in title_lower or "hpv" in title_lower:
            priority = "High"
        elif "visit" in cat_lower or "checkup" in cat_lower:
            priority = "Routine"
        else:
            priority = "Informational"

        # Flag unsure
        is_unsure = any(u.lower() in title_lower for u in unsure_items) or "unsure" in [x.lower() for x in unsure_items]

        rows.append({
            "title": title,
            "description": desc,
            "category": category,
            "priority": priority,
            "is_unsure": is_unsure,
            "status": "verify" if is_unsure else "recommended",
        })

    return pd.DataFrame(rows)


def get_clean_for_llm(df: pd.DataFrame, max_items: int = 5) -> str:
    """Return minimal clean text for LLM - only necessary fields."""
    if df is None or df.empty:
        return ""
    parts = []
    for _, row in df.head(max_items).iterrows():
        parts.append(f"- {row['title']} ({row['category']}): {row['description'][:200]}")
    return "\n".join(parts)
