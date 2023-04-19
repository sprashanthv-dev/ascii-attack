import pygame
import random

from singleton import Singleton
from block import Block
class BlockManager(metaclass=Singleton):
  def __init__(self):
    self.__block = None
    self.__blocks = []
    
  @property
  def block(self):
    return self.__block
  
  @property
  def blocks(self):
    return self.__blocks
  
  @block.setter
  def block(self, value: Block):
    self.__block = value
    
  # Create a block and return it
  def create_block(self) -> Block:
    block = Block()
    
    # TODO: Change this based on current level number
    x_limit = 736
    y_limit = 100
    y_speed = 0.03
    
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