"""
Cài đặt thuật toán IDA* (Iterative Deepening A*) giải bàn cờ 15-Puzzle.

Đặc điểm theo README.md:
    - Hàm đánh giá Heuristic: f = g + 2*h (h: khoảng cách Manhattan).
    - Sử dụng cấu trúc HashTable tùy biến để lưu vết và cắt tỉa trạng thái trùng lặp.
    - Tìm kiếm theo chiều sâu có giới hạn ngưỡng (cost threshold).
"""

import time
from typing import Sequence
from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE, is_solvable
from src.structures.hash_table import HashTable


class IDASolver(BaseSolver):
    """Bộ giải 15-Puzzle sử dụng thuật toán IDA* kết hợp HashTable."""

    # 4 hướng di chuyển của ô trống: 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
    DY = [-1, 1, 0, 0]
    DX = [0, 0, -1, 1]
    MOVE_NAMES = ["UP", "DOWN", "LEFT", "RIGHT"]

    def __init__(self, weight: float = 2.0, max_time_seconds: float = 15.0):
        self.weight = weight
        self.max_time_seconds = max_time_seconds
        self.visited = HashTable(cap=100003)
        self.nodes_expanded = 0
        self.execution_time = 0.0

    @staticmethod
    def _manhattan_distance(state: Sequence[int]) -> int:
        """Tính tổng khoảng cách Manhattan của các ô số (1-15) về vị trí đích."""
        dist = 0
        for i in range(16):
            val = state[i]
            if val == 0:
                continue
            goal_row = (val - 1) // 4
            goal_col = (val - 1) % 4
            curr_row = i // 4
            curr_col = i % 4
            dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return dist

    def _search(
        self,
        state: list[int],
        empty_pos: int,
        g: int,
        threshold: float,
        last_dir: int,
        path: list[str],
        start_time: float,
    ) -> float:
        """Duyệt sâu có giới hạn ngưỡng chi phí f."""
        self.nodes_expanded += 1

        # Kiểm tra timeout
        if time.time() - start_time > self.max_time_seconds:
            return float("inf")

        h = self._manhattan_distance(state)
        f = g + self.weight * h

        if f > threshold:
            return f

        if h == 0:
            return -1.0  # Tìm thấy đích

        state_key = tuple(state)
        prev_g = self.visited.get(state_key)
        if prev_g is not None and prev_g <= g:
            return float("inf")
        self.visited.put(state_key, g)

        min_threshold = float("inf")
        empty_row = empty_pos // 4
        empty_col = empty_pos % 4

        for d in range(4):
            # Không đi ngược lại ngay bước trước đó (0^1=1, 2^3=1)
            if last_dir != -1 and d == (last_dir ^ 1):
                continue

            new_row = empty_row + self.DY[d]
            new_col = empty_col + self.DX[d]

            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_pos = new_row * 4 + new_col
                move_name = self.MOVE_NAMES[d]

                # Hoán vị ô cờ
                state[empty_pos], state[new_pos] = state[new_pos], state[empty_pos]
                path.append(move_name)

                result = self._search(
                    state, new_pos, g + 1, threshold, d, path, start_time
                )

                if result == -1.0:
                    return -1.0

                if result < min_threshold:
                    min_threshold = result

                # Quay lui
                path.pop()
                state[empty_pos], state[new_pos] = state[new_pos], state[empty_pos]

        return min_threshold

    def solve(self, initial_state: Sequence[int] | list[list[int]]) -> list[str]:
        """
        Giải bài toán 15-Puzzle từ trạng thái ban đầu.
        Trả về danh sách các bước di chuyển của ô trống ['UP', 'LEFT', ...].
        """
        start_time = time.time()
        self.nodes_expanded = 0

        # Chuẩn hóa đầu vào về tuple 16 phần tử
        if isinstance(initial_state, list) and len(initial_state) > 0 and isinstance(initial_state[0], list):
            state_tuple = tuple(tile for row in initial_state for tile in row)
        else:
            state_tuple = tuple(initial_state)

        if not is_solvable(state_tuple):
            self.execution_time = time.time() - start_time
            return []

        if state_tuple == GOAL_STATE:
            self.execution_time = time.time() - start_time
            return []

        state = list(state_tuple)
        empty_pos = state.index(0)
        path: list[str] = []
        threshold = self.weight * self._manhattan_distance(state)

        while True:
            self.visited.clear()
            result = self._search(
                state, empty_pos, 0, threshold, -1, path, start_time
            )

            if result == -1.0:
                self.execution_time = time.time() - start_time
                return list(path)

            if result == float("inf") or time.time() - start_time > self.max_time_seconds:
                self.execution_time = time.time() - start_time
                return []

            threshold = result