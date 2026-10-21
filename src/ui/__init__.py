"""
Package src.ui: Giao diện người dùng cho dự án 15-Puzzle.
"""

from src.ui.tab_puzzle import render_tab_puzzle
from src.ui.tab_benchmark import render_tab_benchmark
from src.ui.tab_leaderboard import render_tab_leaderboard
from src.ui.theme import inject_theme_system

__all__ = [
    "render_tab_puzzle",
    "render_tab_benchmark",
    "render_tab_leaderboard",
    "inject_theme_system",
]
