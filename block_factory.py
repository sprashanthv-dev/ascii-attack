from abc import ABC, abstractmethod

from block import Block

# The BlockFactory class provides a basic representation
# of a block creator demonstrating usage of the 
# Factory pattern
class BlockFactory(ABC):

  @property
  @abstractmethod
  def block_number(self):
    pass

  # Specify the config for each block
  @property
  @abstractmethod
  def block_config(self):
    return {
        "x_limit": 736,
        "y_limit": 100,
        "y_speed": 0.07,
        "x_start": 0,
        "y_start": 70,
        "speed_multiplier": 0.05
    }

  # This is the method that will be overridden
  # by the corressponding factory implementations
  # to create either a letter or number block
  @abstractmethod
  def create_block(self, block_number: int) -> Block:
    """Returns either a letter based block or a number based block."""
