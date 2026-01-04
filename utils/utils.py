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

def have_more_pieces(board, color):
    num_piece_player = 0
    num_piece_enemy = 0
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x,y] != "" and board[x,y][-1] == color:
                num_piece_player += 1
            elif board[x,y] != "" and board[x,y][-1] == color:
                num_piece_enemy += 1

    if num_piece_enemy > num_piece_player: return False
    return True

def calculate_execution_time(start_time, end_time):
    return print(f"Execution time: {end_time - start_time:.2f}")