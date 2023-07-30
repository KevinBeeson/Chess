import pygame
import numpy as np
import copy 

pygame.init()


square_size=50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM= (244,241,224)
PINK = (255, 192, 203)
PINK_TRANSPARENT = (255, 192, 203, 0)
BROWN = (139,69,19)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

screen = pygame.display.set_mode([square_size*8, square_size*8])

# Fill the background with white
screen.fill((255, 255, 255))
square_size=50
# # Draw the grid
# for i in range(8):
#     for j in range(8):
#         if (i+j)%2==0:
#             pygame.draw.rect(screen, CREAM, [square_size*i,square_size*j,square_size,square_size])
#         else:
#             pygame.draw.rect(screen, BROWN, [square_size*i,square_size*j,square_size,square_size])
# Define the font
font = pygame.font.SysFont('Arial', 20)
bold_font = pygame.font.SysFont('Arial', 40, True)
bold_font_back = pygame.font.SysFont('Arial', 43, True)


class Unit:
    def __init__(self, unit_type, position):
        self.type = unit_type
        self.position = position

# Update the display
pygame.display.flip()
# Run until the user asks to quit
running = True

def sign(num):
    return -1 if num < 0 else 1

class Unit:
    def __init__(self, unit_type, position,colour):
        self.type = unit_type
        self.position = position
        self.colour = colour
        self.available_moves = []
        if self.type == 'pawn':
            self.en_passant = False


class Board:
    def __init__(self):
        self.units = []
        self.turn = 'white'
        self.can_kingside_castle = {'white': True, 'black': True}
        self.can_queenside_castle = {'white': True, 'black': True}
        self.in_check = None
        self.check_mate = None
        self.selected_unit = None
        self.en_passant = None
        self.half_move_clock=0
        self.full_move=0
        self.board_history=[]
        self.winner=None

    def add_unit(self, unit):
        # check if unit is a class Unit
        if type(unit) == Unit:
            self.units.append(unit)
        else:
            raise Exception('The unit is not a class Unit')

    def remove_unit(self, unit):

        
        self.units.remove(unit)

    def move_unit(self, unit, new_position):
        #check if the unit if a possition or a unit
        if type(unit)==tuple:
            unit=self.get_unit_at_position(unit)
        if unit.type == 'king' and self.can_kingside_castle[unit.colour]:
            if new_position == (6, 0) or new_position == (6, 7):
                if unit.colour == 'white':
                    self.move_unit((7, 7), (5, 7))
                else:
                    self.move_unit((7, 0), (5, 0))
             
        unit.position = new_position

    def get_unit_at_position(self, position):
        for unit in self.units:
            if unit.position == position:
                return unit
        return None
# Create the board
board = Board()

# # Add the white pawns
# for i in range(8):
#     board.add_unit(Unit('pawn', (i, 1), 'black'))

# # Add the black pawns
# for i in range(8):
#     board.add_unit(Unit('pawn', (i, 6), 'white'))

# # Add the white pieces
# board.add_unit(Unit('rook', (0, 0), 'black'))
# board.add_unit(Unit('knight', (1, 0), 'black'))
# board.add_unit(Unit('bishop', (2, 0), 'black'))
# board.add_unit(Unit('queen', (3, 0), 'black'))
# board.add_unit(Unit('king', (4, 0), 'black'))
# board.add_unit(Unit('bishop', (5, 0), 'black'))
# board.add_unit(Unit('knight', (6, 0), 'black'))
# board.add_unit(Unit('rook', (7, 0), 'black'))

# # Add the black pieces
# board.add_unit(Unit('rook', (0, 7), 'white'))
# board.add_unit(Unit('knight', (1, 7), 'white'))
# board.add_unit(Unit('bishop', (2, 7), 'white'))
# board.add_unit(Unit('queen', (3, 7), 'white'))
# board.add_unit(Unit('king', (4, 7), 'white'))
# board.add_unit(Unit('bishop', (5, 7), 'white'))
# board.add_unit(Unit('knight', (6, 7), 'white'))
# board.add_unit(Unit('rook', (7, 7), 'white'))

# the shapes of the pieces in a dict
shapes={'pawn':'p','rook':'r','knight':'n','bishop':'b','queen':'q','king':'k'}
anti_shapes={'p':'pawn','r':'rook','n':'knight','b':'bishop','q':'queen','k':'king'}
# # Draw the pieces

