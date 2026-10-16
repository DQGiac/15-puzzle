"""Algorithms package for 15-Puzzle."""

from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE, count_inversions, is_solvable, shuffle_board
from src.algorithms.ida_solver import IDASolver
from src.algorithms.a_star_solver import AStarSolver

__all__ = [
    "BaseSolver",
    "GOAL_STATE",
    "count_inversions",
    "is_solvable",
    "shuffle_board",
    "IDASolver",
    "AStarSolver",
]
