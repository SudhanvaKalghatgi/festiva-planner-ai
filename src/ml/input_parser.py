import re


# 🔥 Destination cities
DESTINATION_CITIES = {
    "goa", "udaipur", "jaipur", "manali", "rishikesh", "kerala"
}


# 🔥 City tier mapping
CITY_TIER_MAP = {
    "bangalore": 1,
    "bengaluru": 1,
    "mumbai": 1,
    "delhi": 1,

    "hyderabad": 2,
    "chennai": 2,
    "pune": 2,
    "mysore": 2,
    "goa": 2,
    "udaipur": 2,
    "jaipur": 2,

    "manali": 3,
    "rishikesh": 3
}


# 🔥 Normalize synonyms
CITY_ALIASES = {
    "bengaluru": "bangalore",
    "banglore": "bangalore",
    "delhii": "delhi"
}


def normalize_city(city: str) -> str:
    return CITY_ALIASES.get(city, city)


# 🔥 Extract city (FIXED matching)
def extract_city(text: str) -> str:
    text = text.lower()

    for city in CITY_TIER_MAP.keys():
        if re.search(rf"\b{city}\b", text):
            return normalize_city(city)

    return "bangalore"  # fallback


# 🔥 Detect destination
def detect_destination(city: str) -> int:
    return 1 if city in DESTINATION_CITIES else 0


# 🔥 Extract budget (IMPROVED)
def extract_budget(text: str) -> int:
    text = text.lower().replace(",", "")

    # ₹15 lakh / 15 lakh
    match = re.search(r"(₹?\s*\d+(?:\.\d+)?)\s*(lakh|lac)", text)
    if match:
        return int(float(re.findall(r"\d+(?:\.\d+)?", match.group(1))[0]) * 100000)

    # crore
    match = re.search(r"(\d+(?:\.\d+)?)\s*(crore)", text)
    if match:
        return int(float(match.group(1)) * 10000000)

    # 500k / thousand
    match = re.search(r"(\d+(?:\.\d+)?)\s*(k|thousand)", text)
    if match:
        return int(float(match.group(1)) * 1000)

    # raw number
    match = re.search(r"\b(\d{5,8})\b", text)
    if match:
        return int(match.group(1))

    return 1000000


# 🔥 Extract guests (IMPROVED)
def extract_guests(text: str) -> int:
    text = text.lower()

    match = re.search(r"(\d+)\s*(guests|people|persons)", text)
    if match:
        return int(match.group(1))

    # fallback pattern: "for 100"
    match = re.search(r"for\s+(\d+)", text)
    if match:
        return int(match.group(1))

    return 200


# 🔥 Extract lead time (IMPROVED)
def extract_lead_time(text: str) -> int:
    text = text.lower()

    # days
    match = re.search(r"(\d+)\s*(days|day)", text)
    if match:
        return int(match.group(1))

    # weeks
    match = re.search(r"(\d+)\s*(weeks|week)", text)
    if match:
        return int(match.group(1)) * 7

    # months
    match = re.search(r"(\d+)\s*(months|month)", text)
    if match:
        return int(match.group(1)) * 30

    if "next week" in text:
        return 7
    if "next month" in text:
        return 30

    return 90


# 🔥 Extract event type
def extract_event_type(text: str) -> str:
    text = text.lower()

    if "corporate" in text:
        return "corporate"
    return "wedding"


# 🔥 Feature flags
def extract_flags(text: str) -> dict:
    text = text.lower()

    return {
        "has_live_music": 1 if "music" in text or "dj" in text else 0,
        "has_alcohol": 1 if "alcohol" in text or "bar" in text else 0,
        "is_outdoor": 1 if "outdoor" in text or "open" in text else 0,
    }


# 🔥 MAIN PARSER
def parse_query(text: str) -> dict:
    city = extract_city(text)
    flags = extract_flags(text)

    parsed = {
        "event_type": extract_event_type(text),
        "city": city,
        "city_tier": CITY_TIER_MAP.get(city, 2),
        "guest_count": extract_guests(text),
        "season": 1,
        "lead_time_days": extract_lead_time(text),
        "budget": extract_budget(text),
        "is_destination": detect_destination(city),
        **flags
    }

    return parsed