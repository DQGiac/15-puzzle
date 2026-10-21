from src.algorithms.solvability import shuffle_board, is_solvable
from src.algorithms.ida_solver import IDASolver


def test_algo_solvability():
    assert is_solvable((0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)) is True
    assert is_solvable((15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)) is False


def test_ida_solver_execution():
    # Bàn cờ cách đích 3 bước (level Easy)
    board = (1, 2, 3, 4, 5, 6, 0, 7, 9, 10, 11, 8, 13, 14, 15, 12)
    solver = IDASolver()
    moves = solver.solve(board)
    assert len(moves) == 3
    assert solver.nodes_expanded > 0
    assert solver.execution_time > 0
