# Reference — Chess ML Model

_Last refreshed: 2026-05-29_

## Purpose
Collect Chess.com game history as a PGN archive for use in a future ML pipeline. Currently data-collection only — no model code exists yet.

## Stack
- Python 3, `requests`
- chess.com Public API (no auth required)

## Entry Point
```bash
cp .env.example .env
# Fill in CHESS_COM_USERNAME and optional contact/output values.
python3 Trial.py
# Fetches all archives for CHESS_COM_USERNAME and writes CHESS_COM_OUTPUT_FILE.
# Respects rate limits with 1s sleep between requests; auto-retries on 429
```

## Key Files
| File | Role |
|------|------|
| `Trial.py` | Archive fetcher — pulls all monthly PGN bundles from chess.com API and writes to a single file |
| `.env.example` | Template for local Chess.com username, optional contact email, and output path |
| `requirements.txt` | Runtime Python dependencies |
| `*.pgn` | Local game exports — ignored by Git |

## Run Status (2026-05-29)
Syntax check passed. API access was previously live-tested successfully. Local PGN exports are ignored and should be refreshed outside Git before building the ML pipeline.
