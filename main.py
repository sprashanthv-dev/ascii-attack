# The main.py file exists as an entry point to the game.
# Its main purpose is to start the application and
# delegate responsibility to the Game Manager class.

# import random
# from block_decorator import BlockDecorator
# from block_manager import BlockManager
from game_manager import GameManager
# from block_hits import BlockHits


game_manager = GameManager()

# Testing decorator pattern
# block_manager = BlockManager(game_manager)

# random_number = random.randint(36, 39)

# block_factory = block_manager.get_factory(random_number)

# block = block_factory.create_block()
# print("Before decorating "  + str(block.hits_left))

# block = BlockHits(block)
# block = block.get_hits()

# print("After decorating " + str(block.hits_left))
