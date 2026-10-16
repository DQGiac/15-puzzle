"""
Module kiểm tra tính hợp lệ và tính giải được của bàn cờ 15-Puzzle.

Quy tắc toán học (theo README.md):
    - Tính số nghịch thế (Inversions - N_inv) bỏ qua ô trống (0).
    - Vị trí hàng của ô trống tính từ dưới lên (R_blank, 1-indexed: hàng dưới cùng là 1, hàng trên cùng là 4).
    - Bàn cờ 4x4 giải được khi và chỉ khi: (N_inv + R_blank) % 2 == 1.
"""

from typing import Sequence


def count_inversions(state: Sequence[int]) -> int:
    """Đếm số cặp nghịch thế (inversions) trong dãy số, bỏ qua ô trống (0)."""
    tiles = [x for x in state if x != 0]
    n = len(tiles)
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions


def check_solvable(grid_or_state: Sequence[int] | list[list[int]]) -> bool:
    """
    Kiểm tra một bàn cờ có giải được hay không theo công thức:
    (N_inv + R_blank) % 2 == 1
    """
    if not grid_or_state:
        return False

    # Chuyển đổi về danh sách 1D nếu đầu vào là ma trận 2D
    if isinstance(grid_or_state[0], (list, tuple)):
        flat_state = [val for row in grid_or_state for val in row]
    else:
        flat_state = list(grid_or_state)

    if len(flat_state) != 16:
        return False

    # Đảm bảo chứa đầy đủ các số từ 0 đến 15 không trùng lặp
    if sorted(flat_state) != list(range(16)):
        return False

    inversions = count_inversions(flat_state)
    blank_idx = flat_state.index(0)
    blank_row_top = blank_idx // 4
    blank_row_bottom = 4 - blank_row_top  # 1-indexed từ dưới lên

    return (inversions + blank_row_bottom) % 2 == 1


def is_solvable(state: Sequence[int] | list[list[int]]) -> bool:
    """Alias cho check_solvable."""
    return check_solvable(state)


def parse_and_validate_input(raw_input: str) -> tuple[bool, str, list[list[int]] | None]:
    """
    Phân tích chuỗi đầu vào (dấu phẩy, khoảng trắng, hoặc xuống dòng) thành ma trận 4x4.
    Trả về (is_valid, message, grid).
    """
    cleaned = raw_input.replace(",", " ").replace("\n", " ").strip()
    if not cleaned:
        return False, "Chuỗi đầu vào rỗng.", None

    tokens = cleaned.split()
    if len(tokens) != 16:
        return False, f"Cần đúng 16 số (nhận được {len(tokens)} số).", None

    try:
        numbers = [int(tok) for tok in tokens]
    except ValueError:
        return False, "Tất cả các phần tử phải là số nguyên hợp lệ.", None

    if sorted(numbers) != list(range(16)):
        return False, "Bàn cờ phải chứa chính xác các số từ 0 đến 15 (0 là ô trống).", None

    if not check_solvable(numbers):
        return False, "Bàn cờ này VÔ NGHIỆM theo công thức (N_inv + R_blank) % 2 == 1.", None

    grid = [numbers[i * 4 : (i + 1) * 4] for i in range(4)]
    return True, "Bàn cờ hợp lệ và giải được!", grid
