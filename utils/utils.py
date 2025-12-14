def new_board(board, prev_pos, new_pos):
    new_board = board.copy()
    new_board[new_pos] = new_board[prev_pos]
    new_board[prev_pos] = ""
    return new_board
