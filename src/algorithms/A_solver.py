from src.structures.heap import MinHeap
from src.structures.hash_table import HashTable

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GOAL_POS = {val: (i // 3, i % 3) for i, val in enumerate(GOAL_STATE)}

class PuzzleNode:
    def __init__(self, state, g=0, parent=None, move=""):
        self.state = state
        self.g = g
        self.parent = parent
        self.move = move
        self.h = self._calc_manhattan()
        self.f = self.g + self.h

    def _calc_manhattan(self):
        dist = 0
        for idx, val in enumerate(self.state):
            if val != 0:
                curr_r, curr_c = idx // 3, idx % 3
                goal_r, goal_c = GOAL_POS[val]
                dist += abs(curr_r - goal_r) + abs(curr_c - goal_c)
        return dist

    def get_neighbors(self):
        neighbors = []
        zero_idx = self.state.index(0)
        r, c = zero_idx // 3, zero_idx % 3
        directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for dr, dc, move_name in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                new_state = list(self.state)
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                neighbors.append((tuple(new_state), move_name))
        return neighbors

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

def solve_a_star(start_state):
    open_set = MinHeap()
    
    dict = HashTable(cap=100000) 
    
    start_node = PuzzleNode(start_state)
    open_set.push(start_node)
    dict.put(start_state, 0)

    while not open_set.is_empty():
        cur = open_set.pop()

        if cur.state == GOAL_STATE:
            path = []
            curr = cur
            while curr:
                path.append(curr)
                curr = curr.parent
            return path[::-1]

        cur_best_g = dict.get(cur.state)
        if cur_best_g is not None and cur.g > cur_best_g:
            continue

        for next_state, move_name in cur.get_neighbors():
            next_g = cur.g + 1
            
            neighbor_best_g = dict.get(next_state)
            
            if neighbor_best_g is None or next_g < neighbor_best_g:
                dict.put(next_state, next_g)
                
                neighbor_node = PuzzleNode(next_state, next_g, cur, move_name)
                open_set.push(neighbor_node)

    return None

