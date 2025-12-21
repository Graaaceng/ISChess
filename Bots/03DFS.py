import random
from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import *
from strategies.board_score import get_board_score
from utils.type import Board


def Observer(player_sequence, initial_board, time_budget, **kwargs):

    my_color = player_sequence[1]

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
            (move_from, move_to, board, score + get_board_score(board, color))
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

    def getBestBoards(
        boards: list[tuple[Board, int, list[tuple[tuple[int, int], tuple[int, int]]]]],
    ):
        best_score = float("-inf")
        best_first_moves = []
        for board, score, move_path in boards:
            if score > best_score:
                best_score = score
                best_first_moves = [move_path[0]]
            elif score == best_score:
                if move_path[0] not in best_first_moves:
                    best_first_moves.append(move_path[0])
        return best_first_moves

    def dfs(
        boards: list[tuple[Board, int, list[tuple[tuple[int, int], tuple[int, int]]]]],
        depth: int,
        max_depth: int,
        color: str,
    ):
        if depth >= max_depth:
            return boards

        next_boards = []
        for board, score, move_path in boards:
            # get all possible next boards
            for next_from, next_to, next_board, next_score in getNextBoards(
                [board], color, score
            ):
                # add move to the path
                new_path = move_path + [(next_from, next_to)]
                next_boards.append((next_board, next_score, new_path))

        if len(next_boards) == 0:
            return boards

        # change color for next step
        next_color = "w" if color == "b" else "b"
        return dfs(next_boards, depth + 1, max_depth, next_color)

    initial_boards = [(initial_board, 0, [])]
    evaluated_boards = dfs(initial_boards, 0, 2, my_color)

    if len(evaluated_boards) == 0 or len(evaluated_boards[0][2]) == 0:
        return (0, 0), (0, 0)
    print(f"calculated boards: {len(evaluated_boards)}")

    best_first_moves = getBestBoards(evaluated_boards)

    return_pos_x, return_pos_y = random.choice(best_first_moves)

    return return_pos_x, return_pos_y


register_chess_bot("01DFS", Observer)
