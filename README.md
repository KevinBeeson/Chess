# Chess engine

A recreation of the classic game of chess. 

Chess_game.py contains the main game. You can only currently play with another human. But engines will come. If a player is in check their king will be highlighted in blue, if checkmate happens the losing player's king will be red, if a draw happens both kings will be in Blue.

In Main_move_generator.py houses functions such as the FEN_loader, available move generator, checks whether you are in check, checks if an outcome of the game has been reached. 



Chess_move_checker.py checks how many moves is available depending on the depth 

## Requirements

--pygame


## To do 

Most of the main chess functions has been implemented. The only main rule that has not been implemented is promoting to something other than a queen. Auto-Queening is currently on.

Chess engines: Will try to provide a range of engines: Would like to have an engine with alpha beta pruning implemented. Time permitting would like to try using some ML to make better weights for the engine 
