"""Storage package for 15-Puzzle."""

from src.storage.storage import (
    save_game,
    load_game,
    save_leaderboard,
    load_leaderboard,
    add_score_record,
)

__all__ = [
    "save_game",
    "load_game",
    "save_leaderboard",
    "load_leaderboard",
    "add_score_record",
]
