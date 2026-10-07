import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

USERNAME = "Dikshithab"

URL = f"https://github.com/users/{USERNAME}/contributions"

request = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8")

days = []

pattern = re.compile(
    r'<td[^>]*class="[^"]*ContributionCalendar-day[^"]*"'
    r'[^>]*data-date="([^"]+)"'
    r'[^>]*data-level="([^"]+)"'
    r'[^>]*aria-label="([^"]*)"'
)

for match in pattern.finditer(html):
    date = match.group(1)
    level = int(match.group(2) or 0)
    label = match.group(3)

    count_match = re.search(r"(\d+)\s+contributions?", label)

    count = int(count_match.group(1)) if count_match else 0

    days.append({
        "date": date,
        "count": count,
        "level": level
    })

days.sort(key=lambda item: item["date"])

Path("data").mkdir(exist_ok=True)

output = {
    "username": USERNAME,
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "days": days
}

with open(
    "data/contributions.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(output, file, indent=2)

print(f"Fetched {len(days)} contribution days.")