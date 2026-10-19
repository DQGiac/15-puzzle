"""
Interface cơ sở cho các thuật toán giải bài toán 15-Puzzle.
"""

from abc import ABC, abstractmethod
from typing import Sequence


class BaseSolver(ABC):
    """Lớp trừu tượng định nghĩa phương thức giải bàn cờ."""

    @abstractmethod
    def solve(self, initial_state: Sequence[int] | list[list[int]]) -> list[str]:
        """
        Nhận vào trạng thái ban đầu (tuple/list 16 số hoặc ma trận 4x4).
        Trả về danh sách các bước di chuyển ('UP', 'DOWN', 'LEFT', 'RIGHT' của ô trống) để đạt Goal State.
        """
        pass
