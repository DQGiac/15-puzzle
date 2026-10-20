from src.algorithms.solvability import shuffle_board, is_solvable
from src.algorithms.ida_solver import IDASolver


def test_algo_solvability():
    assert is_solvable((0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)) is True
    assert is_solvable((15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)) is False


if __name__ == "__main__":
    board = shuffle_board(50)
    board2 = (0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
    print(board)  # test
    solver = IDASolver()
    print(is_solvable((0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)))  # True
    print(is_solvable((15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)))  # False
    ans1 = solver.solve(board)
    print(ans1, len(ans1))