#make a function to draw the board and the pieces on it
def draw_board():
    # Draw the board
    for i in range(8):
        for j in range(8):
            # Is the square white?
            if (i + j) % 2 == 0:
                colour = CREAM
            else:
                colour = BROWN
            # Draw the square
            pygame.draw.rect(screen, colour, [square_size * i, square_size * j, square_size, square_size])
            # Draw the pieces
            unit = board.get_unit_at_position((i, j))
            if unit is not None:
                if unit.colour=='white':
                    # have the text be bold 
                    text_width, text_height = bold_font.size(shapes[unit.type])
                    text = bold_font.render(shapes[unit.type], True, WHITE)
                    #possition the text to be in the centre of the square
                    text_back=bold_font_back.render(shapes[unit.type], True, BLACK)
                    screen.blit(text_back, [square_size * (unit.position[0]+0.3), square_size * (unit.position[1])])
                    screen.blit(text, [square_size * (unit.position[0]+0.3), square_size * (unit.position[1])])

                else:
                    text = bold_font.render(shapes[unit.type], True, BLACK)
                    text_back=bold_font_back.render(shapes[unit.type], True, WHITE)
                    screen.blit(text_back, [square_size * (unit.position[0]+0.3), square_size * unit.position[1]])
                    screen.blit(text, [square_size * (unit.position[0]+0.3), square_size * unit.position[1]])
    #draw the letters and numbers on the side of the board
    for i in range(8):
        if i % 2 == 0:
            text = font.render(str(i + 1), True, CREAM)
        else:
            text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, [square_size*7.8,square_size * i])
    for i in range(8):
        if i % 2 == 0:
            text = font.render(chr(ord('A') + i), True, CREAM)
        else:
            text = font.render(chr(ord('A') + i), True, BLACK)
        screen.blit(text, [square_size * i , square_size*7.6])
