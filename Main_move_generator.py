import pygame
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
square_size=50

class Unit:
    def __init__(self, unit_type, position):
        self.type = unit_type
        self.position = position



all_moves={}
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
        #shows which pawn can be captured by en passant
        self.en_passant = None
        self.half_move_clock=0
        self.full_move=0
        self.board_history=[]
        self.winner=None
        self.units_positions=[]
    def add_unit(self, unit):
        # check if unit is a class Unit
        if type(unit) == Unit:
            self.units.append(unit)
        else:
            raise Exception('The unit is not a class Unit')

    def remove_unit(self, unit):

        
        self.units.remove(unit)

    def move_unit(self, unit, new_position,location=None):
        #check if the unit if a possition or a unit
        if type(unit)==tuple:
            unit,location=self.get_unit_at_position(unit,return_location=True)
        if unit.type == 'king' and self.can_kingside_castle[unit.colour]:
            if new_position == (6, 0) or new_position == (6, 7):
                if unit.colour == 'white':
                    self.move_unit((7, 7), (5, 7))
                else:
                    self.move_unit((7, 0), (5, 0))
        if unit.type == 'king' and self.can_queenside_castle[unit.colour]:
            if new_position == (2, 0) or new_position == (2, 7):
                if unit.colour == 'white':
                    self.move_unit((0, 7), (3, 7))
                else:
                    self.move_unit((0, 0), (3, 0))
             
        unit.position = new_position
        if location is None:
            location=self.units_positions.index(unit.position)
        self.units_positions[location]=new_position

    def get_unit_at_position(self, position,return_location=False):
        try:
            location=self.units_positions.index(position)
            if return_location:
                return self.units[location],location
            return self.units[location]

        except ValueError:
            return None
# Create the board


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
font = pygame.font.SysFont('Arial', 20)
bold_font = pygame.font.SysFont('Arial', 40, True)
bold_font_back = pygame.font.SysFont('Arial', 43, True)
#make a function to draw the board and the pieces on it
def draw_board():
    # Fill the background with white
    screen.fill((255, 255, 255))
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
            unit = board.get_unit_at_position((i, j),return_location=False)
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
            text = font.render(str(i + 1), True, BLACK)
        else:
            text = font.render(str(i + 1), True, CREAM)
        screen.blit(text, [square_size*7.8,square_size * (7-i)])
    for i in range(8):
        if i % 2 == 0:
            text = font.render(chr(ord('A') + i), True, CREAM)
        else:
            text = font.render(chr(ord('A') + i), True, BLACK)
        screen.blit(text, [square_size * i , square_size*7.6])
    
    #if the board has not reached an end state draw the turn at the bottom of the board
    if board.winner is None:
        #draw the turn at the bottom of the board
        if board.turn=='white':
            text = font.render('White to move', True, BLACK)
        else:
            text = font.render('Black to move', True, BLACK)
        screen.blit(text, [square_size * 3.5, square_size*8])
    elif board.winner=='white':
        text = font.render('White wins', True, BLACK)
        screen.blit(text, [square_size * 3.5, square_size*8])
    elif board.winner=='black':
        text = font.render('Black wins', True, BLACK)
        screen.blit(text, [square_size * 3.5, square_size*8])
    elif board.winner=='draw':
        text = font.render('Draw', True, BLACK)
        screen.blit(text, [square_size * 3.5, square_size*8])

