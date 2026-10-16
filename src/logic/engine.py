"""
Game engine xử lý luật chơi và tương tác cho bàn cờ 15-Puzzle.
"""

import random
from src.models.board_state import BoardState


class GameEngine:
    """Quản lý luật chơi, di chuyển ô cờ, xáo bàn và kiểm tra trạng thái thắng."""

    DIRECTIONS = {
        "UP": (-1, 0),     # Ô trống di chuyển lên (ô phía trên trượt xuống ô trống)
        "DOWN": (1, 0),    # Ô trống di chuyển xuống (ô phía dưới trượt lên ô trống)
        "LEFT": (0, -1),   # Ô trống di chuyển sang trái (ô bên trái trượt sang phải)
        "RIGHT": (0, 1),   # Ô trống di chuyển sang phải (ô bên phải trượt sang trái)
    }

    def __init__(self, board_state: BoardState | None = None) -> None:
        if board_state is None:
            self.board_state = BoardState()
        else:
            self.board_state = board_state

    def reset_solved(self) -> None:
        """Đặt lại bàn cờ về trạng thái đích chuẩn đã giải."""
        size = self.board_state.size
        self.board_state.grid = [
            [row * size + col + 1 for col in range(size)]
            for row in range(size)
        ]
        self.board_state.grid[-1][-1] = 0
        self.board_state.empty_pos = (size - 1, size - 1)
        self.board_state.step_count = 0
        self.board_state.elapsed_time = 0.0

    def reset_and_shuffle(self, steps: int = 50) -> None:
        """
        Xáo ngẫu nhiên bàn cờ bằng cách thực hiện `steps` bước đi hợp lệ từ trạng thái đích.
        Đảm bảo 100% bàn cờ sinh ra luôn giải được.
        """
        if steps < 0:
            raise ValueError("Số bước xáo (steps) phải >= 0.")

        self.reset_solved()
        previous_empty_pos: tuple[int, int] | None = None

        for _ in range(steps):
            valid_moves = self.get_valid_moves()
            # Tránh lùi lại vị trí vừa đi để xáo hiệu quả hơn
            non_reversing_moves = [
                pos for pos in valid_moves if pos != previous_empty_pos
            ]
            candidates = non_reversing_moves if non_reversing_moves else valid_moves
            current_empty_pos = self.board_state.empty_pos
            chosen_tile_pos = random.choice(candidates)
            self.move(*chosen_tile_pos)
            previous_empty_pos = current_empty_pos

        # Đặt lại bộ đếm bước và thời gian cho ván chơi mới
        self.board_state.step_count = 0
        self.board_state.elapsed_time = 0.0

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Trả về danh sách tọa độ (row, col) của các ô kề cạnh ô trống có thể trượt."""
        r, c = self.board_state.empty_pos
        size = self.board_state.size
        candidates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        return [
            (nr, nc)
            for nr, nc in candidates
            if 0 <= nr < size and 0 <= nc < size
        ]

    def can_move(self, row: int, col: int) -> bool:
        """Kiểm tra ô tại (row, col) có trượt được vào ô trống không."""
        return (row, col) in self.get_valid_moves()

    def move(self, row: int, col: int) -> bool:
        """
        Trượt ô cờ tại (row, col) vào ô trống nếu hợp lệ.
        Trả về True nếu di chuyển thành công.
        """
        if not self.can_move(row, col):
            return False

        er, ec = self.board_state.empty_pos
        grid = self.board_state.grid
        # Hoán vị ô cờ với ô trống
        grid[er][ec], grid[row][col] = grid[row][col], grid[er][ec]
        self.board_state.empty_pos = (row, col)
        self.board_state.step_count += 1
        return True

    def move_by_direction(self, direction: str) -> bool:
        """
        Di chuyển ô trống theo một trong 4 hướng: 'UP', 'DOWN', 'LEFT', 'RIGHT'.
        Ví dụ: 'UP' nghĩa là ô trống di chuyển lên trên (ô phía trên trượt xuống).
        """
        direction = direction.upper()
        if direction not in self.DIRECTIONS:
            return False

        dr, dc = self.DIRECTIONS[direction]
        er, ec = self.board_state.empty_pos
        target_r, target_c = er + dr, ec + dc
        size = self.board_state.size

        if 0 <= target_r < size and 0 <= target_c < size:
            return self.move(target_r, target_c)
        return False

    def is_win(self) -> bool:
        """Kiểm tra bàn cờ đã về trạng thái giải (1 -> 15 và ô trống ở cuối) chưa."""
        size = self.board_state.size
        for r in range(size):
            for c in range(size):
                expected = r * size + c + 1 if (r, c) != (size - 1, size - 1) else 0
                if self.board_state.grid[r][c] != expected:
                    return False
        return True
