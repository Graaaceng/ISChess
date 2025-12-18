from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
import random

from strategies.board_score import get_board_score


def naiveRandom(player_sequence, board, time_budget, **kwargs):

    # find all pieces that can move = their move list is NOT empty (and store them in a list)
    # choose at random a piece in that list
    # choose at random a move in that piece's move list

    color = player_sequence[1]

    all_moves = []
    best_moves = []
    best_score = -9999

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):

            # look for all the pieces
            if board[x, y] != "" and board[x, y][-1] == color:
                match board[x, y][0]:
                    case "r":
                        all_moves.extend(rook_moves(board, (x, y), color))
                    case "b":
                        all_moves.extend(bishop_moves(board, (x, y), color))
                    case "n":
                        all_moves.extend(knight_moves(board, (x, y), color))
                    case "p":
                        all_moves.extend(pawn_moves(board, (x, y), color))
                    case "q":
                        all_moves.extend(queen_moves(board, (x, y), color))
                    case "k":
                        all_moves.extend(king_moves(board, (x, y), color))
                    case _:
                        pass

    if len(all_moves) == 0:
        return (0, 0), (0, 0)

    for move_from, move_to, board in all_moves:
        score = get_board_score(board, color)
        if score > best_score:
            best_score = score
            best_moves = [(move_from, move_to)]
        elif score == best_score:
            best_moves.append((move_from, move_to))

    (return_pos_x, return_pos_y) = random.choice(best_moves)
    return return_pos_x, return_pos_y


register_chess_bot("RandomBlind", naiveRandom)
