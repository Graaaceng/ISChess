# return all positions possible of the rook (r)
def rook_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]

    # for each directions:
    # if adjacent square is not free and same color -> stop the loop
    # if adjacent square is not free and different color -> add position and stop the loop
    # else add the position and continue loop
    
    #up
    for i in range(pos_x, board.shape[0]-1):
        if board[i+1 , pos_y] != '' and board[i+1, pos_y][-1] == color:
            break
        elif board[i+1 , pos_y] != '' and board[i+1, pos_y][-1] != color:
            all_moves.append((i+1, pos_y))
            break
        else:
            all_moves.append((i+1, pos_y))
        
    #down
    for i in range(pos_x, 0, -1):    
        if board[i-1 , pos_y] != '' and board[i-1, pos_y][-1] == color:
            break
        elif board[i-1 , pos_y] != '' and board[i-1, pos_y][-1] != color:
            all_moves.append((i-1, pos_y))
            break
        else:
            all_moves.append((i-1, pos_y))
        
    #right
    for i in range(pos_y, board.shape[1]-1):
        if board[pos_x , i+1] != '' and board[pos_x, i+1][-1] == color:
            break
        elif board[pos_x , i+1] != '' and board[pos_x, i+1][-1] != color:
            all_moves.append((pos_x, i+1))
            break
        else:
            all_moves.append((pos_x, i+1))
            
    #left
    for i in range(pos_y, 0, -1):
        if board[pos_x , i-1] != '' and board[pos_x, i-1][-1] == color:
            break
        elif board[pos_x , i-1] != '' and board[pos_x, i-1][-1] != color:
            all_moves.append((pos_x, i-1))
            break
        else:
            all_moves.append((pos_x, i-1))
    
    return all_moves

# return all positions possible of the bishop (b)
def bishop_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]
    
    # same as the rook but diagonally
    
    # north east
    for i, j in zip(range(pos_x, board.shape[0]-1), range(pos_y, board.shape[1]-1)):
        if board[i+1 , j+1] != '' and board[i+1, j+1][-1] == color:
            break
        elif board[i+1 , j+1] != '' and board[i+1, j+1][-1] != color:
            all_moves.append((i+1, j+1))
            break
        else:
            all_moves.append((i+1, j+1))
            
    # north west
    for i, j in zip(range(pos_x, board.shape[0]-1), range(pos_y, 0, -1)):
        if board[i+1 , j-1] != '' and board[i+1, j-1][-1] == color:
            break
        elif board[i+1 , j-1] != '' and board[i+1, j-1][-1] != color:
            all_moves.append((i+1, j-1))
            break
        else:
            all_moves.append((i+1, j-1))
            
    # south est
    for i, j in zip(range(pos_x, 0, -1 ), range(pos_y, board.shape[1]-1)):
        if board[i-1 , j+1] != '' and board[i-1, j+1][-1] == color:
            break
        elif board[i-1 , j+1] != '' and board[i-1, j+1][-1] != color:
            all_moves.append((i-1, j+1))
            break
        else:
            all_moves.append((i-1, j+1))
            
    # south west
    for i, j in zip(range(pos_x, 0, -1), range(pos_y, 0, -1)):
        if board[i-1 , j-1] != '' and board[i-1, j-1][-1] == color:
            break
        elif board[i-1 , j-1] != '' and board[i-1, j-1][-1] != color:
            all_moves.append((i-1, j-1))
            break
        else:
            all_moves.append((i-1, j-1))
    
    return all_moves

# return all positions possible of the knight (n)
def knight_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]
    # all possible steps for a knight
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, +2)]
    
    for x, y in deltas:
        xCandidate = pos_x + x
        yCandidate = pos_y + y
        if 0 <= xCandidate < board.shape[0] and 0 <= yCandidate < board.shape[1]:
            if board[xCandidate, yCandidate] != '' and board[xCandidate, yCandidate][-1] != color:
                all_moves.append((xCandidate, yCandidate))
            elif board[xCandidate, yCandidate] == '':
                all_moves.append((xCandidate, yCandidate))
        
    return all_moves