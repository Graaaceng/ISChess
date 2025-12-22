# return all positions possible of the rook (r)

from utils.utils import new_board


def rook_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]

    # for each directions:
    # if adjacent square is not free and same color -> stop the loop
    # if adjacent square is not free and different color -> add position and stop the loop
    # else add the position and continue loop

    def add_moves_and_stop(new_pos: tuple[int, int]) -> bool:
        if board[new_pos] != "" and board[new_pos][-1] == color:
            return True
        elif board[new_pos] != "" and board[new_pos][-1] != color:
            all_moves.append((pos, new_pos, new_board(board, pos, new_pos)))
            return True
        else:
            all_moves.append((pos, new_pos, new_board(board, pos, new_pos)))
            return False

    # up
    for i in range(pos_x, board.shape[0] - 1):
        if add_moves_and_stop((i + 1, pos_y)):
            break

    # down
    for i in range(pos_x, 0, -1):
        if add_moves_and_stop((i - 1, pos_y)):
            break

    # right
    for i in range(pos_y, board.shape[1] - 1):
        if add_moves_and_stop((pos_x, i + 1)):
            break

    # left
    for i in range(pos_y, 0, -1):
        if add_moves_and_stop((pos_x, i - 1)):
            break

    return all_moves


# return all positions possible of the bishop (b)
def bishop_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]

    def add_moves_and_stop(new_pos: tuple[int, int]) -> bool:
        if board[new_pos] != "" and board[new_pos][-1] == color:
            return True
        elif board[new_pos] != "" and board[new_pos][-1] != color:
            all_moves.append((pos, new_pos, new_board(board, pos, new_pos)))
            return True
        else:
            all_moves.append((pos, new_pos, new_board(board, pos, new_pos)))
            return False

    # north east
    for i, j in zip(range(pos_x, board.shape[0] - 1), range(pos_y, board.shape[1] - 1)):
        if add_moves_and_stop((i + 1, j + 1)):
            break

    # north west
    for i, j in zip(range(pos_x, board.shape[0] - 1), range(pos_y, 0, -1)):
        if add_moves_and_stop((i + 1, j - 1)):
            break

    # south est
    for i, j in zip(range(pos_x, 0, -1), range(pos_y, board.shape[1] - 1)):
        if add_moves_and_stop((i - 1, j + 1)):
            break

    # south west
    for i, j in zip(range(pos_x, 0, -1), range(pos_y, 0, -1)):
        if add_moves_and_stop((i - 1, j - 1)):
            break

    return all_moves


# return all positions possible of the knight (n)
def knight_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]
    # all possible steps for a knight
    deltas = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, +2)]

    for x, y in deltas:
        xCandidate = pos_x + x
        yCandidate = pos_y + y
        if 0 <= xCandidate < board.shape[0] and 0 <= yCandidate < board.shape[1]:
            if (
                board[xCandidate, yCandidate] != ""
                and board[xCandidate, yCandidate][-1] != color
            ):
                all_moves.append(
                    (
                        pos,
                        (xCandidate, yCandidate),
                        new_board(board, pos, (xCandidate, yCandidate)),
                    )
                )
            elif board[xCandidate, yCandidate] == "":
                all_moves.append(
                    (
                        pos,
                        (xCandidate, yCandidate),
                        new_board(board, pos, (xCandidate, yCandidate)),
                    )
                )

    return all_moves


# return all positions possible of the queen
def queen_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    m1 = rook_moves(board, pos, color)
    m2 = bishop_moves(board, pos, color)
    all_moves.extend(m1)
    all_moves.extend(m2)
    return all_moves


# return all positions possibles of the king
def king_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]
    # all possible steps for a king (works the same as the knight)
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    for x, y in deltas:
        xCandidate = pos_x + x
        yCandidate = pos_y + y
        if 0 <= xCandidate < board.shape[0] and 0 <= yCandidate < board.shape[1]:
            if (
                board[xCandidate, yCandidate] != ""
                and board[xCandidate, yCandidate][-1] != color
            ):
                all_moves.append(
                    (
                        pos,
                        (xCandidate, yCandidate),
                        new_board(board, pos, (xCandidate, yCandidate)),
                    )
                )
            elif board[xCandidate, yCandidate] == "":
                all_moves.append(
                    (
                        pos,
                        (xCandidate, yCandidate),
                        new_board(board, pos, (xCandidate, yCandidate)),
                    )
                )

    return all_moves


# return all position possibles of the pawn
def pawn_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
    all_moves = []
    pos_x = pos[0]
    pos_y = pos[1]

    if pos_x + 1 >= board.shape[0]:
        return all_moves

    if (
        pos_y > 0
        and board[pos_x + 1, pos_y - 1] != ""
        and board[pos_x + 1, pos_y - 1][-1] != color
    ):
        all_moves.append(
            (pos, (pos_x + 1, pos_y - 1), new_board(board, pos, (pos_x + 1, pos_y - 1)))
        )
    if (
        pos_y < board.shape[1] - 1
        and board[pos_x + 1, pos_y + 1] != ""
        and board[pos_x + 1, pos_y + 1][1] != color
    ):
        all_moves.append(
            (pos, (pos_x + 1, pos_y + 1), new_board(board, pos, (pos_x + 1, pos_y + 1)))
        )
    if board[pos_x + 1, pos_y] == "":
        all_moves.append(
            (pos, (pos_x + 1, pos_y), new_board(board, pos, (pos_x + 1, pos_y)))
        )

    return all_moves
