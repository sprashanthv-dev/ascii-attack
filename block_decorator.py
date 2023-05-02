from block import Block

# The BlockDecorator class is the base decorator class.
# It inherits from Block class and decorates it with
# additional number of hits during run time. We see
# the usage of the decorator pattern through this.
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