draw_board()
#make a function that gets the board as the input and then returns the possible moves
def generate_moves(colour=None,checking=False,func_board=board):
    if colour is None:
        current_colour=func_board.turn
    else:
        current_colour=colour
    for piece in func_board.units:
        piece.avaliable_moves=[]
        if piece.colour==current_colour:
            peice_type=piece.type
            if peice_type=='pawn':
                if piece.colour=='black':
                    #check if there is a unit infrount of the pawn
                    if func_board.get_unit_at_position((piece.position[0],piece.position[1]+1)) is None and piece.position[1]+1<8:
                        piece.avaliable_moves.append((piece.position[0],piece.position[1]+1))
                        #check if the pawn is in its starting possition
                        if piece.position[1]==1:
                            if func_board.get_unit_at_position((piece.position[0],piece.position[1]+2)) is None:
                                piece.avaliable_moves.append((piece.position[0],piece.position[1]+2))
                    #check if there is a unit to the right of the pawn
                    if func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]+1)) is not None:
                        if func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]+1)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]+1,piece.position[1]+1))
                    #check if there is a unit to the left of the pawn
                    if func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]+1)) is not None:
                        if func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]+1)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]-1,piece.position[1]+1))
                    #check if the pawn can en passanted
                    if func_board.en_passant is not None:
                        if func_board.en_passant==(piece.position[0]+1,piece.position[1]):
                            piece.avaliable_moves.append((piece.position[0]+1,piece.position[1]+1))
                        elif func_board.en_passant==(piece.position[0]-1,piece.position[1]):
                            piece.avaliable_moves.append((piece.position[0]-1,piece.position[1]+1))

                else:
                    #check if there is a unit infrount of the pawn
                    if func_board.get_unit_at_position((piece.position[0],piece.position[1]-1)) is None and piece.position[1]-1>=0:
                        piece.avaliable_moves.append((piece.position[0],piece.position[1]-1))
                        #check if the pawn is in its starting possition
                        if piece.position[1]==6:
                            if func_board.get_unit_at_position((piece.position[0],piece.position[1]-2)) is None:
                                piece.avaliable_moves.append((piece.position[0],piece.position[1]-2))
                    #check if there is a unit to the right of the pawn
                    if func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]-1)) is not None:
                        if func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]-1)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]+1,piece.position[1]-1))
                    #check if there is a unit to the left of the pawn
                    if func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]-1)) is not None:
                        if func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]-1)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]-1,piece.position[1]-1))
                    #check if the pawn can en passanted
                    if func_board.en_passant is not None:
                        if func_board.en_passant==(piece.position[0]+1,piece.position[1]):
                            piece.avaliable_moves.append((piece.position[0]+1,piece.position[1]-1))
                        elif func_board.en_passant==(piece.position[0]-1,piece.position[1]):
                            piece.avaliable_moves.append((piece.position[0]-1,piece.position[1]-1))
            elif peice_type=='king':
                possible_moves=[(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
                for move in possible_moves:
                    if piece.position[0]+move[0]<8 and piece.position[0]+move[0]>=0 and piece.position[1]+move[1]<8 and piece.position[1]+move[1]>=0:
                        if func_board.get_unit_at_position((piece.position[0]+move[0],piece.position[1]+move[1])) is None:
                            piece.avaliable_moves.append((piece.position[0]+move[0],piece.position[1]+move[1]))
                        else:
                            if func_board.get_unit_at_position((piece.position[0]+move[0],piece.position[1]+move[1])).colour!=current_colour:
                                piece.avaliable_moves.append((piece.position[0]+move[0],piece.position[1]+move[1]))


            elif peice_type=='knight':
                knight_shifts=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
                for shift in knight_shifts:
                    if piece.position[0]+shift[0]<8 and piece.position[0]+shift[0]>=0 and piece.position[1]+shift[1]<8 and piece.position[1]+shift[1]>=0:
                        if func_board.get_unit_at_position((piece.position[0]+shift[0],piece.position[1]+shift[1])) is None:
                            piece.avaliable_moves.append((piece.position[0]+shift[0],piece.position[1]+shift[1]))
                        else:
                            if func_board.get_unit_at_position((piece.position[0]+shift[0],piece.position[1]+shift[1])).colour!=current_colour:
                                piece.avaliable_moves.append((piece.position[0]+shift[0],piece.position[1]+shift[1]))
                continue
            if peice_type=='rook' or peice_type=='queen':
                #check if there is a unit infront of the rook
                for i in range(1,8-piece.position[1]):
                    if func_board.get_unit_at_position((piece.position[0],piece.position[1]+i)) is None:
                        piece.avaliable_moves.append((piece.position[0],piece.position[1]+i))
                    else:
                        if func_board.get_unit_at_position((piece.position[0],piece.position[1]+i)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0],piece.position[1]+i))
                        break
                #check if there is a unit behind the rook
                for i in range(1,1+piece.position[1]):
                    if func_board.get_unit_at_position((piece.position[0],piece.position[1]-i)) is None:
                        piece.avaliable_moves.append((piece.position[0],piece.position[1]-i))
                    else:
                        if func_board.get_unit_at_position((piece.position[0],piece.position[1]-i)).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0],piece.position[1]-i))
                        break
                #check if there is a unit to the right of the rook
                for i in range(1,8-piece.position[0]):
                    if func_board.get_unit_at_position((piece.position[0]+i,piece.position[1])) is None:
                        piece.avaliable_moves.append((piece.position[0]+i,piece.position[1]))
                    else:
                        if func_board.get_unit_at_position((piece.position[0]+i,piece.position[1])).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]+i,piece.position[1]))
                        break
                #check if there is a unit to the left of the rook
                for i in range(1,1+piece.position[0]):
                    if func_board.get_unit_at_position((piece.position[0]-i,piece.position[1])) is None:
                        piece.avaliable_moves.append((piece.position[0]-i,piece.position[1]))
                    else:
                        if func_board.get_unit_at_position((piece.position[0]-i,piece.position[1])).colour!=current_colour:
                            piece.avaliable_moves.append((piece.position[0]-i,piece.position[1]))
                        break
                if peice_type=='rook':
                    continue
            if peice_type=='bishop' or peice_type=='queen':
                moves_bottom_right=-min(7-piece.position[0],7-piece.position[1])
                moves_bottom_left=-min(piece.position[0],7-piece.position[1])
                moves_top_right=min(7-piece.position[0],piece.position[1])+1
                moves_top_left=min(piece.position[0],piece.position[1])+1

                for move in [moves_bottom_left,moves_top_right]:
                    for i in range(sign(move),move+sign(move),sign(move)):
                        if func_board.get_unit_at_position((piece.position[0]+i,piece.position[1]-i)) is None:
                            piece.avaliable_moves.append((piece.position[0]+i,piece.position[1]-i))
                        else:
                            if func_board.get_unit_at_position((piece.position[0]+i,piece.position[1]-i)).colour!=current_colour:
                                piece.avaliable_moves.append((piece.position[0]+i,piece.position[1]-i))
                            break
                for move in [moves_bottom_right,moves_top_left]:
                    for i in range(sign(move),move+sign(move),sign(move)):
                        if func_board.get_unit_at_position((piece.position[0]-i,piece.position[1]-i)) is None:
                            piece.avaliable_moves.append((piece.position[0]-i,piece.position[1]-i))
                        else:
                            if func_board.get_unit_at_position((piece.position[0]-i,piece.position[1]-i)).colour!=current_colour:
                                piece.avaliable_moves.append((piece.position[0]-i,piece.position[1]-i))
                            break
    if not checking:
        for temp_piece in func_board.units:
            temp_board=copy.deepcopy(func_board)
            moves_to_remove=[]
            for move in temp_piece.avaliable_moves:
                                #if there is a unit in the new square delete it
                unit_attacked=temp_board.get_unit_at_position(move)
                #check if the unit is a pawn and if it has performed an en passant
                if temp_piece.type=='pawn' and temp_board.en_passant is not None:
                    if temp_board.en_passant==(temp_piece.position[0]+1,temp_piece.position[1]) or temp_board.en_passant==(temp_piece.position[0]-1,temp_piece.position[1]):
                        unit_attacked=temp_board.get_unit_at_position(temp_board.en_passant)

                if unit_attacked is not None:
                    temp_board.units.remove(unit_attacked)
                temp_board.move_unit(temp_piece.position,move)
                if temp_piece.type=='king':
                    temp_board.can_kingside_castle[temp_board.turn]=False
                    temp_board.can_queenside_castle[temp_board.turn]=False
                elif temp_piece.type=='rook':
                    if temp_piece.position[0]==0:
                        temp_board.can_queenside_castle[temp_board.turn]=False
                    elif temp_piece.position[0]==7:
                        temp_board.can_kingside_castle[temp_board.turn]=False


                if check_check(colour=current_colour,func_board=temp_board):
                    moves_to_remove.append(move)
                temp_board=copy.deepcopy(func_board)
            for move in moves_to_remove:
                temp_piece.avaliable_moves.remove(move)
    #check if the king can castle kingside
    if func_board.can_kingside_castle[current_colour]:
        if current_colour=='white':
            x=7
        else:
            x=0
        if func_board.get_unit_at_position((5,x)) is None and func_board.get_unit_at_position((6,x)) is None:
            temp_board=copy.deepcopy(func_board)
            for i in range(1,3):
                temp_board.move_unit((4,x),(4+i,x))
                if check_check(colour=current_colour,func_board=temp_board):
                    func_board.can_kingside_castle[current_colour]=False
                    break
                temp_board=copy.deepcopy(func_board)
            for piece in func_board.units:
                if piece.colour==current_colour:
                    if piece.type=='king':
                        piece.avaliable_moves.append((6,x))
                        break


