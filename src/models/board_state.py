"""Data model for the current state of a 15-puzzle game."""

from dataclasses import dataclass, field


@dataclass
class BoardState:
    """Store the board layout and progress for one game."""

    size: int = field(default=4, init=False)
    grid: list[list[int]] = field(
        default_factory=lambda: [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0],
        ]
    )
    empty_pos: tuple[int, int] = (3, 3)
    step_count: int = 0
    elapsed_time: float = 0.0
