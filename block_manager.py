import pygame
import random
from destroy_block import DestroyBlock

from singleton import Singleton

from block_factory import BlockFactory
from letter_block_factory import LetterBlockFactory
from number_block_factory import NumberBlockFactory

from block import Block
from block_hits import BlockHits

from score_calculator import ScoreCalculator
from handle_commands import HandleCommands


# The BlockManager class deals with all operations
# related to blocks such as creating and destroying
# blocks, determine if it is time to spawn new blocks,
# and if blocks should continue move in the game loop.
class BlockManager(metaclass=Singleton):
  def __init__(self, game_manager):
    self.__block = None
    self.__game_manager = game_manager
    self.__score_calculator = ScoreCalculator()
    self.__blocks = []

    self.__block_x_limit = 825
    self.__block_y_limit = 700
    self.__y_start = 50
    self.__offset = 150

  @property
  def block(self):
    return self.__block

  @property
  def blocks(self):
    return self.__blocks

  @property
  def block_x_limit(self):
    return self.__block_x_limit

  @property
  def block_y_limit(self):
    return self.__block_y_limit

  @property
  def y_start(self):
    return self.__y_start

  @property
  def offset(self):
    return self.__offset

  @property
  def game_manager(self):
    return self.__game_manager
  
  @property
  def score_calculator(self):
    return self.__score_calculator

  @block.setter
  def block(self, value: Block):
    self.__block = value

  @blocks.setter
  def blocks(self, value=[]):
    self.__blocks = value

  # Create a block and return it
  def create_block(self) -> Block:
    random_number = random.randint(0, 45)

    # Get the corressponding block
    # factory based on random number
    block_factory = self.get_factory(random_number)

    # Create the block
    block = block_factory.create_block()
    
    # Decorate the block to apply the required
    # number of hits needed to destroy it.
    block = BlockHits(block)
    block = block.get_hits()

    # Track the created block in our blocks list.
    # This will be used later on to destroy blocks.
    self.blocks.append(block)

    return block

  # Get the block factory method based
  # on the random number generated
  def get_factory(self, random_number: int):
    block_factory: BlockFactory

    # If the block number lies between 0 and 9 inclusive,
    # it is a number block, otherwise it is a letter block.
    if random_number >= 0 and random_number <= 9:
      block_factory = NumberBlockFactory(random_number, self.game_manager.level_manager)
    else:
      block_factory = LetterBlockFactory(random_number, self.game_manager.level_manager)

    return block_factory

  # Destroy the block from the game
  def destroy_block(self,
                    ascii_value: int,
                    base: int,
                    block_hit_sound: pygame.mixer.Sound):

    # Store a reference of the current blocks in the game
    blocks = self.blocks
    item: Block = None

    # Reference: https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
    # Check if a block exists with the ascii value specified
    block: Block = filter(lambda block: int(
        block.block_number) == ascii_value - base, blocks)

    # Reference: https://stackoverflow.com/questions/68186924/how-do-i-check-if-a-filter-returns-no-results-in-python-3
    try:
      # Try to retrieve the filtered block, if it exists
      item = next(block)
    # If no block exists with the specified ascii value
    except StopIteration:

      # Check if the block is a special block
      block_number = (ascii_value - base) + 26
      
      block: Block = filter(lambda block: int(
          block.block_number) == block_number, blocks)

      try:
        item = next(block)
      except StopIteration:
        print("No item exists and not a special block")
        
    finally:
      if item is not None:
        # Get index of the current block
        item.hits_left = item.hits_left - 1
        
        # Update the player's current score
        self.score_calculator.score += item.point
        
        # Play block hit sound
        block_hit_sound.play()
        
        # If the block has no hits left, destroy it.
        # This is done through the Command Pattern.
        if item.hits_left == 0:
          command_handler = HandleCommands()
          command_handler.execute(DestroyBlock(item, self.game_manager, self))  
      else:
        print("Item is none")
      
  # Decide if it is time to spawn the next block
  def spawn_next_block(self,
                       timer_info,
                       spawned_blocks: int,
                       total_blocks: int) -> bool:
    
    # Get the timer configurations
    start_timer = timer_info["start_time"]
    current_timer = timer_info["current_time"]
    delay_timer = timer_info["delay_time"]

    # Check if the specified time duration has expired
    has_timer_expired = self.game_manager.has_timer_expired(
        start_timer,
        current_timer,
        delay_timer)

    # Check if the necessary amount of blocks for the
    # current level has been spawned.
    has_count_reached = self.block_count_reached(spawned_blocks, total_blocks)

    return has_timer_expired and not has_count_reached

  # Returns True if the required number of blocks have 
  # been spawned for the current level, False otherwise.
  def block_count_reached(self, spawned_blocks: int, total_blocks: int) -> bool:
    return True if spawned_blocks == total_blocks else False

  # Returns True if the current block's y-coordinate is 
  # less than the game window's y-coordinate, False otherwise.
  def can_block_move(self, block: Block) -> bool:
    return block.y_pos < self.block_y_limit

  # Returns True if the current block's y-coordinate is out of
  # bounds of the game window's y-coordinate, False otherwise
  def is_touching_ground(self, block: Block) -> bool:
    return block.y_pos >= self.block_y_limit
