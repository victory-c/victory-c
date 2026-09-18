# telemetry

The Garmin card on the profile README.

- `garmin-card.svg` — the card, re-rendered every Sunday night by a local scheduled task
- `render_card.py` — deterministic renderer; reads a local, git-ignored `data.json`
  (aggregates only — no activity names or locations) fetched through the Garmin MCP.
  It never talks to Garmin or touches auth tokens.
