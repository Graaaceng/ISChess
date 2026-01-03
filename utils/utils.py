def new_board(board, prev_pos, new_pos):
    new_board = board.copy()
    piece = new_board[prev_pos]
    new_board[new_pos] = piece
    new_board[prev_pos] = ""

    # Promote pawn to queen if it reaches the last rank
    if piece != "" and piece[0] == "p" and new_pos[0] == board.shape[0] - 1:
        color = piece[1]
        new_board[new_pos] = f"q{color}"

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
