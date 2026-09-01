## Victor Chun

DS + CogSci @ UC Berkeley. I build local-first tools — software that runs on your own
machine, keeps your data there, and automates something I got tired of doing by hand.

### Things I've built

**[token-counter](https://github.com/victory-c/token-counter)** — audits monthly AI coding-agent
spend across Claude Code, Codex, Cursor, and Gemini, and flags every run that would have been
fine on a cheaper model.

**[fitpet](https://github.com/victory-c/fitpet)** — a Claude Code status-line companion that
grows from real Garmin training load.

**[cal-dining-scanner](https://github.com/victory-c/cal-dining-scanner)** — watches UC Berkeley
dining menus for the foods you care about and emails you when they appear. One command to set
up, runs free on GitHub Actions.

**[magene-garmin-fix](https://github.com/victory-c/magene-garmin-fix)** — Garmin inflates climb
10–70× for third-party bike computers by throwing away barometric altitude. This fixes it.

**[bay-area-venture-map](https://github.com/victory-c/bay-area-venture-map)** —
[interactive map](https://bay-area-venture-map.vercel.app) of the Bay Area venture cluster;
filter by AUM, stage, sector, and check size.

**[qosmic-audit-harness](https://github.com/victory-c/qosmic-audit-harness)** — contracts-first
agent harness: every claim in a generated audit must cite a real crawled page, enforced by a
validator that the writer and the evaluator share.

### Open source

**[Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp)** *(1.1k ★)* — listed
contributor. Three PRs merged, all in the same vein: the server crashed on data Garmin
legitimately returns.

- [#253](https://github.com/Taxuspt/garmin_mcp/pull/253) — harden null-section handling
  across HRV, sleep, progress, and body-battery. Garmin omits whole sections for days you
  didn't wear the watch; the server assumed they were always present.
- [#254](https://github.com/Taxuspt/garmin_mcp/pull/254) — bound Garmin call duration, so
  one stalled upstream request can't hang the whole MCP server.
- [#250](https://github.com/Taxuspt/garmin_mcp/pull/250) — surface gear notes in
  `get_gear` output.

Open elsewhere:

- [**clash-verge-rev**](https://github.com/clash-verge-rev/clash-verge-rev/pulls?q=author%3Avictory-c)
  *(141k ★)* — import proxies from share links; tray menu updates without a full rebuild
- [**NousResearch/hermes-agent**](https://github.com/NousResearch/hermes-agent/pulls?q=author%3Avictory-c)
  *(239k ★)* — configurable fallback chain for web extraction; decouple Gemini reasoning
  effort from thought-summary output

### Elsewhere

Berkeley, CA — usually on a bike when I'm not here.
