# Reference — Chess ML Model

_Last refreshed: 2026-05-29_

## Purpose
Collect all chess.com game history for user `laluboom` as a PGN archive for use in a future ML pipeline. Currently data-collection only — no model code exists yet.

## Stack
- Python 3, `requests`
- chess.com Public API (no auth required)

## Entry Point
```bash
python3 Trial.py
# Fetches all archives for 'laluboom', writes laluboom_all_games.pgn
# Respects rate limits with 1s sleep between requests; auto-retries on 429
```

## Key Files
| File | Role |
|------|------|
| `Trial.py` | Archive fetcher — pulls all monthly PGN bundles from chess.com API and writes to a single file |
| `laluboom_all_games.pgn` | Current game archive — 932 games, 23,304 lines |

## Dataset Snapshot (as of last fetch)
- **Games:** 932
- **Results:** 435 wins (1-0) · 457 losses (0-1) · 40 draws — win rate ~46.7%
- **Time controls:** 3+2 blitz (417), 10min rapid (196), 2+1 bullet (83), daily (76), others
- **Date range:** 2020-08-23 onwards

## Run Status (2026-05-29)
Syntax check passed. API live-tested — chess.com returned HTTP 200, **19 archives found**, latest is **April 2026**. The on-disk PGN is stale and missing recent games. `requests` available in system Python — `Trial.py` can run as-is.
