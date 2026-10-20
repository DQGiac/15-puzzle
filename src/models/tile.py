"""
Định nghĩa thực thể Tile (Ô cờ trong bàn cờ 15-Puzzle).

Tác dụng:
    - Lưu trữ giá trị value (0 đến 15, với 0 đại diện cho ô trống).
    - Lưu trữ vị trí hàng, cột (row, col) và tọa độ hiển thị (pixel_x, pixel_y).
"""

from dataclasses import dataclass


@dataclass
class Tile:
    """Đại diện cho một ô cờ trên bàn cờ 15-Puzzle."""
    value: int
    row: int
    col: int
    pixel_x: float = 0.0
    pixel_y: float = 0.0

    @property
    def is_empty(self) -> bool:
        """Kiểm tra xem ô này có phải là ô trống (0) không."""
        return self.value == 0

    def __repr__(self) -> str:
        return f"Tile(val={self.value}, pos=({self.row}, {self.col}))"
