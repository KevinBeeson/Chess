from Main_move_generator import *
import Main_move_generator
import pygame

pygame.init()




screen = pygame.display.set_mode([square_size*8, square_size*8.5])

# Fill the background with white
screen.fill((255, 255, 255))




Main_move_generator.screen=screen

board=Board()
Main_move_generator.board=board
load_FEN("rnb1kbnr/pppppppp/8/8/7q/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
draw_board()
generate_moves()
#save the board
board.board_history.append(create_FEN(True,func_board=board))
# Update the display
pygame.display.flip()
# Run until the user asks to quit
running = True
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
                #move the piece to the new square, capture the piece if there is one, changes the turns, en passant, half move clock, full move number, and promotion
                move_piece(board.selected_unit,(i,j))
                
                board.selected_unit=None
                generate_moves()
                #save the board position
                board.board_history.append(create_FEN(True))
                draw_board()
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
                            draw_board()
                        else:
                            s.fill(BLUE)    # this fills the entire surface
                        screen.blit(s,  [square_size * i, square_size * j, square_size, square_size])    # (0,0) are the top-left coordinates
                        break
            
            #if half move clock is 50 then the game is a draw
            if board.half_move_clock==50 or stale_mate() or three_fold_repetition():
                board.winner='draw'
                draw_board()
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