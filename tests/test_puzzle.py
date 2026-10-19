"""
Unit tests for 15-Puzzle core modules and algorithms.
"""

from src.structures.hash_table import HashTable
from src.structures.heap import MinHeap
from src.models.board_state import BoardState
from src.models.record import ScoreRecord
from src.logic.validator import check_solvable, count_inversions, parse_and_validate_input
from src.logic.engine import GameEngine
from src.algorithms.solvability import GOAL_STATE, shuffle_board
from src.algorithms.ida_solver import IDASolver


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

    ht.remove("state1")
    assert ht.contains("state1") is False
    assert len(ht) == 1

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


def test_solvability():
    # Solved state should be solvable
    assert check_solvable(list(GOAL_STATE)) is True

    # Swapping 14 and 15 should make it unsolvable
    unsolvable = list(GOAL_STATE)
    unsolvable[13], unsolvable[14] = unsolvable[14], unsolvable[13]
    assert check_solvable(unsolvable) is False

    # Trường Vũ test cases
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


def test_ida_solver_short():
    engine = GameEngine()
    engine.reset_solved()
    # Perform 3 moves
    engine.move(2, 3)  # UP
    engine.move(2, 2)  # LEFT
    engine.move(3, 2)  # DOWN

    solver = IDASolver()
    solution = solver.solve(engine.board_state.to_tuple())
    assert len(solution) > 0

    # Apply solution moves to check if it reaches goal
    for move_name in solution:
        engine.move_by_direction(move_name)
    assert engine.is_win() is True


def test_score_record_sorting():
    r1 = ScoreRecord(player_name="P1", step_count=40, elapsed_time=15.0)
    r2 = ScoreRecord(player_name="P2", step_count=30, elapsed_time=20.0)
    r3 = ScoreRecord(player_name="P3", step_count=30, elapsed_time=12.0)

    records = [r1, r2, r3]
    records.sort()
    # P3 has 30 steps & 12s -> best
    # P2 has 30 steps & 20s -> second
    # P1 has 40 steps -> third
    assert records[0].player_name == "P3"
    assert records[1].player_name == "P2"
    assert records[2].player_name == "P1"
