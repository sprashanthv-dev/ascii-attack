from block import Block

import random
import pygame


class NumberBlock(Block):
  def __init__(self, block_number: int, block_config, level_manager) -> None:
    super().__init__()
    self.__block_number = block_number
    self.__block_config = block_config
    self.__level_manager = level_manager

  @property
  def block_number(self):
    return self.__block_number

  @property
  def block_config(self):
    return self.__block_config
  
  @property
  def level_manager(self):
    return self.__level_manager

  def create_block(self):
    block = Block()

    x_limit = self.block_config["x_limit"]
    y_limit = self.block_config["y_limit"]

    x_start = self.block_config["x_start"]
    y_start = self.block_config["y_start"]
    y_speed = self.block_config["y_speed"]
    speed_multiplier = self.block_config["speed_multiplier"]

    sprite_path = './assets/img/blocks/' + str(self.block_number) + '.png'
    block.sprite = pygame.image.load(sprite_path)

    block.x_pos = random.randint(x_start, x_limit)
    block.y_pos = random.randint(y_start, y_limit)
    
    block.speed = (self.level_manager.level_number * speed_multiplier) + y_speed
    block.point = 2
    block.block_number = str(self.block_number)

    return block
