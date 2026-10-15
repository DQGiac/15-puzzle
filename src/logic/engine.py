"""Game engine operations for a 15-puzzle board."""

import random

from src.models.board_state import BoardState


class GameEngine:
    """Manage game rules and update an injected board state."""

    def __init__(self, board_state: BoardState) -> None:
        self.board_state = board_state

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
            self.move(row, col)
            previous_empty_pos = current_empty_pos

        self.board_state.step_count = 0

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

    def move(self, row: int, col: int) -> bool:
        """Slide an adjacent tile into the empty cell, if the move is legal."""
        if (row, col) not in self.get_valid_moves():
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

    def is_win(self) -> bool:
        """Return whether the board is in its canonical solved arrangement."""
        size = self.board_state.size
        expected = [
            [row * size + col + 1 for col in range(size)]
            for row in range(size)
        ]
        expected[-1][-1] = 0
        return self.board_state.grid == expected
