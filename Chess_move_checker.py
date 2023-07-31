from Main_move_generator import *
global board
board=Board()
load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

#see how many moves there are per depth

def get_moves_per_depth(depth):
    moves=0
    if depth==0:
        return 1
    else:
        generate_moves()
        for move in board.move_list:
            make_move(move)
            moves+=get_moves_per_depth(depth-1)
            undo_move()
        return moves