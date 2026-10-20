"""
Cài đặt thuật toán IDA* (Iterative Deepening A*) giải bài toán 15-Puzzle.
Kết hợp hàm Heuristic Manhattan có trọng số f = g + weight * h và bảng băm
để phát hiện và cắt tỉa chu trình trên nhánh tìm kiếm.
"""

import time
from typing import Sequence
from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE, is_solvable
from src.structures.hash_table import HashTable


class IDASolver(BaseSolver):
    """Bộ giải 15-Puzzle sử dụng thuật toán Iterative Deepening A*."""

    DY = [-1, 1, 0, 0]
    DX = [0, 0, -1, 1]
    # 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
    MOVE_NAMES = ["UP", "DOWN", "LEFT", "RIGHT"]

    def __init__(self, weight: float = 2.0):
        self._weight = float(weight)
        self._visited = HashTable(cap=100003)
        self.nodes_expanded: int = 0
        self.execution_time: float = 0.0

    def _manhattan_distance(self, state: list[int] | tuple[int, ...]) -> int:
        """Tính tổng khoảng cách Manhattan của bàn cờ về vị trí đích."""
        dist = 0
        for i in range(16):
            val = state[i]
            if val == 0:
                continue
            goal_row = (val - 1) // 4
            goal_col = (val - 1) % 4
            dist += abs(i // 4 - goal_row) + abs(i % 4 - goal_col)
        return dist

    def _search(
        self,
        state: list[int],
        empty_pos: int,
        g: int,
        threshold: float,
        last_dir: int,
        path: list[str],
    ) -> float:
        """Hàm tìm kiếm đệ quy có chặn ngưỡng chi phí (f-limit) và phát hiện chu trình."""
        self.nodes_expanded += 1
        h = self._manhattan_distance(state)
        f = g + self._weight * h

        if f > threshold:
            return f
        if h == 0:
            return -1.0

        state_key = tuple(state)
        if self._visited.contains(state_key):
            return float("inf")

        # Đánh dấu trạng thái trên nhánh tìm kiếm hiện tại để tránh chu trình
        self._visited.put(state_key, True)

        min_threshold = float("inf")
        empty_row = empty_pos // 4
        empty_col = empty_pos % 4

        for d in range(4):
            # Cắt tỉa bước đi ngược lại bước ngay trước đó (0 <-> 1, 2 <-> 3)
            if last_dir != -1 and d == (last_dir ^ 1):
                continue

            new_row = empty_row + self.DY[d]
            new_col = empty_col + self.DX[d]

            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_pos = new_row * 4 + new_col
                move_name = self.MOVE_NAMES[d]

                state[empty_pos], state[new_pos] = state[new_pos], state[empty_pos]
                path.append(move_name)

                result = self._search(state, new_pos, g + 1, threshold, d, path)
                if result == -1.0:
                    return -1.0
                if result < min_threshold:
                    min_threshold = result

                path.pop()
                state[empty_pos], state[new_pos] = state[new_pos], state[empty_pos]

        # Backtrack: Gỡ trạng thái khỏi nhánh tìm kiếm hiện tại
        self._visited.remove(state_key)
        return min_threshold

    def solve(self, initial_state: Sequence[int] | list[list[int]]) -> list[str]:
        """
        Giải bàn cờ từ trạng thái ban đầu.
        Trả về danh sách các hướng di chuyển ['UP', 'DOWN', 'LEFT', 'RIGHT'] của ô trống.
        """
        start_time = time.perf_counter()
        self.nodes_expanded = 0
        self.execution_time = 0.0

        if isinstance(initial_state, list) and len(initial_state) > 0 and isinstance(initial_state[0], list):
            initial_tuple = tuple(tile for row in initial_state for tile in row)
        else:
            initial_tuple = tuple(initial_state)

        if not is_solvable(initial_tuple):
            self.execution_time = time.perf_counter() - start_time
            return []

        if initial_tuple == GOAL_STATE:
            self.execution_time = time.perf_counter() - start_time
            return []

        state = list(initial_tuple)
        empty_pos = state.index(0)
        path: list[str] = []
        threshold = float(self._weight * self._manhattan_distance(state))

        while True:
            self._visited.clear()
            result = self._search(state, empty_pos, 0, threshold, -1, path)
            if result == -1.0:
                self.execution_time = time.perf_counter() - start_time
                return path
            if result == float("inf"):
                self.execution_time = time.perf_counter() - start_time
                return []
            threshold = result
