from Main_move_generator import *
import Main_move_generator
import copy
import cProfile
import pstats
board=Board()
Main_move_generator.board=board
load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
generate_moves()
create_FEN(func_board=board)
#see how many moves there are per depth
move_list=[]
def get_moves_per_depth(depth,board=board,return_moves=False):
    moves=0
    if depth==0:
        if return_moves:
            move_list.append(create_FEN(func_board=board))
        return 1
    else:

        generate_moves(func_board=board)
        current_board=create_FEN(func_board=board)
        for move in board.move_list:
            temp_board=Board()
            load_FEN(current_board,func_board=temp_board)
            move_piece(move[0],move[1],temp_board)
            moves+=get_moves_per_depth(depth-1,temp_board,return_moves)

        return moves
# get_moves_per_depth(2)
cProfile.run('get_moves_per_depth(3)', 'restats')
p = pstats.Stats('restats')
p.print_stats()
p.sort_stats('cumulative').print_stats(10)
# print(get_moves_per_depth(2,return_moves=True))

# #compare our moves to a to Premade_moves.txt
# premade_moves=open("Premade_moves.txt","r")
# premade_moves=premade_moves.read()
# premade_moves=premade_moves.split("\n")
# premade_moves=[move.split(" ")[0] for move in premade_moves]

# move_list=[move.split(" ")[0] for move in move_list]

# too_many_moves=[x for x in move_list if x not in premade_moves]
# too_few_moves=[x for x in premade_moves if x not in move_list]