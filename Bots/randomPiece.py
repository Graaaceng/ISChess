from Bots.ChessBotList import register_chess_bot
from strategies.base_moves import rook_moves, bishop_moves, knight_moves
import random

def atRandom(player_sequence, board, time_budget, **kwargs):
    
    # find all pieces that can move = their move list is NOT empty (and store them in a list)
    # choose at random a piece in that list
    # choose at random a move in that piece's move list
    
    color = player_sequence[1]
    movable_pieces = []
    all_rooks_moves = {}
    all_bishops_moves = {}
    all_knights_moves = {}
    
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            
            # look for all the pieces
            if board[x,y] != '' and board[x,y][-1] == color:
                
                if board[x,y][0] == "r":
                    # calculate all its moves
                    moves = rook_moves(board, (x,y), color)
                    # save it in a dictionnary with its origine coordinates as a key
                    all_rooks_moves[(x,y)] = moves
                    # movable piece if the move list is not empty
                    if len(moves) > 0:
                        movable_pieces.append((x,y))
                        
                if board[x,y][0] == "b":
                    moves = bishop_moves(board, (x,y), color)
                    all_bishops_moves[(x,y)] = moves
                    if len(moves) > 0:
                        movable_pieces.append((x,y))
                        
                if board[x,y][0] == "n":
                    moves = knight_moves(board, (x,y), color)
                    all_knights_moves[(x,y)] = moves
                    if len(moves) > 0:
                        movable_pieces.append((x,y))
                        
    piece_to_move = random.choice(movable_pieces)
    
    match board[piece_to_move][0]:
        case "r":
            return piece_to_move ,random.choice(all_rooks_moves.get(piece_to_move))
        case "b":
            return piece_to_move, random.choice(all_bishops_moves.get(piece_to_move))
        case "n":
            return piece_to_move, random.choice(all_knights_moves.get(piece_to_move))
   
    return (0,0), (0,0)

register_chess_bot("atRandomV1", atRandom)