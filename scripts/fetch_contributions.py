import json
import urllib.request
from datetime import datetime
from pathlib import Path

USERNAME = "Dikshithab"

URL = f"https://github.com/users/{USERNAME}/contributions"

request = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8")

days = []

# GitHub stores contribution data in SVG elements.
# Look for contribution cells using data-date and data-level.
import re

pattern = re.compile(
    r'<[^>]+data-date="([^"]+)"[^>]+data-level="([^"]+)"[^>]*>'
)

for match in pattern.finditer(html):
    date = match.group(1)
    level = int(match.group(2))

    days.append({
        "date": date,
        "count": 0,
        "level": level
    })

# Remove duplicates
unique = {}

for day in days:
    unique[day["date"]] = day

days = list(unique.values())
days.sort(key=lambda x: x["date"])

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

if not days:
    print("ERROR: GitHub contribution data was not found.")