#make a function that gets the board as the input and then returns the possible moves
def generate_moves(colour=None,checking=False,func_board=None,give_back_moves=False):
    if func_board is None:
        func_board=board

    if colour is None:
        current_colour=func_board.turn
    else:
        current_colour=colour
    current_possition_long=create_FEN(func_board=func_board)
    current_possition=current_possition_long[:-4]
    if current_possition in all_moves:
        print('found')
        if give_back_moves:
            return all_moves[current_possition]
        func_board.move_list=all_moves[current_possition]
        for piece in func_board.units:
            piece.avaliable_moves=[]
            for move in func_board.move_list:
                if move[0]==piece.position:
                    piece.avaliable_moves.append(move[1])
        return
    else:
        temp_move_list=[]

        for piece in func_board.units:
            if piece.colour==current_colour:
                peice_type=piece.type
                if peice_type=='king' and not checking:
                    possible_moves=[(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]
                    for move in possible_moves:
                        if piece.position[0]+move[0]<8 and piece.position[0]+move[0]>=0 and piece.position[1]+move[1]<8 and piece.position[1]+move[1]>=0:
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]+move[0],piece.position[1]+move[1]),return_location=False)
                            if unit_in_square is None or unit_in_square.colour!=current_colour:
                                temp_move_list.append((piece.position,(piece.position[0]+move[0],piece.position[1]+move[1])))
                elif peice_type=='knight':
                    if checking and (abs(piece.position[0]-checking[0])>2 or abs(piece.position[1]-checking[1])>2):
                        continue
                    knight_shifts=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
                    for shift in knight_shifts:
                        if piece.position[0]+shift[0]<8 and piece.position[0]+shift[0]>=0 and piece.position[1]+shift[1]<8 and piece.position[1]+shift[1]>=0:
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]+shift[0],piece.position[1]+shift[1]),return_location=False)
                            if unit_in_square is None:
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0]+shift[0],piece.position[1]+shift[1])))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0]+shift[0],piece.position[1]+shift[1])))
                    continue
                elif peice_type=='rook' or peice_type=='queen':
                    if checking and (abs(piece.position[0]-checking[0])!=0 and abs(piece.position[1]-checking[1])!=0):
                            if peice_type=='rook':
                                continue
                    else:
                        #check if there is a unit infront of the rook
                        for i in range(1,8-piece.position[1]):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0],piece.position[1]+i),return_location=False)
                            if unit_in_square is None :
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0],piece.position[1]+i)))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0],piece.position[1]+i)))
                                break
                            else:
                                break
                        #check if there is a unit behind the rook
                        for i in range(1,1+piece.position[1]):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0],piece.position[1]-i),return_location=False)
                            if unit_in_square is None :
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0],piece.position[1]-i)))                    
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0],piece.position[1]-i)))
                                break
                            else:
                                break
                        #check if there is a unit to the right of the rook
                        for i in range(1,8-piece.position[0]):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]+i,piece.position[1]),return_location=False)
                            if unit_in_square is None:
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0]+i,piece.position[1])))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0]+i,piece.position[1])))
                                break
                            else:
                                break
                        #check if there is a unit to the left of the rook
                        for i in range(1,1+piece.position[0]):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]-i,piece.position[1]),return_location=False)
                            if unit_in_square is None:
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0]-i,piece.position[1])))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0]-i,piece.position[1])))
                                break
                            else:
                                break
                    if peice_type=='rook':
                        continue
                if peice_type=='bishop' or peice_type=='queen':
                    if checking and (abs(piece.position[0]-checking[0])!=abs(piece.position[1]-checking[1])):
                        continue
                    moves_bottom_right=-min(7-piece.position[0],7-piece.position[1])-1
                    moves_bottom_left=-min(piece.position[0],7-piece.position[1])-1
                    moves_top_right=min(7-piece.position[0],piece.position[1])+1
                    moves_top_left=min(piece.position[0],piece.position[1])+1

                    for move in [moves_bottom_left,moves_top_right]:
                        for i in range(sign(move),move,sign(move)):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]+i,piece.position[1]-i),return_location=False)
                            if unit_in_square is None :
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0]+i,piece.position[1]-i)))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0]+i,piece.position[1]-i)))
                                break
                            else:
                                break
                    for move in [moves_bottom_right,moves_top_left]:
                        for i in range(sign(move),move,sign(move)):
                            unit_in_square=func_board.get_unit_at_position((piece.position[0]-i,piece.position[1]-i),return_location=False)
                            if unit_in_square is None:
                                if checking:
                                    continue
                                temp_move_list.append((piece.position,(piece.position[0]-i,piece.position[1]-i)))
                            elif unit_in_square.colour!=current_colour:
                                if checking:
                                    if unit_in_square.type=='king':
                                        return True
                                temp_move_list.append((piece.position,(piece.position[0]-i,piece.position[1]-i)))
                                break
                            else:
                                break
                elif peice_type=='pawn':
                    if checking and (abs(piece.position[0]-checking[0])!=1 or abs(piece.position[1]-checking[1])!=1):
                        continue
                    if piece.colour=='black':
                        #check if there is a unit infrount of the pawn
                        if func_board.get_unit_at_position((piece.position[0],piece.position[1]+1),return_location=False) is None and piece.position[1]+1<8 and not checking:
                            temp_move_list.append((piece.position,(piece.position[0],piece.position[1]+1)))
                            #check if the pawn is in its starting possition
                            if piece.position[1]==1:
                                if func_board.get_unit_at_position((piece.position[0],piece.position[1]+2),return_location=False) is None :
                                    temp_move_list.append((piece.position,(piece.position[0],piece.position[1]+2)))
                        #check if there is a unit to the right of the pawn
                        right_unit=func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]+1),return_location=False)
                        if right_unit is not None and right_unit.colour!=current_colour:
                            if checking: 
                                if right_unit.type=='king':
                                    return True
                            temp_move_list.append((piece.position,(piece.position[0]+1,piece.position[1]+1)))
                        #check if there is a unit to the left of the pawn
                        left_unit=func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]+1),return_location=False)
                        if left_unit is not None and left_unit.colour!=current_colour:
                            if checking:
                                if left_unit.type=='king':
                                    return True
                            temp_move_list.append((piece.position,(piece.position[0]-1,piece.position[1]+1)))
                
                        #check if the pawn can en passanted
                        if func_board.en_passant is not None and not checking:
                            if func_board.en_passant==(piece.position[0]+1,piece.position[1]+1):
                                temp_move_list.append((piece.position,(piece.position[0]+1,piece.position[1]+1)))
                            elif func_board.en_passant==(piece.position[0]-1,piece.position[1]+1):
                                temp_move_list.append((piece.position,(piece.position[0]-1,piece.position[1]+1)))

                    else:
                        #check if there is a unit infrount of the pawn
                        if func_board.get_unit_at_position((piece.position[0],piece.position[1]-1),return_location=False) is None and piece.position[1]-1>=0 and not checking:
                            temp_move_list.append((piece.position,(piece.position[0],piece.position[1]-1)))
                            #check if the pawn is in its starting possition
                            if piece.position[1]==6:
                                if func_board.get_unit_at_position((piece.position[0],piece.position[1]-2),return_location=False) is None:
                                    temp_move_list.append((piece.position,(piece.position[0],piece.position[1]-2)))
                        #check if there is a unit to the right of the pawn
                        right_unit=func_board.get_unit_at_position((piece.position[0]+1,piece.position[1]-1),return_location=False)
                        if right_unit is not None and right_unit.colour!=current_colour:
                            if checking:
                                if right_unit.type=='king':
                                    return True
                            temp_move_list.append((piece.position,(piece.position[0]+1,piece.position[1]-1)))
                        #check if there is a unit to the left of the pawn
                        left_unit=func_board.get_unit_at_position((piece.position[0]-1,piece.position[1]-1),return_location=False)
                        if left_unit is not None and left_unit.colour!=current_colour:
                            if checking:
                                if left_unit.type=='king':
                                    return True
                            temp_move_list.append((piece.position,(piece.position[0]-1,piece.position[1]-1)))
                        #check if the pawn can en passanted
                        if func_board.en_passant is not None and not checking:
                            if func_board.en_passant==(piece.position[0]+1,piece.position[1]-1):
                                temp_move_list.append((piece.position,(piece.position[0]+1,piece.position[1]-1)))
                            elif func_board.en_passant==(piece.position[0]-1,piece.position[1]-1):
                                temp_move_list.append((piece.position,(piece.position[0]-1,piece.position[1]-1)))

    if not checking:
        moves_to_remove=[]
        temp_board=Board()
        load_FEN(current_possition_long,func_board=temp_board)
        for check_move in temp_move_list:
            move_piece(check_move[0],check_move[1],temp_board)
            if check_check(colour=current_colour,func_board=temp_board):
                moves_to_remove.append(check_move)
            temp_board=Board()
            load_FEN(current_possition_long,func_board=temp_board)
        for move in moves_to_remove:
            temp_move_list.remove(move)
    #check if the king can castle kingside
    if func_board.can_kingside_castle[current_colour] and not checking:
        if current_colour=='white':
            x=7
        else:
            x=0
        if func_board.get_unit_at_position((5,x),return_location=False) is None and func_board.get_unit_at_position((6,x),return_location=False) is None:

            temp_board=Board()
            load_FEN(current_possition_long,func_board=temp_board)
            for i in range(1,3):
                temp_board.move_unit((4,x),(4+i,x))
                if check_check(colour=current_colour,func_board=temp_board):
                    func_board.can_kingside_castle[current_colour]=False
                    break
                load_FEN(current_possition_long,func_board=temp_board)
            if func_board.can_kingside_castle[current_colour]:
                for piece in func_board.units:
                    if piece.colour==current_colour:
                        if piece.type=='king':
                            temp_move_list.append((piece.position,(6,x)))
                            break
    #check if the king can castle queenside
    if func_board.can_queenside_castle[current_colour] and not checking:
        if current_colour=='white':
            x=7
        else:
            x=0
        if func_board.get_unit_at_position((1,x),return_location=False) is None and func_board.get_unit_at_position((2,x),return_location=False) is None and func_board.get_unit_at_position((3,x),return_location=False) is None:
            temp_board=Board()
            load_FEN(current_possition_long,func_board=temp_board)
            for i in range(1,3):
                temp_board.move_unit((4,x),(4-i,x))
                if check_check(colour=current_colour,func_board=temp_board):
                    func_board.can_queenside_castle[current_colour]=False
                    break
                load_FEN(current_possition_long,func_board=temp_board)
            if func_board.can_queenside_castle[current_colour]:
                for piece in func_board.units:
                    if piece.colour==current_colour:
                        if piece.type=='king':
                            temp_move_list.append((piece.position,(2,x)))
                            break
    #has checked all the moves and the king is not in check
    if checking:
        return False
    #add the possible move list to the dictionary
    if give_back_moves:
        return temp_move_list
    else:
        func_board.move_list=temp_move_list
        for piece in func_board.units:
            piece.avaliable_moves=[]
            for move in temp_move_list:
                if move[0]==piece.position:
                    piece.avaliable_moves.append(move[1])
    if not checking:
        all_moves[current_possition]=func_board.move_list
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
def check_check(colour=None,func_board=None):
    if func_board is None:
        func_board=board
    #gets the turn of the board
    if colour is None:
        if func_board.turn=='white':
            current_colour='black'
        else:
            current_colour='white'
    else:
        current_colour=colour
    opponent_colour='white' if current_colour=='black' else 'black'
    #find the position of the king
    for piece in func_board.units:
        if piece.colour==current_colour:
            if piece.type=='king':
                king_position=piece.position
                break
    func_board.turn=opponent_colour
    check=generate_moves(checking=king_position,func_board=func_board,give_back_moves=True)
    func_board.turn=opponent_colour
    #check if there is a unit that can attack the king
    return check

