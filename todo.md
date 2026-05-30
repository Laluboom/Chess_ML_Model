# TODOs

1. **Re-run `Trial.py` to refresh the PGN** — the API confirmed 19 archives with the latest being April 2026, but the on-disk PGN only captures older games. Run `python3 Trial.py` to pull the full up-to-date history before building anything on top of the data.

2. **Add a PGN parser to extract ML features** — the raw PGN is not directly usable for ML. Use `python-chess` (`pip install chess`) to parse each game and extract structured features per game: opening ECO code, number of moves, material balance at various points, castling side, clock usage, blunder/inaccuracy counts (if clock data allows), and result. Write these to a CSV or dataframe so the data is model-ready.

3. **Add `requirements.txt` and `.gitignore`** — the project has no dependency file (`requests` and `python-chess` should be listed) and no `.gitignore`. The PGN contains your personal username and game history — decide whether you want it tracked in git or excluded.

---

## Future Ideas

4. **Win probability model by opening** — with 932+ games and ECO codes already in the PGN headers, you can train a simple classifier (logistic regression or gradient boosting) to predict win/loss/draw probability by opening. Enough data for blitz (417 games in 3+2 alone) to get meaningful signals. Could answer: "which openings do you actually win with vs just play?"

5. **Personal weakness detection** — parse clock usage and move quality across game phases (opening/middlegame/endgame). If you consistently lose on time or blunder in the endgame, that's a measurable pattern. Needs clock data from the PGN `{[%clk ...]}` annotations, which are already present in the file.

6. **Style fingerprinting** — extract features like average game length, pawn structure tendencies, exchange frequency, king safety metrics. Could characterise your playing style and compare it across your Elo progression over time (you went from ~233 Elo in 2022 to ~1200+ — how did the style change?).

7. **Opening recommendation engine** — given your win rates by ECO code and colour (White vs Black), build a small recommender that suggests which openings to study or drop. Could integrate with a chess opening database to pull suggested study lines. Open question: do you want this as a CLI tool or a simple web UI?

8. **Opponent modelling** — the PGN has opponent usernames and Elos. Could cluster opponents by rating band and analyse which types of players you struggle against most, or detect if certain opponent playstyles (aggressive/positional) correlate with your losses.

9. **Stockfish eval integration** — run games through Stockfish (local engine) to get centipawn loss per move and accuracy scores. This is the gold-standard feature set for chess ML and would make the model far more powerful than metadata alone. Computationally expensive for 932+ games but doable offline.
