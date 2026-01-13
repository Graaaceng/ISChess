import random
import time
from Bots.ChessBotList import register_chess_bot

import numpy as np
from numpy.typing import NDArray

Board = NDArray[np.str_]


PIECE_VALUES = {
    "p": 10,
    "n": 40,
    "b": 40,
    "r": 40,
    "q": 100,
    "k": 10000,
}


def get_board_score(board: Board, player_color: str, depth: int = 0) -> int:
    score = 0
    has_my_king = False
    has_opponent_king = False
    opponent_color = "w" if player_color == "b" else "b"

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            piece = board[x, y]
            if piece != "":
                if piece == f"k{player_color}":
                    has_my_king = True
                elif piece == f"k{opponent_color}":
                    has_opponent_king = True

                if piece[0] != "k":
                    value = PIECE_VALUES.get(piece[0], 0)
                    if piece[-1] == player_color:
                        score += value
                    else:
                        score -= value

    if not has_my_king:
        return -999999 + depth

    if not has_opponent_king:
        return 999999 - depth

    return score


def new_board(board, prev_pos, new_pos):
    new_board = board.copy()
    piece = new_board[prev_pos]
    new_board[new_pos] = piece
    new_board[prev_pos] = ""

    # Promote pawn to queen
    if piece != "" and piece[0] == "p" and new_pos[0] == board.shape[0] - 1:
        color = piece[1]
        new_board[new_pos] = f"q{color}"

    return new_board


def rook_moves(board, pos: tuple[int, int], color) -> list[tuple[int, int, any]]:
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