"""
This function will load starting position of the pieces using the FEN notation
"""
def load_FEN(FEN,func_board=None):
    if func_board is None:
        func_board=board
    #split the FEN into the different parts
    FEN_parts=FEN.split(' ')
    #split the first part into the different rows
    FEN_rows=FEN_parts[0].split('/')
    #go through each row
    for i in range(len(FEN_rows)-1,-1,-1):
        to_add=0
        #go through each character in the row
        for j in range(len(FEN_rows[i])):
            #check if the character is a number
            if not FEN_rows[i][j].isnumeric():
                #check if the character is uppercase
                if FEN_rows[i][j].isupper():
                    #add the piece
                    func_board.add_unit(Unit(anti_shapes[FEN_rows[i][j].lower()],(j+to_add,i),'white'))
                    func_board.units_positions.append((j+to_add,i))
                #if it is a letter add that piece
                else:
                    func_board.add_unit(Unit(anti_shapes[FEN_rows[i][j]],(j+to_add,i),'black'))
                    func_board.units_positions.append((j+to_add,i))
            #if it is a number add that many empty squares
            else:
                to_add+=int(FEN_rows[i][j])-1
    #set the turn
    if FEN_parts[1]=='w':
        func_board.turn='white'
    else:

        func_board.turn='black'
    #set the castling
    if FEN_parts[2]=='-':
        func_board.can_kingside_castle['white']=False
        func_board.can_kingside_castle['black']=False
        func_board.can_queenside_castle['white']=False
        func_board.can_queenside_castle['black']=False
    else:
        for letter in FEN_parts[2]:
            if letter=='K':
                func_board.can_kingside_castle['white']=True
            elif letter=='Q':
                func_board.can_queenside_castle['white']=True
            elif letter=='k':
                func_board.can_kingside_castle['black']=True
            elif letter=='q':
                func_board.can_queenside_castle['black']=True
    #set the en passant
    if FEN_parts[3]=='-':
        func_board.en_passant=None
    else:
        func_board.en_passant=(ord(FEN_parts[3][0])-97,8-int(FEN_parts[3][1]))
    #set the half move clock
    func_board.half_move_clock=int(FEN_parts[4])
    #set the full move number
    func_board.full_move=int(FEN_parts[5])
