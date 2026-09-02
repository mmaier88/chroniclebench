#!/usr/bin/env python3
"""Regenerate assets/board.svg from data/ — the README results chart.

One scale, mirroring bench.chronicle.town: blue = Chronicle-powered entrants
(one row per model; system entries labeled), gold = the published-novel average,
sand = human reference anchors. Run: python tools/make_chart.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "benchmark-v1.1.json").read_text())
opus = json.loads((ROOT / "data" / "chronicle-x-opus.json").read_text())
sonnet = json.loads((ROOT / "data" / "chronicle-x-sonnet.json").read_text())

hum = [b["sagascore"] for b in data["boards"]["human"]["books"] if b.get("sagascore")]
human_mean = sum(hum) / len(hum)
SUPERSEDED = {"sonnet46", "opus5"}  # shown via their system entries

rows = [
    ("Chronicle × Opus 5", opus["sagascore"], "sys"),
    ("Chronicle × Sonnet (Production)", sonnet["sagascore"], "sys"),
]
for r in data["boards"]["sustained"]:
    if r.get("sagascore") and r["model"] not in SUPERSEDED:
        rows.append((f"Chronicle × {r['display']}", r["sagascore"], "ai"))
rows.append(("Average published novel (36-book corpus)", round(human_mean, 1), "human"))
rows.append(("Best reference novel", max(hum), "anchor"))
rows.append(("Weakest reference novel", min(hum), "anchor"))
rows.sort(key=lambda x: -x[1])

LO, HI, W, RH = 30, 96, 860, 34
H = len(rows) * RH + 70
bar_x, bar_w = 330, W - 330 - 70


def x(v: float) -> float:
    return bar_x + bar_w * (v - LO) / (HI - LO)


FILL = {"sys": "#2b5bd7", "ai": "#5a8bf1", "human": "#c9a227", "anchor": "#d8cdb8"}
TXT = {"sys": "#1d44b8", "ai": "#3a63c4", "human": "#8a6d1f", "anchor": "#8b8574"}

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
    f'<rect width="{W}" height="{H}" fill="#faf6ec" rx="12"/>',
    f'<text x="24" y="34" font-size="17" font-weight="700" fill="#10142a">ChronicleBench Score — every entrant and the published-fiction reference, one pinned instrument</text>',
]
y = 58
for name, score, cls in rows:
    svg.append(f'<text x="{bar_x - 10}" y="{y + 16}" font-size="12.5" text-anchor="end" fill="{TXT[cls]}" font-weight="{700 if cls == "sys" else 400}">{name}</text>')
    svg.append(f'<rect x="{bar_x}" y="{y + 4}" width="{x(score) - bar_x:.1f}" height="15" rx="3" fill="{FILL[cls]}"/>')
    svg.append(f'<text x="{x(score) + 8:.1f}" y="{y + 16}" font-size="12.5" font-weight="600" fill="#10142a">{score}</text>')
    y += RH
svg.append("</svg>")
out = ROOT / "assets" / "board.svg"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(svg))
print(f"wrote {out} ({len(rows)} rows)")
