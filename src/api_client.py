"""
MyHealthfinder API Client
Base URL: https://odphp.health.gov/myhealthfinder/api/v4/
No API key required - U.S. HHS public API
"""

import requests
from typing import Optional

BASE_URL = "https://odphp.health.gov/myhealthfinder/api/v4"


def fetch_myhealthfinder(
    age: int = 25,
    sex: str = "female",
    pregnant: str = "no",
    sexually_active: str = "yes",
    tobacco_use: str = "no",
    lang: str = "en",
) -> Optional[dict]:
    """Fetch personalized preventive care recommendations."""
    url = f"{BASE_URL}/myhealthfinder.json"
    params = {
        "age": age,
        "sex": sex,
        "pregnant": pregnant,
        "sexuallyActive": sexually_active,
        "tobaccoUse": tobacco_use,
        "Lang": lang,
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None


def fetch_itemlist(item_type: str = "topic", lang: str = "en") -> Optional[dict]:
    """Fetch list of health topics or categories."""
    url = f"{BASE_URL}/itemlist.json"
    params = {"Type": item_type, "Lang": lang}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None


def fetch_topic(topic_id: str, lang: str = "en") -> Optional[dict]:
    """Fetch details for a specific topic."""
    url = f"{BASE_URL}/topicsearch.json"
    params = {"TopicId": topic_id, "Lang": lang}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None