#function sees if the board is in checkmate
def check_mate():
    if board.in_check is None:
        return False
    else:
        for piece in board.units:
            if piece.colour==board.turn:
                if piece.avaliable_moves!=[]:
                    return False
    return True
#function sees if the board is in stalemate
def stale_mate():
    if board.in_check is not None:
        return False
    else:
        for piece in board.units:
            if piece.colour==board.turn:
                if piece.avaliable_moves!=[]:
                    return False
    return True
#make a function that checks if a square is avaliable to move to
def individual_checker(position_to_check,colour):
    #check if there is a unit at the position
    if board.get_unit_at_position(position_to_check) is not None:
        #check if the unit is the same colour
        if board.get_unit_at_position(position_to_check).colour==colour:
            return False
        else:
            return True
    else:
        return True
#make a function that checks if the king is in check
def check_check(colour=None,func_board=board):
    if colour is None:
        if func_board.turn=='white':
            current_colour='black'
        else:
            current_colour='white'
    else:
        current_colour=colour
    opponent_colour='white' if current_colour=='black' else 'black'
    for piece in func_board.units:
        if piece.colour==current_colour:
            if piece.type=='king':
                king_position=piece.position
                break
    generate_moves(opponent_colour,checking=True,func_board=func_board)
    #check if there is a unit that can attack the king
    for piece_check in func_board.units:
        if piece_check.colour!=current_colour:
            if king_position in piece_check.avaliable_moves:
                return True
    return False
