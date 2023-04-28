
from block import Block
from command import Command

class DestroyBlock(Command):
  def __init__(self, block: Block, game_manager, block_manager) -> None:
    self.block = block
    self.game_manager = game_manager
    self.block_manager = block_manager

  def execute(self) -> None:
    print("Inside execute of destroy block")

    blocks = self.block_manager.blocks

    # Try to get the index of the block if it exists
    item_index = blocks.index(self.block)

    # Remove that block from our blocks_list
    blocks.pop(item_index)

    # Update our original blocks list
    self.block_manager.blocks = blocks
