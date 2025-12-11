#   Be careful with modules to import from the root (don't forget the Bots.)
import copy
from Bots.ChessBotList import register_chess_bot
from ChessRules import move_is_valid


#   Simply move the pawns forward and tries to capture as soon as possible
def chess_bot(player_sequence, board, time_budget, **kwargs):
    temp_boards = []
    temp_boards2 = []

    color = player_sequence[1]
    # parcourir toutes les cases du plateau
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):

            # si c'est une piece de la bonne couleur (pb, pw pour pion blanc ou noir) faire action
            if board[y, x] != "" and board[y, x][-1] == color:
                for b in range(board.shape[0]):
                    for a in range(board.shape[1]):
                        if move_is_valid(player_sequence, ([y, x], [b, a]), board):
                            temp_board = board.copy()
                            # Déplacer la pièce : copier vers nouvelle position, vider ancienne
                            temp_board[b, a] = temp_board[y, x]
                            temp_board[y, x] = ""
                            temp_boards.append(temp_board)

    # for potential_board in temp_boards:
    #     for y in range(board.shape[0]):
    #         for x in range(board.shape[1]):
    #             if potential_board[y, x] != "" and potential_board[y, x][-1] == color:
    #                 for b in range(board.shape[0]):
    #                     for a in range(board.shape[1]):
    #                         if move_is_valid(
    #                             player_sequence, ([y, x], [b, a]), potential_board
    #                         ):
    #                             temp_board = potential_board.copy()
    #                             temp_board[b, a] = temp_board[y, x]
    #                             temp_board[y, x] = ""
    #                             temp_boards2.append(temp_board)

    for temp_board in temp_boards:
        for y in range(temp_board.shape[0]):
            for x in range(temp_board.shape[1]):
                # Utiliser .string() pour obtenir le nom de la pièce au lieu de l'objet
                piece = temp_board[y, x]
                if piece != "":
                    print(piece.string(), end=" ")
                else:
                    print("  ", end=" ")
            print()
        print("---")
    print(board)
    # print(temp_boards[0])

    return (0, 0), (0, 0)


#   Example how to register the function
register_chess_bot("killtheking", chess_bot)