"""
This function will load starting position of the pieces using the FEN notation
"""
def load_FEN(FEN):
    #split the FEN into the different parts
    FEN_parts=FEN.split(' ')
    #split the first part into the different rows
    FEN_rows=FEN_parts[0].split('/')
    #go through each row
    for i in range(len(FEN_rows)-1,-1,-1):
        #go through each character in the row
        for j in range(len(FEN_rows[i])):
            #check if the character is a number
            if not FEN_rows[i][j].isnumeric():
                #check if the character is uppercase
                if FEN_rows[i][j].isupper():
                    #add the piece
                    board.add_unit(Unit(anti_shapes[FEN_rows[i][j].lower()],(j,i),'white'))
                #if it is a letter add that piece
                else:
                    board.add_unit(Unit(anti_shapes[FEN_rows[i][j]],(j,i),'black'))
    #set the turn
    if FEN_parts[1]=='w':
        board.turn='white'
    else:

        board.turn='black'
    #set the castling
    if FEN_parts[2]=='-':
        board.can_kingside_castle['white']=False
        board.can_kingside_castle['black']=False
        board.can_queenside_castle['white']=False
        board.can_queenside_castle['black']=False
    else:
        for letter in FEN_parts[2]:
            if letter=='K':
                board.can_kingside_castle['white']=True
            elif letter=='Q':
                board.can_queenside_castle['white']=True
            elif letter=='k':
                board.can_kingside_castle['black']=True
            elif letter=='q':
                board.can_queenside_castle['black']=True
    #set the en passant
    if FEN_parts[3]=='-':
        board.en_passant=None
    else:
        board.en_passant=(ord(FEN_parts[3][0])-97,int(FEN_parts[3][1])-1)
    #set the half move clock
    board.half_move_clock=int(FEN_parts[4])
    #set the full move number
    board.full_move=int(FEN_parts[5])
#from board create a FEN
def create_FEN(short=False):
    FEN=''
    for i in range(7,-1,-1):
        empty=0
        for j in range(8):
            unit=board.get_unit_at_position((j,i))
            if unit is None:
                empty+=1
            else:
                if empty!=0:
                    FEN+=str(empty)
                    empty=0
                if unit.colour=='white':
                    FEN+=shapes[unit.type].upper()
                else:
                    FEN+=shapes[unit.type]
        if empty!=0:
            FEN+=str(empty)
        if i!=0:
            FEN+='/'
    if short:
        return FEN
    FEN+=' '
    if board.turn=='white':
        FEN+='w'
    else:
        FEN+='b'
    FEN+=' '
    if board.can_kingside_castle['white'] or board.can_queenside_castle['white'] or board.can_kingside_castle['black'] or board.can_queenside_castle['black']:
        if board.can_kingside_castle['white']:
            FEN+='K'
        if board.can_queenside_castle['white']:
            FEN+='Q'
        if board.can_kingside_castle['black']:
            FEN+='k'
        if board.can_queenside_castle['black']:
            FEN+='q'
    else:
        FEN+='-'
    FEN+=' '
    if board.en_passant is not None:
        FEN+=chr(board.en_passant[0]+97)+str(board.en_passant[1]+1)
    else:
        FEN+='-'
    FEN+=' '
    FEN+=str(board.half_move_clock)
    FEN+=' '
    FEN+=str(board.full_move)
    return FEN
#function for checking a three fold repetition
def three_fold_repetition():
    fen=board.board_history[-1]
    count=0
    for i in range(len(board.board_history)-1,-1,-1):
        if board.board_history[i]==fen:
            count+=1
        if count==3:
            return True

    
load_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
draw_board()
generate_moves()
#save the board
board.board_history.append(create_FEN(True))


