## Victor Chun

DS + CogSci @ UC Berkeley. I build local-first tools — software that runs on your own
machine, keeps your data there, and automates something I got tired of doing by hand.

### Things I've built

**[token-counter](https://github.com/victory-c/token-counter)** — audits monthly AI coding-agent
spend across Claude Code, Codex, Cursor, and Gemini, and flags every run that would have been
fine on a cheaper model.

**[fitpet](https://github.com/victory-c/fitpet)** — a Claude Code status-line companion that
grows from real Garmin training load.

**[vibeapply](https://github.com/victory-c/vibeapply)** — an AI-native job-application
copilot: a browser extension that rides along on job boards, backed by a structured candidate
profile and evidence bank. Scaffolded with agents, then audited — all nine findings fixed
before any feature work.

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

#### [Taxuspt/garmin_mcp](https://github.com/Taxuspt/garmin_mcp) — *1.1k ★, listed contributor*

Garmin's API returns explicit `null` for sections you have no data in, so `resp.get(k, {})`
yields `None` — the default only applies when the key is *absent*. Most of my merged work
there is that bug and its relatives.

| | |
|---|---|
| [**#253**](https://github.com/Taxuspt/garmin_mcp/pull/253) ✅ merged | Five unguarded null-section crashes — HRV baseline, progress-summary `.items()`, the sleep-score chain, body-battery event iteration, and a GraphQL `{"data": null}` that slipped past the existing guard. Each fix ships a regression test feeding the explicit-null payload. |
| [**#254**](https://github.com/Taxuspt/garmin_mcp/pull/254) ✅ merged | Garmin occasionally stalls a request indefinitely; because every tool calls the client synchronously, one stalled call hung the *whole* MCP server until the client's ~4-minute timeout fired (issue #248). Bounds each proxied call on a daemon worker thread, surfacing a retry-able `TimeoutError` instead. Configurable via `GARMIN_MCP_CALL_TIMEOUT`. |
| [**#250**](https://github.com/Taxuspt/garmin_mcp/pull/250) ✅ merged | Gear notes never appeared, because the pinned client reads the legacy `filterGear` endpoint and Notes only exists on `/gear/v2/list`. Joins the two — the v2 response hyphenates its UUIDs and the legacy one doesn't, so the join normalizes them first. |
| [**#276**](https://github.com/Taxuspt/garmin_mcp/pull/276) | Per-sport heart-rate zone reads and writes, via read-modify-write so unrelated sport profiles aren't clobbered. Verified against a live account; documents the quirk that Garmin won't persist a `CUSTOM` calculation method. |
| [**#170**](https://github.com/Taxuspt/garmin_mcp/pull/170) | There's a Dockerfile but no published image, so everyone builds locally. Publishes multi-arch (amd64 + arm64) images to GHCR on release — no extra secrets, just `GITHUB_TOKEN`. |
| [**#167**](https://github.com/Taxuspt/garmin_mcp/pull/167) | The security workflow had a `# Add pip-audit here if desired` placeholder where the dependency scan should be. Wires up `pip-audit` and clears the one CVE it flags — h11 request smuggling (CVE-2025-43859). |

#### [clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev) — *141k ★*

- [**#7672**](https://github.com/clash-verge-rev/clash-verge-rev/pull/7672) — importing a single
  `vless://` / `trojan://` / `ss://` share link required creating a throwaway subscription and
  pasting URIs into Edit Proxy. Adds real import.
- [**#7652**](https://github.com/clash-verge-rev/clash-verge-rev/pull/7652) — every proxy
  selection rebuilt the entire native tray menu. On profiles with thousands of nodes that meant
  stalls and memory spikes. Caches menu handles and updates only the two items that changed.

#### [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — *239k ★*

- [**#64036**](https://github.com/NousResearch/hermes-agent/pull/64036) — reasoning-visibility
  leak on Gemini/Vertex: with `show_reasoning: false`, users still got dozens of raw
  thought-summary blocks. Two causes — effort and visibility were coupled in the request
  builder, and Vertex returns summaries *untagged* unless you set `thought_tag_marker`, so
  nothing downstream could key on them. Splits the two knobs to match Google's own API.
- [**#68524**](https://github.com/NousResearch/hermes-agent/pull/68524) — `web_extract` had one
  backend; expired credits or a rate limit meant total failure plus a gateway restart. Adds a
  configurable fallback chain.

### Elsewhere

Berkeley, CA — usually on a bike when I'm not here.