#from board create a FEN
def create_FEN(short=False,func_board=None):
    if func_board is None:
        func_board=board
    FEN=''
    for i in range(0,8,1):
        empty=0
        for j in range(8):
            unit=func_board.get_unit_at_position((j,i),return_location=False)
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
        if i!=7:
            FEN+='/'
    FEN+=' '
    if func_board.turn=='white':
        FEN+='w'
    else:
        FEN+='b'
    FEN+=' '
    if func_board.can_kingside_castle['white'] or func_board.can_queenside_castle['white'] or func_board.can_kingside_castle['black'] or func_board.can_queenside_castle['black']:
        if func_board.can_kingside_castle['white']:
            FEN+='K'
        if func_board.can_queenside_castle['white']:
            FEN+='Q'
        if func_board.can_kingside_castle['black']:
            FEN+='k'
        if func_board.can_queenside_castle['black']:
            FEN+='q'
    else:
        FEN+='-'
    FEN+=' '
    if func_board.en_passant is not None:
        FEN+=chr(func_board.en_passant[0]+97)+str(8-func_board.en_passant[1])
    else:
        FEN+='-'
    if short:
        return FEN
    FEN+=' '
    FEN+=str(func_board.half_move_clock)
    FEN+=' '
    FEN+=str(func_board.full_move)
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

