"""Game engine operations for a 15-puzzle board."""

import random
from src.models.board_state import BoardState


class GameEngine:
    """Manage game rules and update an injected board state."""

    DIRECTIONS = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
    }

    def __init__(self, board_state: BoardState | None = None) -> None:
        self.board_state = board_state if board_state is not None else BoardState()
        self.history: list[tuple[int, int]] = []

    def reset_solved(self) -> None:
        """Reset to canonical solved state without shuffling."""
        size = self.board_state.size
        self.board_state.grid = [
            [row * size + col + 1 for col in range(size)]
            for row in range(size)
        ]
        self.board_state.grid[-1][-1] = 0
        self.board_state.empty_pos = (size - 1, size - 1)
        self.board_state.step_count = 0
        self.board_state.elapsed_time = 0.0
        self.history.clear()

    def reset_and_shuffle(self, steps: int) -> None:
        """Reset to the solved board, then perform legal random moves."""
        if type(steps) is not int or steps < 0:
            raise ValueError("steps must be a non-negative integer.")

        size = self.board_state.size
        self.board_state.grid = [
            [row * size + col + 1 for col in range(size)]
            for row in range(size)
        ]
        self.board_state.grid[-1][-1] = 0
        self.board_state.empty_pos = (size - 1, size - 1)
        self.board_state.step_count = 0
        self.board_state.elapsed_time = 0.0
        self.history.clear()

        previous_empty_pos: tuple[int, int] | None = None
        for _ in range(steps):
            valid_moves = self.get_valid_moves()
            non_reversing_moves = [
                move for move in valid_moves if move != previous_empty_pos
            ]
            if non_reversing_moves:
                valid_moves = non_reversing_moves

            current_empty_pos = self.board_state.empty_pos
            row, col = random.choice(valid_moves)
            self._internal_move(row, col)
            previous_empty_pos = current_empty_pos

        self.board_state.step_count = 0
        self.history.clear()

    def _internal_move(self, row: int, col: int) -> bool:
        """Internal move without adding to user undo history."""
        if not self.can_move(row, col):
            return False
        empty_row, empty_col = self.board_state.empty_pos
        grid = self.board_state.grid
        grid[empty_row][empty_col], grid[row][col] = (
            grid[row][col],
            grid[empty_row][empty_col],
        )
        self.board_state.empty_pos = (row, col)
        self.board_state.step_count += 1
        return True

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return coordinates of tiles adjacent to the empty cell."""
        row, col = self.board_state.empty_pos
        size = self.board_state.size
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [
            (next_row, next_col)
            for next_row, next_col in candidates
            if 0 <= next_row < size and 0 <= next_col < size
        ]

    def can_move(self, row: int, col: int) -> bool:
        """Kiểm tra ô tại (row, col) có trượt được vào ô trống không."""
        return (row, col) in self.get_valid_moves()

    def move(self, row: int, col: int) -> bool:
        """Slide an adjacent tile into the empty cell, if the move is legal."""
        if not self.can_move(row, col):
            return False

        empty_row, empty_col = self.board_state.empty_pos
        self.history.append((empty_row, empty_col))

        grid = self.board_state.grid
        grid[empty_row][empty_col], grid[row][col] = (
            grid[row][col],
            grid[empty_row][empty_col],
        )
        self.board_state.empty_pos = (row, col)
        self.board_state.step_count += 1
        return True

    def undo(self) -> bool:
        """Hoàn tác bước đi gần nhất (Undo)."""
        if not self.history:
            return False
        prev_row, prev_col = self.history.pop()
        empty_row, empty_col = self.board_state.empty_pos
        grid = self.board_state.grid
        grid[empty_row][empty_col], grid[prev_row][prev_col] = (
            grid[prev_row][prev_col],
            grid[empty_row][empty_col],
        )
        self.board_state.empty_pos = (prev_row, prev_col)
        self.board_state.step_count = max(0, self.board_state.step_count - 1)
        return True

    def can_undo(self) -> bool:
        """Kiểm tra có thể hoàn tác bước đi không."""
        return len(self.history) > 0

    def move_by_direction(self, direction: str) -> bool:
        """
        Di chuyển ô trống theo một trong 4 hướng: 'UP', 'DOWN', 'LEFT', 'RIGHT'.
        Ví dụ: 'UP' nghĩa là ô trống di chuyển lên (ô phía trên trượt xuống).
        """
        direction = direction.upper()
        if direction not in self.DIRECTIONS:
            return False

        dr, dc = self.DIRECTIONS[direction]
        empty_row, empty_col = self.board_state.empty_pos
        target_row, target_col = empty_row + dr, empty_col + dc
        size = self.board_state.size

        if 0 <= target_row < size and 0 <= target_col < size:
            return self.move(target_row, target_col)
        return False

    def is_win(self) -> bool:
        """Return whether the board is in its canonical solved arrangement."""
        size = self.board_state.size
        expected = [
            [row * size + col + 1 for col in range(size)]
            for row in range(size)
        ]
        expected[-1][-1] = 0
        return self.board_state.grid == expected
