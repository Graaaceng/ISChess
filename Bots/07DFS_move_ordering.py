import random
import time
from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
from strategies.board_score import get_board_score
from utils.type import Board


def Observer(player_sequence, initial_board, time_budget, **kwargs):

    my_color = player_sequence[1]
    opponent_color = "w" if my_color == "b" else "b"
    metrics = kwargs.get("metrics", None)

    PIECE_VALUES = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}

    start_time = time.time()
    time_limit = time_budget if time_budget else float("inf")

    nodes_explored = 0
    possible_moves = []

    def get_all_moves(
        board: Board, color: str
    ) -> list[tuple[tuple[int, int], tuple[int, int], Board]]:
        moves_map = {
            "r": rook_moves,
            "b": bishop_moves,
            "n": knight_moves,
            "p": pawn_moves,
            "q": queen_moves,
            "k": king_moves,
        }

        all_moves = []
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x, y] != "" and board[x, y][-1] == color:
                    piece_type = board[x, y][0]
                    function = moves_map.get(piece_type)
                    if function:
                        moves = function(board, (x, y), color)
                        all_moves.extend(moves)

        return all_moves

    def order_moves(
        moves: list[tuple[tuple[int, int], tuple[int, int], Board]],
        board: Board,
        color: str,
    ) -> list[tuple[tuple[int, int], tuple[int, int], Board]]:

        def score_move(move):
            from_pos, to_pos, new_board = move
            score = 0

            target = board[to_pos]
            if target != "":
                target_value = PIECE_VALUES.get(target[0], 0)
                moving_piece = board[from_pos]
                moving_value = PIECE_VALUES.get(moving_piece[0], 0)
                score += target_value * 10 - moving_value

            center_distance = abs(to_pos[0] - board.shape[0] // 2) + abs(
                to_pos[1] - board.shape[1] // 2
            )
            score += (board.shape[0] - center_distance) * 0.5

            piece = board[from_pos]
            if piece[0] == "p":
                if color == "w":
                    score += (board.shape[0] - to_pos[0]) * 0.3
                else:
                    score += to_pos[0] * 0.3

            return score

        scored_moves = [(score_move(move), move) for move in moves]
        scored_moves.sort(reverse=True, key=lambda x: x[0])

        return [move for _, move in scored_moves]

    def has_both_kings(board: Board) -> bool:
        has_white_king = False
        has_black_king = False

        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                if board[x, y] == "kw":
                    has_white_king = True
                elif board[x, y] == "kb":
                    has_black_king = True

                if has_white_king and has_black_king:
                    return True

        return has_white_king and has_black_king

    def minimax(
        board: Board,
        depth: int,
        max_depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float,
    ) -> int:
        nonlocal nodes_explored
        nodes_explored += 1

        elapsed_time = time.time() - start_time
        if elapsed_time > 0.90 * time_limit:
            return get_board_score(board, my_color)

        if depth >= max_depth or not has_both_kings(board):
            return get_board_score(board, my_color)

        color = my_color if is_maximizing else opponent_color
        moves = get_all_moves(board, color)

        if not moves:
            return get_board_score(board, my_color)

        moves = order_moves(moves, board, color)

        if is_maximizing:
            max_eval = float("-inf")
            for move_from, move_to, next_board in moves:
                eval_score = minimax(
                    next_board, depth + 1, max_depth, False, alpha, beta
                )
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # beta break
            return max_eval
        else:
            min_eval = float("inf")
            for move_from, move_to, next_board in moves:
                eval_score = minimax(
                    next_board, depth + 1, max_depth, True, alpha, beta
                )
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha break
            return min_eval

    def get_best_move(
        board: Board, max_depth: int
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        nonlocal nodes_explored, possible_moves
        nodes_explored = 0

        moves = get_all_moves(board, my_color)

        if not moves:
            return (0, 0), (0, 0)

        moves = order_moves(moves, board, my_color)

        possible_moves.append(len(moves))

        best_score = float("-inf")
        best_moves = []
        alpha = float("-inf")

        for move_from, move_to, next_board in moves:
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.90 * time_limit:
                if not best_moves:
                    return move_from, move_to
                return random.choice(best_moves)

            score = minimax(next_board, 1, max_depth, False, alpha, float("inf"))

            if score > best_score:
                best_score = score
                best_moves = [(move_from, move_to)]
            elif score == best_score:
                best_moves.append((move_from, move_to))

            alpha = max(alpha, score)

        if not best_moves:
            move_from, move_to, _ = random.choice(moves)
            return move_from, move_to

        return random.choice(best_moves)

    result = get_best_move(initial_board, 4)

    if metrics:
        metrics.add_nodes_explored(nodes_explored)
        if possible_moves:
            metrics.add_possible_moves(possible_moves[-1])

    return result


register_chess_bot("07DFS_move_ordering", Observer)
