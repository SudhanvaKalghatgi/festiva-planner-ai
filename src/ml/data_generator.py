import random
import pandas as pd
import numpy as np

CITIES = [
    ("Bangalore", 1),
    ("Mumbai", 1),
    ("Delhi", 1),
    ("Hyderabad", 1),
    ("Pune", 2),
    ("Mysore", 2),
    ("Nagpur", 2),
    ("Indore", 2),
    ("Belgaum", 3),
    ("Hubli", 3),
    ("Kolhapur", 3)
]

EVENT_TYPES = [
    "wedding",
    "corporate",
    "birthday",
    "engagement",
    "anniversary",
    "festival"
]

def random_preferences():
    return {
        "has_live_music": random.choice([0, 1]),
        "has_alcohol": random.choice([0, 1]),
        "is_outdoor": random.choice([0, 1]),
        "is_destination": random.choice([0, 1]),
    }

def generate_budget(event_type, city_tier, guests):
    base = {
        "wedding": 3000,
        "corporate": 1500,
        "birthday": 800,
        "engagement": 2000,
        "anniversary": 1000,
        "festival": 1200
    }

    per_person = base[event_type]
    multiplier = 1 + (0.3 if city_tier == 1 else 0.1 if city_tier == 2 else 0)

    return int(per_person * guests * multiplier + random.randint(-50000, 50000))


def generate_split():
    categories = [
        "venue", "catering", "decor", "photography",
        "music", "invites", "transport", "contingency"
    ]

    splits = np.random.dirichlet(np.ones(len(categories)), size=1)[0]
    return dict(zip(categories, splits))


def generate_dataset(n=2000):
    data = []

    for _ in range(n):
        city, tier = random.choice(CITIES)
        event_type = random.choice(EVENT_TYPES)
        guests = random.randint(50, 500)
        season = random.choice([0, 1])
        lead_time = random.randint(7, 180)

        prefs = random_preferences()
        budget = generate_budget(event_type, tier, guests)
        split = generate_split()

        row = {
            "city": city,
            "city_tier": tier,
            "event_type": event_type,
            "guest_count": guests,
            "season": season,
            "lead_time_days": lead_time,
            "budget": budget,
            **prefs
        }

        for k, v in split.items():
            row[f"{k}_pct"] = v

        data.append(row)

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    df = generate_dataset(2000)
    df.to_csv("data/raw/events.csv", index=False)
    print("Dataset generated at data/raw/events.csv")