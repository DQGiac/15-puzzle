"""Validation helpers for puzzle board states."""


def check_solvable(grid: list[list[int]]) -> bool:
    """Return whether a rectangular sliding-puzzle board is solvable."""
    if not grid or not grid[0]:
        raise ValueError("Grid must be a non-empty rectangular matrix.")

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
