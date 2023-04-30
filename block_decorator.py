from block import Block


class BlockDecorator(Block):

  """
    Base class for decorators
  """

  def __init__(self, block: Block):
    self.__block = block

  @property
  def block(self):
    return self.__block

  def get_hits(self) -> Block:
    return self.block.get_hits()
