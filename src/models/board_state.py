"""
Data model cho trạng thái bàn cờ 15-Puzzle.
"""

from dataclasses import dataclass, field
from copy import deepcopy


@dataclass
class BoardState:
    """Lưu trữ cấu hình bàn cờ và tiến trình của một ván chơi."""

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
        """Chuyển ma trận 2D thành tuple 16 phần tử (dùng cho hashing/so sánh)."""
        return tuple(val for row in self.grid for val in row)

    @classmethod
    def from_tuple(
        cls,
        state_tuple: tuple[int, ...] | list[int],
        size: int = 4,
        step_count: int = 0,
        elapsed_time: float = 0.0,
    ) -> "BoardState":
        """Khởi tạo BoardState từ tuple hoặc list 16 số."""
        if len(state_tuple) != size * size:
            raise ValueError(f"State must have exactly {size * size} elements.")

        grid = [
            list(state_tuple[r * size : (r + 1) * size])
            for r in range(size)
        ]
        empty_index = list(state_tuple).index(0)
        empty_pos = (empty_index // size, empty_index % size)

        instance = cls(
            size=size,
            grid=grid,
            empty_pos=empty_pos,
            step_count=step_count,
            elapsed_time=elapsed_time,
        )
        return instance

    def clone(self) -> "BoardState":
        """Tạo bản sao độc lập của trạng thái hiện tại."""
        return BoardState(
            size=self.size,
            grid=deepcopy(self.grid),
            empty_pos=self.empty_pos,
            step_count=self.step_count,
            elapsed_time=self.elapsed_time,
        )
