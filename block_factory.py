from abc import ABC, abstractmethod

from block import Block

# Basic representation of a block creator


class BlockFactory(ABC):

  @property
  @abstractmethod
  def block_number(self):
    pass

  @property
  @abstractmethod
  def block_config(self):
    # TODO: Change this based on current level number
    return {
        "x_limit": 736,
        "y_limit": 100,
        "y_speed": 0.09,
        "x_start": 0,
        "y_start": 70
    }

  @abstractmethod
  def create_block(self, block_number: int) -> Block:
    """Returns either a letter based block or a number based block."""
