"""
Cài đặt thuật toán A* Search giải bàn cờ 15-Puzzle sử dụng MinHeap và HashTable.
Dùng để so sánh hiệu năng (thời gian, bộ nhớ) với IDA* theo yêu cầu thiết kế.
"""

import time
from typing import Sequence
from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE, is_solvable
from src.structures.heap import MinHeap
from src.structures.hash_table import HashTable


class PuzzleNode:
    """Nút trạng thái trong cây tìm kiếm A*."""

    def __init__(
        self,
        state: tuple[int, ...],
        g: int = 0,
        parent: "PuzzleNode | None" = None,
        move: str = "",
    ):
        self.state = state
        self.g = g
        self.parent = parent
        self.move = move
        self.h = self._calc_manhattan()
        self.f = self.g + self.h

    def _calc_manhattan(self) -> int:
        dist = 0
        for i, val in enumerate(self.state):
            if val != 0:
                goal_r, goal_c = (val - 1) // 4, (val - 1) % 4
                curr_r, curr_c = i // 4, i % 4
                dist += abs(curr_r - goal_r) + abs(curr_c - goal_c)
        return dist

    def get_neighbors(self) -> list[tuple[tuple[int, ...], str]]:
        neighbors = []
        zero_idx = self.state.index(0)
        r, c = zero_idx // 4, zero_idx % 4
        directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for dr, dc, move_name in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                new_idx = nr * 4 + nc
                new_state = list(self.state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append((tuple(new_state), move_name))
        return neighbors

    def __lt__(self, other: "PuzzleNode") -> bool:
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f


class AStarSolver(BaseSolver):
    """Bộ giải 15-Puzzle sử dụng thuật toán A* tiêu chuẩn."""

    def __init__(self, max_nodes: int = 50000, max_time_seconds: float = 10.0):
        self.max_nodes = max_nodes
        self.max_time_seconds = max_time_seconds
        self.nodes_expanded = 0
        self.execution_time = 0.0

    def solve(self, initial_state: Sequence[int] | list[list[int]]) -> list[str]:
        start_time = time.time()
        self.nodes_expanded = 0

        if isinstance(initial_state, list) and len(initial_state) > 0 and isinstance(initial_state[0], list):
            state_tuple = tuple(val for row in initial_state for val in row)
        else:
            state_tuple = tuple(initial_state)

        if not is_solvable(state_tuple):
            self.execution_time = time.time() - start_time
            return []

        if state_tuple == GOAL_STATE:
            self.execution_time = time.time() - start_time
            return []

        open_set = MinHeap()
        visited = HashTable(cap=100003)

        start_node = PuzzleNode(state_tuple)
        open_set.push(start_node)
        visited.put(state_tuple, 0)

        while not open_set.is_empty():
            self.nodes_expanded += 1
            if time.time() - start_time > self.max_time_seconds or self.nodes_expanded > self.max_nodes:
                break

            cur: PuzzleNode = open_set.pop()

            if cur.state == GOAL_STATE:
                path = []
                node = cur
                while node and node.move:
                    path.append(node.move)
                    node = node.parent
                self.execution_time = time.time() - start_time
                return path[::-1]

            cur_best_g = visited.get(cur.state)
            if cur_best_g is not None and cur.g > cur_best_g:
                continue

            for next_state, move_name in cur.get_neighbors():
                next_g = cur.g + 1
                best_g = visited.get(next_state)

                if best_g is None or next_g < best_g:
                    visited.put(next_state, next_g)
                    neighbor_node = PuzzleNode(next_state, next_g, cur, move_name)
                    open_set.push(neighbor_node)

        self.execution_time = time.time() - start_time
        return []
