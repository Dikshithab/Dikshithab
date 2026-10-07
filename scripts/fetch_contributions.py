import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path

USERNAME = "Dikshithab"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""

token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise RuntimeError("GITHUB_TOKEN is not available.")

payload = json.dumps({
    "query": QUERY,
    "variables": {
        "login": USERNAME
    }
}).encode("utf-8")

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Dikshithab-GitHub-Profile"
    },
    method="POST"
)

with urllib.request.urlopen(request, timeout=30) as response:
    result = json.loads(response.read().decode("utf-8"))

if "errors" in result:
    raise RuntimeError(result["errors"])

calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]

days = []

for week in calendar["weeks"]:
    for day in week["contributionDays"]:
        level_map = {
            "NONE": 0,
            "FIRST_QUARTILE": 1,
            "SECOND_QUARTILE": 2,
            "THIRD_QUARTILE": 3,
            "FOURTH_QUARTILE": 4
        }

        days.append({
            "date": day["date"],
            "count": day["contributionCount"],
            "level": level_map.get(day["contributionLevel"], 0)
        })

Path("data").mkdir(exist_ok=True)

output = {
    "username": USERNAME,
    "total_contributions": calendar["totalContributions"],
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
print(f"Total contributions: {calendar['totalContributions']}")