# The main.py file exists as an entry point to the game.
# Its main purpose is to start the application and
# delegate responsibility to the Game Manager class.

from game_manager import GameManager
from level_manager import LevelManager

level_manager = LevelManager()
game_manager = GameManager(level_manager)