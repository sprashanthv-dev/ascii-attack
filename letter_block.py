from block import Block

import random
import pygame


class LetterBlock(Block):
  def __init__(self, block_number: int, block_config) -> None:
    super().__init__()
    self.__block_number = block_number
    self.__block_config = block_config

  @property
  def block_number(self):
    return self.__block_number

  @property
  def block_config(self):
    return self.__block_config

  def create_block(self):
    block = Block()

    x_limit = self.block_config["x_limit"]
    y_limit = self.block_config["y_limit"]

    x_start = self.block_config["x_start"]
    y_start = self.block_config["y_start"]
    y_speed = self.block_config["y_speed"]

    sprite_path = './assets/img/blocks/' + str(self.block_number) + '.png'
    block.sprite = pygame.image.load(sprite_path)

    block.x_pos = random.randint(x_start, x_limit)
    block.y_pos = random.randint(y_start, y_limit)
    block.speed = y_speed

    return block
