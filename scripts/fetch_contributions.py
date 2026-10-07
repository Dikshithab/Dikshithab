import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Dikshithab"
URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20,
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")

    if not date:
        continue

    label = cell.get("aria-label", "")
    match = re.search(r"(\d+) contributions?", label)

    count = int(match.group(1)) if match else 0

    days.append({
        "date": date,
        "count": count,
        "level": int(level or 0),
    })

days.sort(key=lambda x: x["date"])

Path("data").mkdir(exist_ok=True)

output = {
    "username": USERNAME,
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "days": days,
}

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Fetched {len(days)} contribution days.")