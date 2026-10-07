import json
from pathlib import Path
from html import escape

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("profile/contribution-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

CELL = 12
GAP = 3
STEP = CELL + GAP

WIDTH = 860
HEIGHT = 150

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

days = data["days"]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
.cell {{
    opacity: 0;
    animation: reveal 0.5s ease-out forwards;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translateY(-8px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.title {{
    fill: #c9d1d9;
    font-family: monospace;
    font-size: 15px;
}}

.legend {{
    fill: #8b949e;
    font-family: monospace;
    font-size: 11px;
}}
</style>

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="20" y="25" class="title">
GitHub Contributions — {escape(data["username"])}
</text>
'''

# Keep the most recent contribution days
days = days[-371:]

for index, day in enumerate(days):

    week = index // 7
    weekday = index % 7

    x = 20 + week * STEP
    y = 40 + weekday * STEP

    level = max(0, min(day["level"], 4))
    color = PALETTE[level]

    delay = (week * 7 + weekday) * 0.008

    svg += f'''
    <rect
        class="cell"
        x="{x}"
        y="{y}"
        width="{CELL}"
        height="{CELL}"
        rx="3"
        fill="{color}"
        style="animation-delay:{delay:.3f}s">
        <title>{escape(day["date"])} — {day["count"]} contributions</title>
    </rect>
    '''

svg += '''
<text x="20" y="142" class="legend">Less</text>
'''

for i in range(5):
    x = 55 + i * 16

    svg += f'''
    <rect
        x="{x}"
        y="133"
        width="12"
        height="12"
        rx="3"
        fill="{PALETTE[i]}"/>
    '''

svg += '''
<text x="145" y="142" class="legend">More</text>

</svg>
'''

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Created {OUTPUT_FILE}")