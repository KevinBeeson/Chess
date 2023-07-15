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
        self.can_castle = {'white': True, 'black': True}
        self.in_check = None
        self.check_mate = None
        self.selected_unit = None


    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        
        self.units.remove(unit)

    def move_unit(self, unit, new_position):
        #check if the unit if a possition or a unit
        if type(unit)==tuple:
            unit=self.get_unit_at_position(unit)
        unit.position = new_position

    def get_unit_at_position(self, position):
        for unit in self.units:
            if unit.position == position:
                return unit
        return None
# Create the board
board = Board()

# Add the white pawns
for i in range(8):
    board.add_unit(Unit('pawn', (i, 1), 'black'))

# Add the black pawns
for i in range(8):
    board.add_unit(Unit('pawn', (i, 6), 'white'))

# Add the white pieces
board.add_unit(Unit('rook', (0, 0), 'black'))
board.add_unit(Unit('knight', (1, 0), 'black'))
board.add_unit(Unit('bishop', (2, 0), 'black'))
board.add_unit(Unit('queen', (3, 0), 'black'))
board.add_unit(Unit('king', (4, 0), 'black'))
board.add_unit(Unit('bishop', (5, 0), 'black'))
board.add_unit(Unit('knight', (6, 0), 'black'))
board.add_unit(Unit('rook', (7, 0), 'black'))

# Add the black pieces
board.add_unit(Unit('rook', (0, 7), 'white'))
board.add_unit(Unit('knight', (1, 7), 'white'))
board.add_unit(Unit('bishop', (2, 7), 'white'))
board.add_unit(Unit('queen', (3, 7), 'white'))
board.add_unit(Unit('king', (4, 7), 'white'))
board.add_unit(Unit('bishop', (5, 7), 'white'))
board.add_unit(Unit('knight', (6, 7), 'white'))
board.add_unit(Unit('rook', (7, 7), 'white'))

# the shapes of the pieces in a dict
shapes={'pawn':'p','rook':'r','knight':'n','bishop':'b','queen':'q','king':'k'}

# # Draw the pieces

# for piece in board.units:
#     if piece.colour=='white':
#         # have the text be bold 
#         text_width, text_height = bold_font.size(shapes[piece.type])
#         text = bold_font.render(shapes[piece.type], True, BLACK)
#         #possition the text to be in the centre of the square
#         text_back=bold_font_back.render(shapes[piece.type], True, WHITE)
#         screen.blit(text_back, [square_size * (piece.position[0]+0.3), square_size * (piece.position[1])])
#         screen.blit(text, [square_size * (piece.position[0]+0.3), square_size * (piece.position[1])])

#     else:
#         text = bold_font.render(shapes[piece.type], True, WHITE)
#         text_back=bold_font_back.render(shapes[piece.type], True, BLACK)
#         screen.blit(text_back, [square_size * (piece.position[0]+0.3), square_size * piece.position[1]])
#         screen.blit(text, [square_size * (piece.position[0]+0.3), square_size * piece.position[1]])
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
        temp_board=copy.deepcopy(func_board)
        for temp_piece in func_board.units:
            moves_to_remove=[]
            for move in temp_piece.avaliable_moves:
                temp_board.move_unit(temp_piece.position,move)
                if check_check(colour=current_colour,func_board=temp_board):
                    moves_to_remove.append(move)
                temp_board=copy.deepcopy(func_board)
            for move in moves_to_remove:
                temp_piece.avaliable_moves.remove(move)
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
generate_moves()
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
                if unit_attacked is not None:
                    board.units.remove(unit_attacked)
                #we will move the unit to the new position
                unit_selected.position=(i,j)
                draw_board()
                board.selected_unit=None
                #check if the opponents king is in check
                if check_check():
                    if board.turn=='white':
                        board.in_check='black'
                    else:
                        board.in_check='white'
                else:
                    board.in_check=None
                #change the turn
                if board.turn=='white':
                    board.turn='black'
                else:
                    board.turn='white'
                generate_moves()
            #if in check draw a red square around the king
            if not board.in_check==None:
                for piece in board.units:
                    if piece.type=='king' and piece.colour==board.in_check:
                        i,j=piece.position
                        s = pygame.Surface((square_size,square_size))  # the size of your rect
                        s.set_alpha(150)                # alpha level
                        s.fill(RED)           # this fills the entire surface
                        screen.blit(s,  [square_size * i, square_size * j, square_size, square_size])    # (0,0) are the top-left coordinates
                        break



    # Update the display


    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()