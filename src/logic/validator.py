"""Validation helpers for puzzle board states."""


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


def check_solvable(grid: list[list[int]] | Sequence[int]) -> bool:
    """Return whether a rectangular sliding-puzzle board is solvable."""
    if not grid:
        return False

    if not isinstance(grid[0], (list, tuple)):
        flat = list(grid)
        if len(flat) != 16:
            return False
        grid = [flat[i * 4 : (i + 1) * 4] for i in range(4)]

    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("Grid must be a non-empty rectangular matrix.")

    tile_count = len(grid) * width
    tiles = [tile for row in grid for tile in row]
    if any(type(tile) is not int for tile in tiles) or sorted(tiles) != list(
        range(tile_count)
    ):
        raise ValueError("Grid must contain each integer from 0 to N-1 exactly once.")

    blank_index = tiles.index(0)
    blank_row_from_bottom = len(grid) - blank_index // width
    inversions = sum(
        earlier > later
        for index, earlier in enumerate(tiles)
        if earlier != 0
        for later in tiles[index + 1 :]
        if later != 0
    )

    if width % 2 == 1:
        return inversions % 2 == 0
    return (inversions + blank_row_from_bottom) % 2 == 1


def is_solvable(state: Sequence[int] | list[list[int]]) -> bool:
    """Alias cho check_solvable."""
    try:
        return check_solvable(state)
    except ValueError:
        return False


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

    grid = [numbers[i * 4 : (i + 1) * 4] for i in range(4)]
    try:
        if not check_solvable(grid):
            return False, "Bàn cờ này VÔ NGHIỆM theo công thức (N_inv + R_blank) % 2 == 1.", None
    except ValueError as e:
        return False, f"Lỗi bàn cờ: {e}", None

    return True, "Bàn cờ hợp lệ và giải được!", grid

