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
