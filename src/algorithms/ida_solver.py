from src.algorithms.base_solver import BaseSolver
from src.algorithms.solvability import GOAL_STATE,is_solvable
from src.structures.hash_table import HashTable
class IDASolver:
    DY=[-1,1,0,0]
    DX=[0,0,-1,1] 
    #0 len, 1 xuong, 2 trai, 3 phai
    MOVE_NAMES=["UP","DOWN","LEFT","RIGHT"]
    def __init__(self,weight=2):
        self._weight=2
        self._visited=HashTable() #cho khi nao co hash tu Danh
        # self._visited=dict()

    def _manhattan_distance(self,state:list) -> int:
        dist=0
        for i in range(16):
            val=state[i]
            if val==0:
                continue
            goal_row=(val-1)//4
            goal_col=(val-1)%4
            dist+=abs(i//4-goal_row)+abs(i%4-goal_col)
        return dist
    def _search(self,state:list,empty_pos,g,threshold,last_dir,path:list):
        h=self._manhattan_distance(state)
        f=g+self._weight*h
        if f>threshold:
            return f
        if h==0:
            return -1
        state_key=tuple(state)
        if self._visited.contains(state_key):
            return float("inf")
        # if state_key in self._visited and self._visited[state_key]<=g:
        #     return float("inf")
        min_threshold=float("inf")
        empty_row=empty_pos//4
        empty_col=empty_pos%4
        for d in range(4):
            if last_dir!=-1 and d==(last_dir^1):
                continue
            new_row=empty_row+self.DY[d]
            new_col=empty_col+self.DX[d]
            if 0<=new_row<4 and 0<=new_col<4:
                new_pos=new_row*4+new_col
                move_name=self.MOVE_NAMES[d]
                state[empty_pos],state[new_pos]=(state[new_pos],state[empty_pos])
                path.append(move_name)
                result=self._search(state,new_pos,g+1,threshold,d,path)
                if result==-1:
                    return -1
                if result<min_threshold:
                    min_threshold=result
                path.pop()
                state[empty_pos],state[new_pos]=(state[new_pos],state[empty_pos])
        return min_threshold
    def solve(self,initial_state):
        if isinstance(initial_state,list) and isinstance(initial_state[0],list):
            initial_state=tuple(tile for row in initial_state for tile in row)
        else:
            initial_state=tuple(initial_state)

        if not is_solvable(initial_state):
            print("Lỗi: Bàn cờ này vô nghiệm")
            return []
        state=list(initial_state)
        if self._manhattan_distance(state)==0:
            return []
        empty_pos=state.index(0)
        path=[]
        threshold=self._weight*self._manhattan_distance(state)
        while True:
            self._visited.clear()
            result=self._search(state,empty_pos,0,threshold,-1,path)
            if result==-1:
                return path
            if result==float("inf"):
                return []
            threshold=result
        ...