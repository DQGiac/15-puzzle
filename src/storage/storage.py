"""
Module quản lý lưu trữ (Storage) cho dự án 15-Puzzle.

Chức năng theo README.md:
    - Lưu trữ Bảng xếp hạng (Leaderboard): Lưu dữ liệu Top 10 lượt chơi vào file CSV.
    - Lưu trữ Trạng thái ván đấu: File save.dat chụp ảnh snapshot bàn cờ (16 số, số bước, thời gian).
"""

import csv
import json
from pathlib import Path
from src.models.board_state import BoardState
from src.models.record import ScoreRecord

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DEFAULT_SAVE_FILE = DEFAULT_DATA_DIR / "save.dat"
DEFAULT_LEADERBOARD_FILE = DEFAULT_DATA_DIR / "leaderboard.csv"


def ensure_data_dir(filepath: Path | str) -> Path:
    """Đảm bảo thư mục cha tồn tại."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_game(board_state: BoardState, filepath: Path | str = DEFAULT_SAVE_FILE) -> bool:
    """
    Lưu trạng thái ván đấu hiện tại vào file save.dat.
    Nội dung bao gồm mảng 16 số, số bước đi và thời gian đã trôi qua.
    """
    path = ensure_data_dir(filepath)

    # Đảm bảo empty_pos chuẩn xác theo vị trí ô số 0 trong grid
    empty_pos = board_state.empty_pos
    for r in range(board_state.size):
        for c in range(len(board_state.grid[r])):
            if board_state.grid[r][c] == 0:
                empty_pos = (r, c)
                break

    data = {
        "grid": board_state.grid,
        "empty_pos": list(empty_pos),
        "step_count": board_state.step_count,
        "elapsed_time": float(board_state.elapsed_time),
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Lỗi khi lưu game vào {path}: {e}")
        return False


def load_game(filepath: Path | str = DEFAULT_SAVE_FILE) -> BoardState | None:
    """
    Tải trạng thái ván đấu từ file save.dat.
    Trả về đối tượng BoardState hoặc None nếu file không hợp lệ.
    """
    path = Path(filepath)
    if not path.is_file():
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        grid = data["grid"]
        size = len(grid)

        # Tự động tìm vị trí ô trống 0 trong grid để đảm bảo tính toàn vẹn
        empty_pos = None
        for r in range(size):
            for c in range(len(grid[r])):
                if grid[r][c] == 0:
                    empty_pos = (r, c)
                    break
            if empty_pos is not None:
                break

        if empty_pos is None:
            empty_pos = tuple(data.get("empty_pos", (size - 1, size - 1)))

        step_count = data.get("step_count", 0)
        elapsed_time = data.get("elapsed_time", 0.0)

        return BoardState(
            size=size,
            grid=grid,
            empty_pos=empty_pos,
            step_count=step_count,
            elapsed_time=elapsed_time,
        )
    except Exception as e:
        print(f"Lỗi khi tải game từ {path}: {e}")
        return None


def load_leaderboard(filepath: Path | str = DEFAULT_LEADERBOARD_FILE) -> list[ScoreRecord]:
    """
    Tải danh sách bảng xếp hạng từ file CSV.
    Tự động sắp xếp ưu tiên số bước ít hơn, sau đó thời gian ngắn hơn.
    """
    path = Path(filepath)
    if not path.is_file():
        default_mock = [
            ScoreRecord(player_name="Antigravity", step_count=38, elapsed_time=15.2),
            ScoreRecord(player_name="Player 1", step_count=45, elapsed_time=18.0),
            ScoreRecord(player_name="Player 2", step_count=58, elapsed_time=23.6),
        ]
        save_leaderboard(default_mock, filepath)
        return default_mock

    records: list[ScoreRecord] = []
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)

            # Bỏ qua dòng tiêu đề chuẩn xác (chỉ bỏ qua nếu là header thật)
            rows_to_process = list(reader)
            if header:
                # Nếu dòng đầu tiên không phải header (ví dụ file CSV không có header)
                is_header = False
                if len(header) >= 2:
                    col0 = header[0].strip().lower()
                    col1 = header[1].strip()
                    if col0 in ("playername", "player_name", "name") or not col1.isdigit():
                        is_header = True
                if not is_header:
                    rows_to_process.insert(0, header)

            for parts in rows_to_process:
                if not parts:
                    continue
                # Bỏ qua dòng comment
                if parts[0].strip().startswith("#"):
                    continue
                try:
                    if len(parts) >= 4:
                        records.append(
                            ScoreRecord(
                                player_name=parts[0].strip(),
                                step_count=int(parts[1].strip()),
                                elapsed_time=float(parts[2].strip()),
                                date_played=parts[3].strip(),
                            )
                        )
                    elif len(parts) == 3:
                        records.append(
                            ScoreRecord(
                                player_name=parts[0].strip(),
                                step_count=int(parts[1].strip()),
                                elapsed_time=float(parts[2].strip()),
                            )
                        )
                except ValueError:
                    continue

        records.sort()
        return records[:10]
    except Exception as e:
        print(f"Lỗi khi tải leaderboard từ {path}: {e}")
        return []


def save_leaderboard(
    records: list[ScoreRecord],
    filepath: Path | str = DEFAULT_LEADERBOARD_FILE,
) -> bool:
    """Lưu danh sách xếp hạng vào file CSV."""
    path = ensure_data_dir(filepath)
    records.sort()
    top_10 = records[:10]
    try:
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["PlayerName", "StepCount", "ElapsedTime", "DatePlayed"])
            for rec in top_10:
                writer.writerow([
                    rec.player_name,
                    rec.step_count,
                    f"{rec.elapsed_time:.2f}",
                    rec.date_played,
                ])
        return True
    except Exception as e:
        print(f"Lỗi khi lưu leaderboard vào {path}: {e}")
        return False


def add_score_record(
    record: ScoreRecord,
    filepath: Path | str = DEFAULT_LEADERBOARD_FILE,
) -> list[ScoreRecord]:
    """Thêm một kỷ lục mới vào bảng xếp hạng, sắp xếp và giữ lại Top 10."""
    current = load_leaderboard(filepath)
    current.append(record)
    current.sort()
    top_10 = current[:10]
    save_leaderboard(top_10, filepath)
    return top_10
