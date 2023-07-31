from Main_move_generator import *
import Main_move_generator
import pygame

board=Board()
Main_move_generator.board=board
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