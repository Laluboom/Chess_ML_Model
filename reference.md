# Reference — Chess ML Model

_Last refreshed: 2026-06-03_

## Purpose
Collect Chess.com game history as a PGN archive, then convert it into structured per-game features for later ML work.

## Stack
- Python 3
- `requests`, `python-dotenv`, `python-chess`
- Chess.com public API (no auth required)

## Entry Points
```bash
cp .env.example .env
# Fill in CHESS_COM_USERNAME and optional contact/output values.
python3 Trial.py
# Fetches all archives for CHESS_COM_USERNAME and writes CHESS_COM_OUTPUT_FILE.

python3 parse_pgn_features.py chess_games.pgn
# Reads a PGN export and writes chess_games_features.csv by default.
# Use --username if the filename does not match the target Chess.com account.
```

## Key Files
| File | Role |
|------|------|
| `Trial.py` | Archive fetcher — pulls all monthly PGN bundles from chess.com API and writes to a single file |
| `parse_pgn_features.py` | Converts a PGN export into one CSV row per game with outcome, rating, opening, move-count, castling, and clock-annotation features |
| `.env.example` | Template for local Chess.com username, optional contact email, and output path |
| `requirements.txt` | Runtime Python dependencies |
| `*.pgn` | Local game exports — ignored by Git |

## Current Run Status
Feature extraction code now exists locally, but it was not executed in this environment because no tracked PGN export is available and `python-dotenv` / `python-chess` are not installed in the system interpreter here. Syntax verification passed for both Python entry points.
