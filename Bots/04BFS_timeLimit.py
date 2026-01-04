import random
import time
from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
from strategies.board_score import get_board_score
from utils.type import Board
from utils.utils import *


def observer_with_limit(player_sequence, initial_board, time_budget, **kwargs):
    start_time = time.time()
    my_color = player_sequence[1]
    
    def remaining_time():
        return time_budget - (time.time() - start_time)

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
            (move_from, move_to, board, score + get_board_score(board, my_color))
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

        best_worst_score = max(moves_worst_score.values())
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
        if remaining_time() < 0.03: #margin of safety
            return boards
        
        if depth >= max_depth:
            return boards

        next_boards = []
        terminal_boards = []

        for board, score, move_path in boards:
            
            if remaining_time() < 0.03: #margin of safety
                return boards + terminal_boards
            
            # get all possible next boards
            for next_from, next_to, next_board, next_score in getNextBoards(
                [board], color, score
            ):
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
    
    initial_boards = [(initial_board, 0, [])]
    best_results = []
    max_depth = 1
    
    while remaining_time() > 0.05:  # keep some time to decide
        try:
            evaluated_boards = bfs(initial_boards, 0, max_depth, my_color)
            
            if len(evaluated_boards) > 0 and len(evaluated_boards[0][2]) > 0:
                best_results = evaluated_boards
            
            if remaining_time() > 0.1:
                max_depth += 1
            else:
                break
        except Exception as e:
            print(f"Error in BFS: {e}")
            break
        
    if len(best_results) == 0 or len(best_results[0][2]) == 0:
        return (0,0), (0,0)
           
    print(f"calculated boards: {len(evaluated_boards)}")
    print(f"search depth: {max_depth}, time used: {time.time() - start_time:.2f}s")

    best_first_moves = getBestBoards(evaluated_boards)

    return_pos_x, return_pos_y = random.choice(best_first_moves)    
    
    end_time = time.time()
    calculate_execution_time(start_time, end_time)
    
    return return_pos_x, return_pos_y


register_chess_bot("BFS_limit", observer_with_limit)
