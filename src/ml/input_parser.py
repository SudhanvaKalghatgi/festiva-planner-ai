import re


CITIES = {
    "bangalore": 1,
    "mumbai": 1,
    "delhi": 1,
    "hyderabad": 1,
    "pune": 2,
    "mysore": 2,
    "nagpur": 2,
    "indore": 2,
    "belgaum": 3,
    "hubli": 3,
    "kolhapur": 3,
}


EVENT_TYPES = [
    "wedding",
    "corporate",
    "birthday",
    "engagement",
    "anniversary",
    "festival",
]


def extract_event_type(text):
    text = text.lower()
    for event in EVENT_TYPES:
        if event in text:
            return event
    return "wedding"


def extract_city(text):
    text = text.lower()
    for city in CITIES:
        if city in text:
            return city, CITIES[city]
    return "bangalore", 1


def extract_guest_count(text):
    match = re.search(r"\d+\s*(guests|people)", text.lower())
    if match:
        return int(match.group().split()[0])
    return 200


# 🔥 NEW FUNCTION
def extract_budget(text):
    text = text.lower()

    # Handle lakh
    match = re.search(r"(\d+)\s*(lakh|lac)", text)
    if match:
        value = int(match.group(1))
        return value * 100000

    # Handle thousand
    match = re.search(r"(\d+)\s*(k|thousand)", text)
    if match:
        value = int(match.group(1))
        return value * 1000

    # Default
    return 1000000


def extract_preferences(text):
    text = text.lower()

    return {
        "has_live_music": int("music" in text or "band" in text),
        "has_alcohol": int("alcohol" in text or "bar" in text),
        "is_outdoor": int("outdoor" in text),
        "is_destination": int("destination" in text),
    }


def parse_input(text):
    event_type = extract_event_type(text)
    city, city_tier = extract_city(text)
    guest_count = extract_guest_count(text)
    budget = extract_budget(text)  # 🔥 integrated here
    preferences = extract_preferences(text)

    return {
        "event_type": event_type,
        "city": city,
        "city_tier": city_tier,
        "guest_count": guest_count,
        "season": 1,
        "lead_time_days": 90,
        "budget": budget,  # 🔥 included
        **preferences,
    }