while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and board.winner is None:
            # Check if the click occurred within a square
            x, y = event.pos



            i, j = (x) // square_size, y // square_size
            #check if there is a selected piece
            if board.selected_unit is None:

                
                print(x,y)
                
                #check if there is a piece in the square and if there is any selected pieces
                unit_selected = board.get_unit_at_position((i, j))
                
                
                if unit_selected is not None and unit_selected.colour==board.turn and unit_selected.avaliable_moves!=[]:
                    board.selected_unit=unit_selected
                    unit_selected.selected=True
                    #change the colour of the square to a transparent pink
                    s = pygame.Surface((square_size,square_size))  # the size of your rect
                    s.set_alpha(150)                # alpha level
                    s.fill(PINK)           # this fills the entire surface
                    screen.blit(s,  [square_size * i, square_size * j, square_size, square_size])    # (0,0) are the top-left coordinates
                    #look at the possible moves and put a black circle on the squares
                    for move in unit_selected.avaliable_moves:
                        pygame.draw.circle(screen,BLACK,(square_size*move[0]+square_size/2,square_size*move[1]+square_size/2),square_size/5)
            #if there is selected peice and the new square is a possible move
            elif (i,j) in board.selected_unit.avaliable_moves:
                
                

                #if there is a unit in the new square delete it
                unit_attacked=board.get_unit_at_position((i,j))
                #check if the unit is a pawn and if it has performed an en passant
                if board.selected_unit.type=='pawn' and board.en_passant is not None:
                    if board.en_passant==(board.selected_unit.position[0]+1,board.selected_unit.position[1]) or board.en_passant==(board.selected_unit.position[0]-1,board.selected_unit.position[1]):
                        unit_attacked=board.get_unit_at_position(board.en_passant)
                #check if the unit is a pawn and if a capture has been made if so reset the half move clock
                if board.selected_unit.type=='pawn' or unit_attacked is not None:
                    board.half_move_clock=0
                else:
                    board.half_move_clock+=1

                if unit_attacked is not None:
                    board.units.remove(unit_attacked)



                #we will move the unit to the new position
                board.move_unit(board.selected_unit,(i,j))
                draw_board()
                if board.selected_unit.type=='king':
                    board.can_kingside_castle[board.turn]=False
                    board.can_queenside_castle[board.turn]=False
                elif board.selected_unit.type=='rook':
                    if board.selected_unit.position[0]==0:
                        board.can_queenside_castle[board.turn]=False
                    elif board.selected_unit.position[0]==7:
                        board.can_kingside_castle[board.turn]=False
                board.selected_unit=None
                #check if the opponents king is in check
                if check_check():
                    if board.turn=='white':
                        board.in_check='black'
                    else:
                        board.in_check='white'
                else:
                    board.in_check=None
                #change the turn and add one move to the full move
                if board.turn=='white':
                    board.turn='black'
                else:
                    board.turn='white'
                    board.full_move+=1


                #check if the pawn can be en passanted
                if unit_selected.type=='pawn':
                    if unit_selected.colour=='white':
                        if unit_selected.position[1]==4:
                            board.en_passant=unit_selected.position
                        else:
                            board.en_passant=None
                    else:
                        if unit_selected.position[1]==3:
                            board.en_passant=unit_selected.position
                        else:
                            board.en_passant=None
                else:
                    board.en_passant=None

                #if the pawn has reached the end of the board make it a queen
                if unit_selected.type=='pawn':
                    if unit_selected.colour=='white':
                        if unit_selected.position[1]==0:
                            board.units.remove(unit_selected)
                            board.units.append(Unit('queen',unit_selected.position,'white'))
                            unit_selected=board.get_unit_at_position(unit_selected.position)
                            draw_board()
                    else:
                        if unit_selected.position[1]==7:
                            board.units.remove(unit_selected)
                            board.units.append(Unit('queen',unit_selected.position,'black'))
                            unit_selected=board.get_unit_at_position(unit_selected.position)
                            draw_board()
                generate_moves()
                #save the board position
                board.board_history.append(create_FEN(True))
            elif (i,j)==board.selected_unit.position:
                board.selected_unit=None
                draw_board()
            #if in check draw a red square around the king
            if not board.in_check==None:

                for piece in board.units:
                    if piece.type=='king' and piece.colour==board.in_check:
                        i,j=piece.position
                        s = pygame.Surface((square_size,square_size))  # the size of your rect
                        s.set_alpha(150)                # alpha level
                        #if in checkmate draw a red square around the king
                        if check_mate():
                            s.fill(RED) 
                            if board.turn=='white':
                                board.check_mate='black'
                                board.winner='white'
                            else:
                                board.check_mate='white'
                                board.winner='black'
                        else:
                            s.fill(BLUE)    # this fills the entire surface
                        screen.blit(s,  [square_size * i, square_size * j, square_size, square_size])    # (0,0) are the top-left coordinates
                        break
            
            #if half move clock is 50 then the game is a draw
            if board.half_move_clock==50 or stale_mate() or three_fold_repetition():
                board.winner='draw'
                #draw green squares around the kings
                for piece in board.units:
                    if piece.type=='king':
                        i,j=piece.position
                        s = pygame.Surface((square_size,square_size))
                        s.set_alpha(150)
                        s.fill(GREEN)
                        screen.blit(s,  [square_size * i, square_size * j, square_size, square_size])



    # Update the display


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()