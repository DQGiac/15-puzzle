"""
Unit tests for 15-Puzzle core modules and algorithms.
"""

from src.structures.hash_table import HashTable
from src.structures.heap import MinHeap
from src.models.board_state import BoardState
from src.models.record import ScoreRecord
from src.logic.validator import check_solvable, count_inversions, parse_and_validate_input
from src.logic.engine import GameEngine
from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE, shuffle_board
from src.algorithms.ida_solver import IDASolver
from src.algorithms.a_star_solver import AStarSolver


def test_hash_table():
    ht = HashTable(cap=17)
    ht.put("state1", 5)
    ht.put("state2", 10)
    assert ht.get("state1") == 5
    assert ht.get("state2") == 10
    assert ht.contains("state1") is True
    assert ht.contains("state3") is False
    assert len(ht) == 2

    # Update key
    ht.put("state1", 3)
    assert ht.get("state1") == 3
    assert len(ht) == 2

    # Remove existing key
    assert ht.remove("state1") is True
    assert ht.contains("state1") is False
    assert len(ht) == 1

    # Remove non-existing key returns False
    assert ht.remove("nonexistent") is False

    # Store None value
    ht.put("null_val", None)
    assert ht["null_val"] is None

    # Clear
    ht.clear()
    assert len(ht) == 0


def test_min_heap():
    heap = MinHeap()
    heap.push(10)
    heap.push(3)
    heap.push(7)
    heap.push(1)
    assert heap.pop() == 1
    assert heap.pop() == 3
    assert heap.pop() == 7
    assert heap.pop() == 10
    assert heap.is_empty() is True
    assert heap.pop() is None


def test_solvability():
    # Solved state should be solvable
    assert check_solvable(list(GOAL_STATE)) is True

    # Swapping 14 and 15 should make it unsolvable
    unsolvable = list(GOAL_STATE)
    unsolvable[13], unsolvable[14] = unsolvable[14], unsolvable[13]
    assert check_solvable(unsolvable) is False

    # Reverse test cases
    assert check_solvable((0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)) is True
    assert check_solvable((15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)) is False

    # Scrambled board must always be solvable
    scrambled = shuffle_board(20)
    assert check_solvable(scrambled) is True


def test_game_engine():
    engine = GameEngine()
    engine.reset_solved()
    assert engine.is_win() is True

    # Initial valid moves adjacent to empty slot (3, 3) are (2, 3) and (3, 2)
    valid = engine.get_valid_moves()
    assert (2, 3) in valid
    assert (3, 2) in valid
    assert (0, 0) not in valid

    # Move tile from (2, 3) -> value 12 slides down into (3, 3)
    assert engine.move(2, 3) is True
    assert engine.board_state.empty_pos == (2, 3)
    assert engine.board_state.step_count == 1
    assert engine.is_win() is False

    # Slide it back
    assert engine.move(3, 3) is True
    assert engine.board_state.empty_pos == (3, 3)
    assert engine.board_state.step_count == 2
    assert engine.is_win() is True

    # Test Undo feature
    assert engine.can_undo() is True
    assert engine.undo() is True
    assert engine.board_state.empty_pos == (2, 3)
    assert engine.board_state.step_count == 1
    assert engine.is_win() is False
    assert engine.undo() is True
    assert engine.board_state.empty_pos == (3, 3)
    assert engine.board_state.step_count == 0
    assert engine.is_win() is True
    assert engine.can_undo() is False
    assert engine.undo() is False


def test_ida_solver_short():
    engine = GameEngine()
    engine.reset_solved()
    engine.move(2, 3)  # UP
    engine.move(2, 2)  # LEFT
    engine.move(3, 2)  # DOWN

    solver = IDASolver(weight=2.0)
    assert isinstance(solver, BaseSolver)
    assert solver._weight == 2.0

    solution = solver.solve(engine.board_state.to_tuple())
    assert len(solution) > 0
    assert solver.nodes_expanded > 0
    assert solver.execution_time > 0

    # Apply solution moves to check if it reaches goal
    for move_name in solution:
        engine.move_by_direction(move_name)
    assert engine.is_win() is True


def test_a_star_solver_short():
    engine = GameEngine()
    engine.reset_solved()
    engine.move(2, 3)  # UP
    engine.move(2, 2)  # LEFT
    engine.move(3, 2)  # DOWN

    solver = AStarSolver()
    assert isinstance(solver, BaseSolver)

    solution = solver.solve(engine.board_state.to_tuple())
    assert len(solution) > 0
    assert solver.nodes_expanded > 0
    assert solver.execution_time > 0

    for move_name in solution:
        engine.move_by_direction(move_name)
    assert engine.is_win() is True


def test_score_record_sorting():
    r1 = ScoreRecord(player_name="P1", step_count=40, elapsed_time=15.0)
    r2 = ScoreRecord(player_name="P2", step_count=30, elapsed_time=20.0)
    r3 = ScoreRecord(player_name="P3", step_count=30, elapsed_time=12.0)

    records = [r1, r2, r3]
    records.sort()
    assert records[0].player_name == "P3"
    assert records[1].player_name == "P2"
    assert records[2].player_name == "P1"


def test_storage_game(tmp_path):
    from src.storage.storage import save_game, load_game

    save_file = tmp_path / "test_save.dat"
    bs = BoardState()
    bs.step_count = 14
    bs.elapsed_time = 25.5
    # Di chuyển ô trống sang (2, 3)
    bs.grid[3][3], bs.grid[2][3] = bs.grid[2][3], bs.grid[3][3]
    bs.empty_pos = (2, 3)

    assert save_game(bs, save_file) is True
    loaded = load_game(save_file)
    assert loaded is not None
    assert loaded.step_count == 14
    assert loaded.elapsed_time == 25.5
    assert loaded.empty_pos == (2, 3)
    assert loaded.grid[2][3] == 0


def test_storage_leaderboard(tmp_path):
    from src.storage.storage import save_leaderboard, load_leaderboard, add_score_record

    lb_file = tmp_path / "test_leaderboard.csv"

    # Test với các tên người chơi đặc biệt (Player 1, Player Pro, tên có dấu phẩy)
    records = [
        ScoreRecord(player_name="Player Pro", step_count=20, elapsed_time=10.0),
        ScoreRecord(player_name="Player 1", step_count=30, elapsed_time=15.0),
        ScoreRecord(player_name="Nguyen, Van A", step_count=25, elapsed_time=12.0),
    ]

    assert save_leaderboard(records, lb_file) is True
    loaded = load_leaderboard(lb_file)

    # Đảm bảo không người chơi nào có tên bắt đầu bằng Player hoặc có dấu phẩy bị mất
    assert len(loaded) == 3
    names = [r.player_name for r in loaded]
    assert "Player Pro" in names
    assert "Player 1" in names
    assert "Nguyen, Van A" in names

    # Kiểm tra thứ tự sắp xếp: 20 bước -> 25 bước -> 30 bước
    assert loaded[0].player_name == "Player Pro"
    assert loaded[1].player_name == "Nguyen, Van A"
    assert loaded[2].player_name == "Player 1"

    # Test thêm kỷ lục mới bằng add_score_record
    new_rec = ScoreRecord(player_name="Player New", step_count=10, elapsed_time=5.0)
    top_after = add_score_record(new_rec, lb_file)
    assert len(top_after) == 4
    assert top_after[0].player_name == "Player New"
