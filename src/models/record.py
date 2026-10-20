"""Data model for a completed game record."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScoreRecord:
    """Store the score details for a completed game."""

    player_name: str
    step_count: int
    elapsed_time: float
    date_played: str = field(
        default_factory=lambda: datetime.now()
        .astimezone()
        .isoformat(timespec="seconds")
    )

    def __lt__(self, other: "ScoreRecord") -> bool:
        """Ưu tiên số bước ít hơn, nếu bằng nhau thì ưu tiên thời gian ít hơn."""
        if self.step_count != other.step_count:
            return self.step_count < other.step_count
        return self.elapsed_time < other.elapsed_time

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
