#!/usr/bin/env python3
"""Render the Garmin telemetry card for the GitHub profile README.

Input:  data.json  (written by the weekly scheduled task from the Garmin MCP)
Output: garmin-card.svg

This script never talks to Garmin and never touches auth tokens. The MCP server
is the only process that holds the Garmin session; refreshing tokens from a
second process rotates the refresh token and breaks the MCP (see memory note
garmin-mcp-pin-mcp-below-2). Data comes in as plain JSON instead.

data.json schema:
{
  "as_of": "YYYY-MM-DD",
  "vo2max": 54.0,                      # or null
  "acute_load": 610,                   # Garmin ATL, latest day; or null
  "activities": [                      # every activity in the last ~12 weeks
    {"start": "YYYY-MM-DD HH:MM:SS", "type": "road_biking",
     "km": 13.4, "dur_s": 3466},
    ...
  ]
}

Only aggregates are rendered. Activity names and locations are deliberately
not part of the schema, so they cannot leak onto the public card.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
WEEKS = 12

RIDE_TYPES = {
    "cycling", "road_biking", "gravel_cycling", "mountain_biking",
    "indoor_cycling", "virtual_ride",
}

# victorchun-site dark theme
INK, SURFACE, BORDER = "#150F0B", "#1E1813", "#372F28"
PAPER, MUTED, AMBER = "#EAE6DD", "#999186", "#EFAC44"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"


def parse(ts: str) -> dt.datetime:
    return dt.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")


def dedupe_rides(rides: list[dict]) -> list[dict]:
    """Drop double-recorded rides.

    The same ride often lands twice: once from the watch (road_biking) and once
    imported from the Magene head unit (cycling). When two rides overlap for more
    than half of the shorter one, keep the one with the larger distance.
    """
    kept: list[dict] = []
    for r in sorted(rides, key=lambda r: -r["km"]):
        s, e = r["_start"], r["_start"] + dt.timedelta(seconds=r["dur_s"])
        dup = False
        for k in kept:
            ks, ke = k["_start"], k["_start"] + dt.timedelta(seconds=k["dur_s"])
            overlap = (min(e, ke) - max(s, ks)).total_seconds()
            shorter = min(r["dur_s"], k["dur_s"]) or 1
            if overlap > 0.5 * shorter:
                dup = True
                break
        if not dup:
            kept.append(r)
    return kept


def aggregate(data: dict) -> dict:
    as_of = dt.date.fromisoformat(data["as_of"])
    rides = []
    for a in data["activities"]:
        if a["type"] in RIDE_TYPES and a["km"] > 0:
            rides.append({**a, "_start": parse(a["start"])})
    rides = dedupe_rides(rides)

    this_monday = as_of - dt.timedelta(days=as_of.weekday())
    first_monday = this_monday - dt.timedelta(weeks=WEEKS - 1)
    weekly = [0.0] * WEEKS
    for r in rides:
        d = r["_start"].date()
        if first_monday <= d <= as_of:
            weekly[(d - first_monday).days // 7] += r["km"]

    since = dt.datetime.combine(as_of - dt.timedelta(days=6), dt.time())
    last7 = sum(r["km"] for r in rides if r["_start"] >= since)

    return {
        "as_of": as_of,
        "vo2max": data.get("vo2max"),
        "acute_load": data.get("acute_load"),
        "weekly": weekly,
        "last7": last7,
        "total12": sum(weekly),
    }


def fmt_int(x: float | None) -> str:
    return "—" if x is None else f"{round(x):,}"


def render(agg: dict) -> str:
    W, H = 840, 206
    stats = [
        (fmt_int(agg["vo2max"]), "", "VO₂MAX"),
        (fmt_int(agg["last7"]), "km", "LAST 7 DAYS"),
        (fmt_int(agg["total12"]), "km", "LAST 12 WEEKS"),
        (fmt_int(agg["acute_load"]), "", "7-DAY LOAD"),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Cycling telemetry from Garmin">',
        f'<title>Cycling telemetry — last 7 days {fmt_int(agg["last7"])} km, '
        f'last 12 weeks {fmt_int(agg["total12"])} km, VO2max {fmt_int(agg["vo2max"])}</title>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{SURFACE}" stroke="{BORDER}"/>',
        f'<circle cx="31" cy="31" r="4" fill="{AMBER}"/>',
        f'<text x="42" y="35" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{AMBER}">TELEMETRY</text>',
        f'<text x="{W-28}" y="35" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">'
        f'live from Garmin · updated {agg["as_of"].strftime("%b %-d, %Y")}</text>',
        f'<line x1="28" y1="52" x2="{W-28}" y2="52" stroke="{BORDER}"/>',
    ]

    # stat columns — widths sized for "54", "146 km", "1,597 km", "610"
    for x, (val, unit, label) in zip((28, 118, 238, 398), stats):
        parts.append(
            f'<text x="{x}" y="112" font-family="{SANS}" font-size="34" font-weight="700" fill="{PAPER}">'
            f'{val}<tspan font-size="14" font-weight="500" fill="{MUTED}" dx="4">{unit}</tspan></text>'
        )
        parts.append(
            f'<text x="{x}" y="136" font-family="{MONO}" font-size="10.5" letter-spacing="1.2" fill="{MUTED}">{label}</text>'
        )

    # weekly volume bars
    cx0, cx1, cy_top, cy_base = 560, W - 28, 72, 150
    weekly = agg["weekly"]
    peak = max(weekly) or 1
    slot = (cx1 - cx0) / len(weekly)
    bw = slot * 0.62
    for i, km in enumerate(weekly):
        h = max(2.0, (cy_base - cy_top) * km / peak)
        x = cx0 + i * slot + (slot - bw) / 2
        last = i == len(weekly) - 1
        op = "1" if last else "0.42"
        parts.append(
            f'<rect x="{x:.1f}" y="{cy_base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" '
            f'fill="{AMBER}" fill-opacity="{op}"/>'
        )
    parts += [
        f'<line x1="{cx0}" y1="{cy_base + 0.5}" x2="{cx1}" y2="{cy_base + 0.5}" stroke="{BORDER}"/>',
        f'<text x="{cx0}" y="{cy_base + 18}" font-family="{MONO}" font-size="10" fill="{MUTED}">12 wk ago</text>',
        f'<text x="{cx1}" y="{cy_base + 18}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}">this week</text>',
        f'<text x="{cx0}" y="{cy_top - 6}" font-family="{MONO}" font-size="10" fill="{MUTED}">'
        f'weekly ride volume · peak {fmt_int(peak)} km</text>',
    ]

    parts.append(
        f'<text x="28" y="{H - 22}" font-family="{MONO}" font-size="10" fill="{MUTED}">'
        f'road cycling · duplicate watch/head-unit recordings merged · synced weekly</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    data = json.loads((HERE / "data.json").read_text())
    agg = aggregate(data)
    (HERE / "garmin-card.svg").write_text(render(agg))
    print(
        f"as_of={agg['as_of']} last7={agg['last7']:.1f}km total12={agg['total12']:.1f}km "
        f"weekly={[round(w) for w in agg['weekly']]}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
