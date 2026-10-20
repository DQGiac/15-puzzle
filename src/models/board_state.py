"""Data model for the current state of a 15-puzzle game."""

from dataclasses import dataclass, field


@dataclass
class BoardState:
    """Store the board layout and progress for one game."""

    size: int = 4
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

    def to_tuple(self) -> tuple[int, ...]:
        """Chuyển đổi lưới 2D thành tuple 1D gồm 16 phần tử."""
        return tuple(tile for row in self.grid for tile in row)

    def clone(self) -> "BoardState":
        """Tạo một bản sao độc lập của trạng thái hiện tại."""
        from copy import deepcopy
        return BoardState(
            size=self.size,
            grid=deepcopy(self.grid),
            empty_pos=self.empty_pos,
            step_count=self.step_count,
            elapsed_time=self.elapsed_time,
        )
