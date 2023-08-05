from Main_move_generator import *
import Main_move_generator
import pygame

board=Board()
Main_move_generator.board=board
load_FEN("rnbqkbnr/pppppppp/8/8/8/4BN2/PPPPPPPP/RNBQK2R w KQkq - 0 1")
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
                move_piece(board.selected_unit,(i,j))
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