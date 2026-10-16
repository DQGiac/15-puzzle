"""
Data model cho kết quả lượt chơi hoàn thành (ScoreRecord).
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScoreRecord:
    """Lưu trữ thông tin thành tích của người chơi."""

    player_name: str
    step_count: int
    elapsed_time: float
    date_played: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    def __lt__(self, other: "ScoreRecord") -> bool:
        """
        Nạp chồng toán tử so sánh nhỏ hơn:
        Ưu tiên số bước (step_count) ít hơn, nếu bằng nhau thì ưu tiên thời gian (elapsed_time) ít hơn.
        """
        if self.step_count != other.step_count:
            return self.step_count < other.step_count
        return self.elapsed_time < other.elapsed_time

    def __le__(self, other: "ScoreRecord") -> bool:
        return self < other or (
            self.step_count == other.step_count
            and self.elapsed_time == other.elapsed_time
        )

    def to_csv_line(self) -> str:
        """Xuất định dạng dòng CSV."""
        return f"{self.player_name},{self.step_count},{self.elapsed_time:.2f},{self.date_played}"

    @classmethod
    def from_csv_line(cls, line: str) -> "ScoreRecord":
        """Đọc từ dòng CSV."""
        parts = line.strip().split(",")
        if len(parts) >= 4:
            return cls(
                player_name=parts[0].strip(),
                step_count=int(parts[1].strip()),
                elapsed_time=float(parts[2].strip()),
                date_played=parts[3].strip(),
            )
        elif len(parts) == 3:
            return cls(
                player_name=parts[0].strip(),
                step_count=int(parts[1].strip()),
                elapsed_time=float(parts[2].strip()),
            )
        raise ValueError(f"Invalid CSV line format: {line}")
