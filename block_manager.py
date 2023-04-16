from block import Block

class BlockManager:
  def __init__(self):
    self.__block = None
    
  @property
  def block(self):
    return self.__block
  
  @block.setter
  def block(self, value: Block):
    self.__block = value
    
  # Create a block and return it
  def create_block(self):
    pass
  
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