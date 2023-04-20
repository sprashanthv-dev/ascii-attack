import pygame
import random

from singleton import Singleton
from block import Block
class BlockManager(metaclass=Singleton):
  def __init__(self, game_manager):
    self.__block = None
    self.__game_manager = game_manager
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

  @block.setter
  def block(self, value: Block):
    self.__block = value

  # Create a block and return it
  def create_block(self) -> Block:
    block = Block()

    # TODO: Change this based on current level number
    x_limit = 736
    y_limit = 100
    y_speed = 0.5

    # TODO : Change the image path to include a
    # TODO: random number between 0 to 38 inclusive
    block.sprite = pygame.image.load('./assets/img/blocks/12.png')
    block.x_pos = random.randint(0, x_limit)
    block.y_pos = random.randint(70, y_limit)
    block.speed = y_speed

    self.blocks.append(block)

    return block

  # Spawns blocks at regular intervals

  def spawn_block(self):
    pass

  # Update the number of hits a
  # block has received
  def update_block_hits(self):
    pass

  # Destroy the block from the game
  def destroy_block(self):
    pass

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
  
  def can_block_move(self, block : Block) -> bool:
    return block.y_pos < self.block_y_limit
  
  def is_touching_ground(self, block: Block) -> bool:
    return block.y_pos >= self.block_y_limit