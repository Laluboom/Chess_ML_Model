import argparse
import csv
import os
import sys
from typing import Iterable


try:
    import chess.pgn
except ImportError as exc:  # pragma: no cover - exercised at runtime
    raise SystemExit(
        "Missing dependency: python-chess. Install project requirements before "
        "running parse_pgn_features.py."
    ) from exc


RESULT_POINTS = {"1-0": 1.0, "0-1": 0.0, "1/2-1/2": 0.5}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Parse a Chess.com PGN export into one CSV row per game."
    )
    parser.add_argument("input_pgn", help="Path to the PGN file exported by Trial.py")
    parser.add_argument(
        "-o",
        "--output-csv",
        help="Destination CSV path. Defaults to <input stem>_features.csv",
    )
    parser.add_argument(
        "--username",
        help=(
            "Target Chess.com username. Defaults to CHESS_COM_USERNAME, then the PGN "
            "filename stem."
        ),
    )
    return parser.parse_args()


def default_output_path(input_pgn: str) -> str:
    stem, _ = os.path.splitext(input_pgn)
    return f"{stem}_features.csv"


def infer_username(args: argparse.Namespace) -> str:
    if args.username:
        return args.username.strip().lower()
    env_username = os.getenv("CHESS_COM_USERNAME")
    if env_username:
        return env_username.strip().lower()
    return os.path.splitext(os.path.basename(args.input_pgn))[0].lower()


def safe_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def count_clock_annotations(game: chess.pgn.Game) -> int:
    count = 0
    for node in game.mainline():
        comment = node.comment or ""
        if "[%clk " in comment:
            count += 1
    return count


def castling_side(board: chess.Board, color: chess.Color) -> str:
    kingside = False
    queenside = False
    replay = chess.Board()
    for move in board.move_stack:
        moving_piece = replay.piece_at(move.from_square)
        if moving_piece and moving_piece.piece_type == chess.KING and moving_piece.color == color:
            if chess.square_file(move.from_square) == 4:
                if chess.square_file(move.to_square) == 6:
                    kingside = True
                elif chess.square_file(move.to_square) == 2:
                    queenside = True
        replay.push(move)
    if kingside:
        return "kingside"
    if queenside:
        return "queenside"
    return "none"


def iter_feature_rows(pgn_path: str, username: str) -> Iterable[dict[str, object]]:
    with open(pgn_path, "r", encoding="utf-8") as handle:
        game_index = 0
        while True:
            game = chess.pgn.read_game(handle)
            if game is None:
                break
            game_index += 1

            headers = game.headers
            white = headers.get("White", "")
            black = headers.get("Black", "")
            white_lower = white.lower()
            black_lower = black.lower()

            if username == white_lower:
                target_color = "white"
                opponent = black
                target_elo = safe_int(headers.get("WhiteElo"))
                opponent_elo = safe_int(headers.get("BlackElo"))
            elif username == black_lower:
                target_color = "black"
                opponent = white
                target_elo = safe_int(headers.get("BlackElo"))
                opponent_elo = safe_int(headers.get("WhiteElo"))
            else:
                target_color = "unknown"
                opponent = ""
                target_elo = None
                opponent_elo = None

            result = headers.get("Result", "")
            target_points = None
            if target_color == "white":
                target_points = RESULT_POINTS.get(result)
            elif target_color == "black":
                white_points = RESULT_POINTS.get(result)
                if white_points is not None:
                    target_points = 1.0 - white_points

            board = game.board()
            for move in game.mainline_moves():
                board.push(move)

            yield {
                "game_index": game_index,
                "date": headers.get("Date", ""),
                "white": white,
                "black": black,
                "white_elo": safe_int(headers.get("WhiteElo")),
                "black_elo": safe_int(headers.get("BlackElo")),
                "result": result,
                "target_color": target_color,
                "target_points": target_points,
                "target_elo": target_elo,
                "opponent": opponent,
                "opponent_elo": opponent_elo,
                "eco": headers.get("ECO", ""),
                "opening": headers.get("Opening", ""),
                "time_control": headers.get("TimeControl", ""),
                "termination": headers.get("Termination", ""),
                "ply_count": board.ply(),
                "fullmove_count": board.fullmove_number,
                "target_castling": (
                    castling_side(board, chess.WHITE)
                    if target_color == "white"
                    else castling_side(board, chess.BLACK)
                    if target_color == "black"
                    else "unknown"
                ),
                "opponent_castling": (
                    castling_side(board, chess.BLACK)
                    if target_color == "white"
                    else castling_side(board, chess.WHITE)
                    if target_color == "black"
                    else "unknown"
                ),
                "clock_annotation_count": count_clock_annotations(game),
            }


def write_csv(rows: Iterable[dict[str, object]], output_csv: str) -> int:
    fieldnames = [
        "game_index",
        "date",
        "white",
        "black",
        "white_elo",
        "black_elo",
        "result",
        "target_color",
        "target_points",
        "target_elo",
        "opponent",
        "opponent_elo",
        "eco",
        "opening",
        "time_control",
        "termination",
        "ply_count",
        "fullmove_count",
        "target_castling",
        "opponent_castling",
        "clock_annotation_count",
    ]
    row_count = 0
    with open(output_csv, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            row_count += 1
    return row_count


def main() -> int:
    args = parse_args()
    username = infer_username(args)
    output_csv = args.output_csv or default_output_path(args.input_pgn)
    row_count = write_csv(iter_feature_rows(args.input_pgn, username), output_csv)
    print(f"Wrote {row_count} games to {output_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
