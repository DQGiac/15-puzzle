"""Validation helpers for puzzle board states."""

from typing import Sequence
from src.algorithms.solvability import (
    count_inversions,
    is_solvable as _algo_is_solvable,
)


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

    # Sử dụng logic toán học chuẩn từ solvability module
    return _algo_is_solvable(tiles)


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
