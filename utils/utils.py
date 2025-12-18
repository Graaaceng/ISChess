def new_board(board, prev_pos, new_pos):
    new_board = board.copy()
    new_board[new_pos] = new_board[prev_pos]
    new_board[prev_pos] = ""
    return new_board


def print_board(board):
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            piece = board[y, x]
            if piece != "":
                print(piece.string(), end=" ")
            else:
                print("  ", end=" ")
        print()
    w
