from block_factory import BlockFactory
from block import Block
from number_block import NumberBlock

"""Factory that aims to provide a number block"""


class NumberBlockFactory(BlockFactory):
  def __init__(self, block_number: int, level_manager) -> None:
    super().__init__()
    self.__block_number = block_number
    self.__block_config = super().block_config
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

  def create_block(self) -> Block:
    number_block = NumberBlock(self.block_number, self.block_config, self.level_manager)
    return number_block.create_block()
