import pygame
import random

from singleton import Singleton

from block_factory import BlockFactory
from letter_block_factory import LetterBlockFactory
from number_block_factory import NumberBlockFactory

from block import Block
from score_calculator import ScoreCalculator


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
    random_number = random.randint(0, 35)

    # Get the corressponding block
    # factory based on random number
    block_factory = self.get_factory(random_number)

    # Create the block
    block = block_factory.create_block()

    self.blocks.append(block)

    return block

  # Get the block factory method based
  # on the random number generated
  def get_factory(self, random_number: int):
    block_factory: BlockFactory

    if random_number >= 0 and random_number <= 9:
      block_factory = NumberBlockFactory(random_number)
    else:
      block_factory = LetterBlockFactory(random_number)

    return block_factory

  # Spawns blocks at regular intervals
  def spawn_block(self):
    pass

  # Update the number of hits a
  # block has received
  def update_block_hits(self):
    pass

  # Destroy the block from the game
  def destroy_block(self, ascii_value: int, base: int):

    # Store a reference of the current blocks in the game
    blocks = self.blocks

    # Reference: https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
    # Check if a block exists with the ascii value specified
    block: Block = filter(lambda block: int(
        block.block_number) == ascii_value - base, blocks)

    # Reference: https://stackoverflow.com/questions/68186924/how-do-i-check-if-a-filter-returns-no-results-in-python-3
    try:
      item: Block = next(block)

      # Try to get the index of the block if it exists
      item_index = self.blocks.index(item)

      # Remove that block from our blocks_list
      blocks.pop(item_index)

      # Update our original blocks list
      self.blocks = blocks
      
      # Update the player's current score
      self.score_calculator.score += item.point

    # If no block exists with the specified ascii value
    except StopIteration:
        print("No item exists")

  # Handle missed block
  def handle_missed_block(self, block):
    image = pygame.Surface(
        [self.game_manager.width, self.game_manager.height],
        pygame.SRCALPHA,
        32)

    block.sprite = image
    block.touching_ground = True

    return block

  # Decide if it is time
  # to spawn the next block
  def spawn_next_block(self, timer_info, spawned_blocks: int, total_blocks: int) -> bool:
    start_timer = timer_info["start_time"]
    current_timer = timer_info["current_time"]
    delay_timer = timer_info["delay_time"]

    has_timer_expired = self.game_manager.has_timer_expired(
        start_timer,
        current_timer,
        delay_timer)

    has_count_reached = self.block_count_reached(spawned_blocks, total_blocks)

    return has_timer_expired and not has_count_reached

  def block_count_reached(self, spawned_blocks: int, total_blocks: int) -> bool:
    return True if spawned_blocks == total_blocks else False

  def can_block_move(self, block: Block) -> bool:
    return block.y_pos < self.block_y_limit

  def is_touching_ground(self, block: Block) -> bool:
    return block.y_pos >= self.block_y_limit
