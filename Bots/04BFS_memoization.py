import random
import time
from functools import lru_cache
from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
from strategies.board_score import get_board_score
from utils.type import Board


def Observer(player_sequence, initial_board, time_budget, **kwargs):

    my_color = player_sequence[1]
    metrics = kwargs.get("metrics", None)

    start_time = time.time()
    time_limit = time_budget if time_budget else float("inf")

    nodes_explored = 0
    possible_moves = []

    # Cache pour mémoïzation
    board_score_cache = {}

    def board_to_key(board: Board) -> tuple:
        """Convertit un board en clé hashable pour la mémoïzation"""
        return tuple(tuple(row) for row in board)

    def get_cached_score(board: Board, color: str) -> int:
        """Version mémoïzée de get_board_score"""
        key = (board_to_key(board), color)
        if key not in board_score_cache:
            board_score_cache[key] = get_board_score(board, color)
        return board_score_cache[key]

    def getMovesAndScore(
        board: Board, pos: tuple[int, int], color: str, score: int
    ) -> list[tuple[tuple[int, int], tuple[int, int], Board, int]]:
        moves_map = {
            "r": rook_moves,
            "b": bishop_moves,
            "n": knight_moves,
            "p": pawn_moves,
            "q": queen_moves,
            "k": king_moves,
        }
        piece_type = board[pos[0], pos[1]][0]
        function = moves_map.get(piece_type)

        moves = function(board, pos, color)
        return [
            (move_from, move_to, board, score + get_cached_score(board, my_color))
            for move_from, move_to, board in moves
        ]

    def getNextBoards(
        boards: list[Board], color: str, score: int = None
    ) -> list[tuple[tuple[int, int], tuple[int, int], Board, int]]:
        all_boards = []
        current_score = 0 if score is None else score

        for board in boards:
            for x in range(board.shape[0]):
                for y in range(board.shape[1]):
                    if board[x, y] != "" and board[x, y][-1] == color:
                        all_boards.extend(
                            getMovesAndScore(
                                board,
                                (x, y),
                                color,
                                current_score,
                            )
                        )
        return all_boards

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

    def getBestBoards(
        boards: list[tuple[Board, int, list[tuple[tuple[int, int], tuple[int, int]]]]],
    ):
        # grouper les boards par leur 1er move
        moves_scores = {}  # (from, to): [scores finaux]

        for board, score, move_path in boards:
            if len(move_path) > 0:
                first_move = move_path[0]
                if first_move not in moves_scores:
                    moves_scores[first_move] = []
                moves_scores[first_move].append(score)

        moves_worst_score = {move: min(scores) for move, scores in moves_scores.items()}
        # print(f"Moves worst scores: {moves_worst_score}")

        best_worst_score = max(moves_worst_score.values())
        # print(f"Best worst score: {best_worst_score}")
        best_first_moves = [
            move
            for move, worst_score in moves_worst_score.items()
            if worst_score == best_worst_score
        ]

        return best_first_moves

    def bfs(
        boards: list[tuple[Board, int, list[tuple[tuple[int, int], tuple[int, int]]]]],
        depth: int,
        max_depth: int,
        color: str,
    ):
        nonlocal nodes_explored

        elapsed_time = time.time() - start_time
        if elapsed_time > 0.90 * time_limit:
            return boards

        if depth >= max_depth:
            return boards

        next_boards = []
        terminal_boards = []

        for board, score, move_path in boards:
            elapsed_time = time.time() - start_time
            if elapsed_time > 0.90 * time_limit:
                break

            # get all possible next boards
            for next_from, next_to, next_board, next_score in getNextBoards(
                [board], color, score
            ):
                nodes_explored += 1
                new_path = move_path + [(next_from, next_to)]

                if not has_both_kings(next_board):
                    terminal_boards.append((next_board, next_score, new_path))
                else:
                    next_boards.append((next_board, next_score, new_path))

        if len(next_boards) == 0:
            return boards + terminal_boards

        next_color = "w" if color == "b" else "b"
        explored_boards = bfs(next_boards, depth + 1, max_depth, next_color)
        return explored_boards + terminal_boards

    initial_moves = getNextBoards([initial_board], my_color, 0)
    total_initial_moves = len(initial_moves)

    initial_boards = [(initial_board, 0, [])]
    evaluated_boards = bfs(initial_boards, 0, 3, my_color)

    if len(evaluated_boards) == 0 or len(evaluated_boards[0][2]) == 0:
        return (0, 0), (0, 0)
    # print(f"calculated boards: {len(evaluated_boards)}")

    best_first_moves = getBestBoards(evaluated_boards)

    possible_moves.append(total_initial_moves)

    return_pos_x, return_pos_y = random.choice(best_first_moves)

    if metrics:
        metrics.add_nodes_explored(nodes_explored)
        if possible_moves:
            metrics.add_possible_moves(possible_moves[-1])

    return return_pos_x, return_pos_y


register_chess_bot("04BFS_memoization", Observer)
