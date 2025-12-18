def get_board_score(board, player_color):
    score = 0
    piece_values = {
        "p": 11,
        "r": 22,
        "n": 22,
        "b": 22,
        "q": 23,
        "k": 0,
    }
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            piece = board[x, y]
            if piece != "":
                value = piece_values.get(piece[0], 0)
                if piece[-1] == player_color:
                    score += value
                else:
                    score -= value

    return score