def Observer(player_sequence, initial_board, time_budget, **kwargs):

    my_color = player_sequence[1]
    opponent_color = "w" if my_color == "b" else "b"

    start_time = time.time()
    time_limit = time_budget if time_budget else float("inf")

    MOVES_MAP = {
        "r": rook_moves,
        "b": bishop_moves,
        "n": knight_moves,
        "p": pawn_moves,
        "q": queen_moves,
        "k": king_moves,
    }

    def time_almost_up() -> bool:
        return (time.time() - start_time) > 0.90 * time_limit

    def find_king(board: Board, color: str):
        target = f"k{color}"
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x, y] == target:
                    return (x, y)
        return None  # roi capturé

    def isAttackable(board: Board, pos: tuple[int, int], by_color: str) -> bool:
        """
        Détection d'attaque fiable (sans dépendre des générateurs de coups),
        avec gestion correcte des pions.
        """
        x, y = pos
        n = board.shape[0]

        def in_bounds(a, b):
            return 0 <= a < n and 0 <= b < n

        # 1) Pions : attaque diagonale uniquement
        pawn_dir = -1 if by_color == "w" else 1
        for dy in (-1, 1):
            ax, ay = x + pawn_dir, y + dy
            if in_bounds(ax, ay) and board[ax, ay] == f"p{by_color}":
                return True

        # 2) Cavaliers
        knight_jumps = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dx, dy in knight_jumps:
            ax, ay = x + dx, y + dy
            if in_bounds(ax, ay) and board[ax, ay] == f"n{by_color}":
                return True

        # 3) Roi (adjacent)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ax, ay = x + dx, y + dy
                if in_bounds(ax, ay) and board[ax, ay] == f"k{by_color}":
                    return True

        # 4) Lignes/colonnes : tours + dames
        rook_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in rook_dirs:
            ax, ay = x + dx, y + dy
            while in_bounds(ax, ay):
                p = board[ax, ay]
                if p != "":
                    if p[-1] == by_color and p[0] in ("r", "q"):
                        return True
                    break
                ax, ay = ax + dx, ay + dy

        # 5) Diagonales : fous + dames
        bishop_dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in bishop_dirs:
            ax, ay = x + dx, y + dy
            while in_bounds(ax, ay):
                p = board[ax, ay]
                if p != "":
                    if p[-1] == by_color and p[0] in ("b", "q"):
                        return True
                    break
                ax, ay = ax + dx, ay + dy

        return False

    def get_all_moves(board: Board, color: str):
        all_moves = []
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                piece = board[x, y]
                if piece != "" and piece[-1] == color:
                    piece_type = piece[0]
                    fn = MOVES_MAP.get(piece_type)
                    if fn:
                        all_moves.extend(fn(board, (x, y), color))
        return all_moves

    def filter_legal_moves(moves, color: str, king_pos):
        opponent = "w" if color == "b" else "b"
        if king_pos is None:
            return []
        legal = []
        for move_from, move_to, new_board in moves:
            new_king_pos = move_to if move_from == king_pos else king_pos
            if not isAttackable(new_board, new_king_pos, opponent):
                legal.append((move_from, move_to, new_board))
        return legal

    def order_moves(moves, board: Board, color: str):
        n = board.shape[0]
        center = n // 2

        def score_move(move):
            from_pos, to_pos, _ = move
            score = 0
            target = board[to_pos]

            if target != "":  # capture
                target_value = PIECE_VALUES.get(target[0], 0)
                moving_piece = board[from_pos]
                moving_value = PIECE_VALUES.get(moving_piece[0], 0)
                score = 10000 + (target_value - moving_value) * 10 + target_value
            else:
                # centralité
                center_distance = abs(to_pos[0] - center) + abs(to_pos[1] - center)
                score += (n - center_distance) * 2

                # avancement des pions
                piece = board[from_pos]
                if piece != "" and piece[0] == "p":
                    if color == "w":
                        score += (n - to_pos[0]) * 5
                    else:
                        score += to_pos[0] * 5

            return score

        moves_scored = [(score_move(m), m) for m in moves]
        moves_scored.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in moves_scored]

    def minimax(
        board: Board,
        depth: int,
        max_depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
        king_pos_my,
        king_pos_opp,
    ) -> int:

        if time_almost_up():
            return get_board_score(board, my_color, depth)

        if depth >= max_depth:
            return get_board_score(board, my_color, depth)

        color = my_color if is_maximizing else opponent_color
        moves = get_all_moves(board, color)

        if color == my_color:
            moves = filter_legal_moves(moves, my_color, king_pos_my)
        else:
            moves = filter_legal_moves(moves, opponent_color, king_pos_opp)

        if not moves:
            return get_board_score(board, my_color, depth)

        moves = order_moves(moves, board, color)

        if is_maximizing:
            best = float("-inf")
            for move_from, move_to, next_board in moves:
                next_king_my = king_pos_my
                next_king_opp = king_pos_opp
                if king_pos_my == move_from:
                    next_king_my = move_to

                val = minimax(
                    next_board,
                    depth + 1,
                    max_depth,
                    False,
                    alpha,
                    beta,
                    next_king_my,
                    next_king_opp,
                )
                if val > best:
                    best = val
                if val > alpha:
                    alpha = val
                if beta <= alpha:
                    break
            return best
        else:
            best = float("inf")
            for move_from, move_to, next_board in moves:
                next_king_my = king_pos_my
                next_king_opp = king_pos_opp
                if king_pos_opp == move_from:
                    next_king_opp = move_to

                val = minimax(
                    next_board,
                    depth + 1,
                    max_depth,
                    True,
                    alpha,
                    beta,
                    next_king_my,
                    next_king_opp,
                )
                if val < best:
                    best = val
                if val < beta:
                    beta = val
                if beta <= alpha:
                    break
            return best

    def get_best_move(board: Board, max_depth: int):

        # positions initiales des rois
        king_my = find_king(board, my_color)
        king_opp = find_king(board, opponent_color)

        moves = get_all_moves(board, my_color)
        if not moves:
            return (0, 0), (0, 0)

        legal_moves = filter_legal_moves(moves, my_color, king_my)
        if not legal_moves:
            move_from, move_to, _ = moves[0]
            return move_from, move_to

        legal_moves = order_moves(legal_moves, board, my_color)

        best_score = float("-inf")
        best_moves = []
        alpha = float("-inf")

        for move_from, move_to, next_board in legal_moves:
            if time_almost_up():
                return random.choice(best_moves) if best_moves else (move_from, move_to)

            next_king_my = king_my
            next_king_opp = king_opp
            if king_my == move_from:
                next_king_my = move_to

            score = minimax(
                next_board,
                1,
                max_depth,
                False,
                alpha,
                float("inf"),
                next_king_my,
                next_king_opp,
            )

            if score > best_score:
                best_score = score
                best_moves = [(move_from, move_to)]
            elif score == best_score:
                best_moves.append((move_from, move_to))

            if score > alpha:
                alpha = score

        return (
            random.choice(best_moves)
            if best_moves
            else (legal_moves[0][0], legal_moves[0][1])
        )

    result = ((0, 0), (0, 0))
    max_depth_cap = 8
    for d in range(1, max_depth_cap + 1):
        if time_almost_up():
            break
        result = get_best_move(initial_board, d)

    return result


register_chess_bot("GRAAL", Observer)