#Function when moving a piece will take and change en passant and castling etc
def move_piece(piece,move,func_board=None,checking=False):
    if func_board is None:
        func_board=board
    # if the piece is a touple find the piece
    if type(piece)==tuple:
        piece=func_board.get_unit_at_position(piece)
    #if there is a unit in the new square delete it
    unit_attacked=func_board.get_unit_at_position(move)
    if unit_attacked is not None:
        func_board.units_positions.remove(unit_attacked.position)
        func_board.units.remove(unit_attacked)
    unit_attacked=None
    func_board.move_unit(piece.position,move)
    #check if the unit is a pawn and if it has performed an en passant
    if piece.type=='pawn' and func_board.en_passant is not None:
        if func_board.en_passant==(piece.position[0],piece.position[1]) :
            if piece.colour=='white':
                unit_attacked=func_board.get_unit_at_position((piece.position[0],piece.position[1]+1))
            else:
                unit_attacked=func_board.get_unit_at_position((piece.position[0],piece.position[1]-1))
    if unit_attacked is not None:
        func_board.units_positions.remove(unit_attacked.position)
        func_board.units.remove(unit_attacked)
    
    
    if piece.type=='king':
        func_board.can_kingside_castle[func_board.turn]=False
        func_board.can_queenside_castle[func_board.turn]=False
    elif piece.type=='rook':
        if piece.position[0]==0:
            func_board.can_queenside_castle[func_board.turn]=False
        elif piece.position[0]==7:
            func_board.can_kingside_castle[func_board.turn]=False
    #check if the unit is a pawn and if a capture has been made if so reset the half move clock
    if piece.type=='pawn' or unit_attacked is not None:
        func_board.half_move_clock=0
    else:
        func_board.half_move_clock+=1
                    #we will move the unit to the new position
    if checking:
        #check if the opponents king is in check
        if check_check(func_board=func_board):
            if func_board.turn=='white':
                func_board.in_check='black'
            else:
                func_board.in_check='white'
        else:
            func_board.in_check=None
    #change the turn and add one move to the full move
    if func_board.turn=='white':
        func_board.turn='black'
    else:
        func_board.turn='white'
        func_board.full_move+=1


    #check if the pawn can be en passanted
    if piece.type=='pawn':
        if piece.colour=='white':
            if piece.position[1]==4:
                func_board.en_passant=(piece.position[0],piece.position[1]+1)
            else:
                func_board.en_passant=None
        else:
            if piece.position[1]==3:
                func_board.en_passant=(piece.position[0],piece.position[1]-1)
            else:
                func_board.en_passant=None
    else:
        func_board.en_passant=None
    #if the pawn has reached the end of the board make it a queen
    if piece.type=='pawn':
        if piece.colour=='white':
            if piece.position[1]==0:
                func_board.units.append(Unit('queen',piece.position,'white'))

                func_board.units.remove(piece)
        else:
            if piece.position[1]==7:
                func_board.units.append(Unit('queen',piece.position,'black'))
                func_board.units.remove(piece)
