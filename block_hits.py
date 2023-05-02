from block_decorator import BlockDecorator
from block import Block

from constants import BLOCK_NO_HITS_MAP

# The BlockHits class is a specific decorator
# that inherits from the base BlockDecorator
# class. 
class BlockHits(BlockDecorator):
  def __init__(self, block: Block):
    super().__init__(block)
    self.__block = block
    
  @property
  def block(self):
    return self.__block
    
  # The get_hits method from the base decorator
  # class is overridden and decorated with
  # additional hits if the block is a special block.
  def get_hits(self) -> Block:
    
    hits_for_block: int = 0
    
    if self.block.block_number in BLOCK_NO_HITS_MAP:
      hits_for_block = BLOCK_NO_HITS_MAP[self.block.block_number]
          
    self.block.hits_left = self.block.hits_left + hits_for_block
    
    return self.block
  
  def __repr__(self):
      return f"{self.__class__.__name__} (\
          {self.sprite}, {self.block_number}, {self.x_pos}, {self.y_pos} \
          {self.speed}, {self.hits_left}, {self.point}\
          {self.touching_ground}, {self.special_block})"
