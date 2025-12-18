from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
import random

from strategies.board_score import get_board_score


def naiveObserver(player_sequence, initial_board, time_budget, **kwargs):

    # find all pieces that can move = their move list is NOT empty (and store them in a list)
    # choose at random a piece in that list
    # choose at random a move in that piece's move list

    my_color = player_sequence[1]

    def getNextBoards(
        boards, color, score=None
    ) -> list[tuple[tuple[int, int], tuple[int, int], any, int]]:
        all_boards = []
        current_score = 0 if score is None else score

        for board in boards:
            for x in range(board.shape[0]):
                for y in range(board.shape[1]):
                    # look for all the pieces
                    if board[x, y] != "" and board[x, y][-1] == color:
                        match board[x, y][0]:
                            case "r":
                                all_boards.extend(
                                    rook_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case "b":
                                all_boards.extend(
                                    bishop_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case "n":
                                all_boards.extend(
                                    knight_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case "p":
                                all_boards.extend(
                                    pawn_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case "q":
                                all_boards.extend(
                                    queen_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case "k":
                                all_boards.extend(
                                    king_moves(
                                        board,
                                        (x, y),
                                        color,
                                    ),
                                    # current_score + get_board_score(board, color),
                                )
                            case _:
                                pass

        return all_boards

    def getBestBoards(boards, color):
        best_score = float("-inf")
        best_moves = list()
        for move_from, move_to, board in boards:
            score = get_board_score(board, color)
            if score > best_score:
                best_score = score
                best_moves = [(move_from, move_to, board)]
            elif score == best_score:
                best_moves.append((move_from, move_to, board))

        return best_moves

    possible_boards = getNextBoards(list([initial_board]), my_color, 0)

    if len(possible_boards) == 0:
        return (0, 0), (0, 0)

    enemy_boards = getNextBoards(
        [board for _, _, board in possible_boards],
        "w" if my_color == "b" else "b",
    )

    best_boards = getBestBoards(possible_boards, my_color)

    (return_pos_x, return_pos_y, board) = random.choice(best_boards)

    return return_pos_x, return_pos_y


register_chess_bot("NaiveObserver", naiveObserver)
