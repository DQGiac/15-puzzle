import random

GOAL_STATE=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
def count_inversions(state): #Ham dem nghich the
    inversions=0
    tiles=[x for x in state if x!=0]
    n=len(tiles)
    for i in range(n):
        for j in range(i+1,n):
            if tiles[i]>tiles[j]:
                inversions+=1
    return inversions

def is_solvable(state): #Ham kiem tra tinh giai duoc hay khong dua vao ct
    inversions=count_inversions(state)
    tmp=state.index(0)
    black_row_top=tmp//4
    black_row_bot=4-black_row_top
    return (inversions+black_row_bot)%2==1
def shuffle_board(steps: int=50): #Xao ngau nhien de tao input cho bai toan 
    board=list(GOAL_STATE)
    blank_pos=15
    last_dir=-1
    moves=[(-1,0,-4),(1,0,4),(0,-1,-1),(0,1,1)]
    for _ in range(steps):
        valid_moves=[]
        r,c=blank_pos//4,blank_pos%4
        for d,(dr,dc,diff) in enumerate(moves):
            if last_dir!=-1 and d==(last_dir ^ 1):
                continue
            nr,nc=r+dr,c+dc
            if 0<=nr<4 and 0<=nc<4:
                valid_moves.append((d,diff))
        if not valid_moves:
            continue
        chosen_d,diff=random.choice(valid_moves)
        new_blank=blank_pos+diff
        board[blank_pos],board[new_blank]=board[new_blank],board[blank_pos]
        blank_pos=new_blank
        last_dir=chosen_d
    return tuple(board)
