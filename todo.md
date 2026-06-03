# TODOs

1. **Refresh the local PGN export before using the parser** — `Trial.py:61` builds and writes the archive file that `parse_pgn_features.py:91` reads, so re-run `python3 Trial.py` with a local `.env` first.

2. **Install the tracked parser dependencies in a project venv** — `requirements.txt:1` now lists `python-dotenv`, `requests`, and `python-chess`, but the current system interpreter here could not import `dotenv` or `chess` during this run.

3. **Extend the feature extractor with board-state features** — `parse_pgn_features.py:90` currently emits header-derived and game-level features only; add per-phase material or mobility metrics there once a sample PGN is available for validation.

4. **Decide whether unknown-player games should fail fast** — `parse_pgn_features.py:105` currently keeps games where `CHESS_COM_USERNAME` does not match either side and marks them `target_color=unknown`; tighten that if mixed-account PGNs are not expected.

## Future Ideas

5. **Train the first baseline model from the CSV output** — `parse_pgn_features.py:171` defines a clean per-game schema that is ready for a logistic-regression or gradient-boosting baseline once the CSV is generated.

6. **Add clock-time feature extraction instead of raw annotation counts** — `parse_pgn_features.py:61` only counts `[%clk ...]` annotations right now; parse those timestamps into usable time-pressure features when you have representative PGNs to test against.

7. **Integrate Stockfish analysis as a second-stage enrichment step** — keep the raw parser in `parse_pgn_features.py:90` focused on deterministic PGN features, then add engine evals in a separate script once local engine setup is confirmed.
