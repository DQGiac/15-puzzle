"""
Kiểm tra tính giải được và xáo bàn cờ ngẫu nhiên cho 15-Puzzle.
"""

import random

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)


def count_inversions(state: tuple[int, ...] | list[int]) -> int:
    """Đếm số cặp nghịch thế (inversions) trong dãy số bỏ qua ô trống 0."""
    tiles = [x for x in state if x != 0]
    n = len(tiles)
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions


def is_solvable(state: tuple[int, ...] | list[int] | list[list[int]]) -> bool:
    """
    Kiểm tra tính giải được dựa trên công thức toán học:
    (N_inv + R_blank) % 2 == 1
    (R_blank: hàng của ô trống tính từ dưới lên, 1-indexed)
    """
    if isinstance(state, list) and len(state) > 0 and isinstance(state[0], list):
        state = tuple(val for row in state for val in row)
    else:
        state = tuple(state)

    if len(state) != 16 or sorted(state) != list(range(16)):
        return False

    inversions = count_inversions(state)
    blank_idx = state.index(0)
    blank_row_top = blank_idx // 4
    blank_row_bottom = 4 - blank_row_top
    return (inversions + blank_row_bottom) % 2 == 1


def shuffle_board(steps: int = 50) -> tuple[int, ...]:
    """
    Xáo ngẫu nhiên từ GOAL_STATE bằng cách đi ngược lại `steps` bước.
    Đảm bảo trạng thái trả về luôn giải được 100%.
    """
    board = list(GOAL_STATE)
    blank_pos = 15
    last_dir = -1
    moves = [(-1, 0, -4), (1, 0, 4), (0, -1, -1), (0, 1, 1)]

    for _ in range(steps):
        valid_moves = []
        r, c = blank_pos // 4, blank_pos % 4
        for d, (dr, dc, diff) in enumerate(moves):
            # Tránh đi ngược lại ngay bước trước đó
            if last_dir != -1 and d == (last_dir ^ 1):
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < 4 and 0 <= nc < 4:
                valid_moves.append((d, diff))

        if not valid_moves:
            continue

        chosen_d, diff = random.choice(valid_moves)
        new_blank = blank_pos + diff
        board[blank_pos], board[new_blank] = board[new_blank], board[blank_pos]
        blank_pos = new_blank
        last_dir = chosen_d

    return tuple(board)
