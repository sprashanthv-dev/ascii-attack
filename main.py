# The main.py file exists as an entry point to the game.
# Its main purpose is to start the application and
# delegate responsibility to the Game Manager class.

from game_manager import GameManager

game_manager = GameManager()

# Need to check if each block is active or not
#  if still active then need to increment y_pos of that block