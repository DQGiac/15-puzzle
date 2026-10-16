from src.algorithms.solvability import shuffle_board,is_solvable
from src.algorithms.ida_solver import IDASolver


board=shuffle_board(50)
print(board) #test
solver=IDASolver()
print(is_solvable((0,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1))) #True
print(is_solvable((15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0))) #False
print(solver.solve(board))