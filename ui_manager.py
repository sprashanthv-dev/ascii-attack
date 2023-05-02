import pygame

from singleton import Singleton
from block import Block
from destroy_block import DestroyBlock
from handle_commands import HandleCommands
from score_calculator import ScoreCalculator

# The UIManager class is responsible for all the UI elements 
# within the game such as rendering the various screens and 
# handling user interactions on these elements.
class UIManager(metaclass=Singleton):
  
  def __init__(self, game_manager):
    self.__game_manager = game_manager
    self.__missed_count = 0
    self.__current_misses = 0
    self.__current_score = 0
    
  @property
  def game_manager(self):
    return self.__game_manager
  
  @property
  def missed_count(self):
    return self.__missed_count
  
  @missed_count.setter
  def missed_count(self, value: int):
    self.__missed_count = value
    
  @property
  def current_misses(self):
    return self.__current_misses
  
  @current_misses.setter
  def current_misses(self, value: int):
    self.__current_misses = value
    
  @property
  def current_score(self):
    return self.__current_score
  
  @current_score.setter
  def current_score(self, value: int):
    self.__current_score = value
      
  # Returns the button placement configuration
  # on the welcome screen of the game.
  def get_welcome_screen_button_params(self, width: int, height: int):

    button_params = {
        "spacing": 80,
        "width": 200,
        "height": 50,
    }

    button_params["x"] = (width / 2) - (button_params["width"] / 2)
    button_params["y"] = (height / 2) - (button_params["height"] / 2)

    return button_params

  # A generic method that takes the specified font, text and (x,y) 
  # coordinates and renders it on the game screen.
  def render_font(self, font: pygame.font.Font, x_coord: int, y_coord: int, text: str, color = (255,255,255)):
    
    if not self.game_manager.game_over:
      font_properties = font.render(text, True, color)
      
      # Render the text on the screen
      self.game_manager.screen.blit(font_properties, (x_coord, y_coord))
    
  # Used to display paragraphs of text within the game
  def render_paragraph(self, text, font, rect, surface, color):
        # Split text into lines
        lines = text.split("\n")
        
        # Create a list to hold the rendered line surfaces
        line_surfaces = []
        
        # Render each line of text and add the surface to the list
        for line in lines:
            line_surface = font.render(line, True, color)
            line_surfaces.append(line_surface)
        
        # Calculate the height of each line surface
        line_height = font.size("Tg")[1]
        
        # Calculate the total height of the rendered paragraph
        total_height = line_height * len(lines)
        
        # Calculate the y-coordinate for the top left corner of the first line surface
        y = rect.top + (rect.height - total_height) // 2
        
        # Render each line surface onto the given surface at the appropriate y-coordinate
        for line_surface in line_surfaces:
            surface.blit(line_surface, (rect.left, y))
            y += line_height
  
  # Paints the UI elements of the main game loop.
  def render_main_screen_ui(self, level_manager, block_manager):
    x_coord = block_manager.block_x_limit
    y_coord = block_manager.y_start
    y_offset = block_manager.offset
    
    font = level_manager.text_font
    
    # Display Level number
    level_number = level_manager.level_number
    self.render_font(font, x_coord, y_coord, "Level: " + str(level_number), (0,0,0))
    
    # Display Current Score
    current_score = ScoreCalculator().score
    y_pos = y_coord + y_offset
    self.render_font(font, x_coord, y_pos, "Score: " + str(current_score), (0,0,0))
    
    # Display Blocks Left
    y_pos = y_pos + y_offset
    blocks_left = level_manager.total_blocks - level_manager.spawned_blocks
    self.render_font(font, x_coord, y_pos, "Blocks Left: " + str(blocks_left), (0,0,0))
    
    # Display Allowed Misses
    y_pos = y_pos + y_offset
    misses_left = level_manager.misses_left
    self.render_font(font, x_coord, y_pos, "Misses Left: " + str(self.missed_count) + "/" + str(misses_left), (0,0,0))
    
    # Display High Score
    y_pos = y_pos + y_offset
    high_score = level_manager.high_score
    self.render_font(font, x_coord, y_pos, "High Score: " + str(high_score), (0,0,0))
    
    
  # Paints the created blocks on the screen
  def render_blocks(self, level_manager, block_manager):
    # Get allowed misses
    self.missed_count = level_manager.misses_left 
        
    if not self.game_manager.game_over:
    
      # Render each block on the screen
      for block in block_manager.blocks:
        self.game_manager.screen.blit(
            block.sprite,
            (block.x_pos, block.y_pos)
        )
            
        # Update block's y_coordinate so that
        # it moves down at a constant speed
        if block_manager.can_block_move(block) and self.current_misses < level_manager.misses_left:
          block.y_pos += block.speed
        else:
            
          # Remove the block from the game, if it is
          # touching the bottom of the game window
          if block_manager.is_touching_ground(block) and not block.touching_ground:
            
            # Denote that the block is touching 
            # the bottom of the game window
            block.touching_ground = True

            # Since the block is missed, remove it from the blocks list
            # by invoking the DestroyBlock() command class
            filtered_block = filter(lambda each_block: int(
                each_block.block_number) == int(block.block_number),
                block_manager.blocks)
            
            try:
              item: Block = next(filtered_block)
              command_handler = HandleCommands()
              command_handler.execute(DestroyBlock(item, self.game_manager, block_manager))
            
            # If no block exists with the specified ascii value
            except StopIteration:
              print("No item exists")
            
            # Play block missed sound
            level_manager.block_miss_sound.play()
            
            # Increment the current misses
            self.current_misses += 1       
            
            # Check game over condition
            # If the current misses is >= allowed misses
            if self.current_misses >= level_manager.misses_left:
              self.game_manager.game_over = True
    
    # Update blocks_left count on the ui
    blocks_left = level_manager.total_blocks - level_manager.spawned_blocks
    level_manager.blocks_left = blocks_left 
        
    # Update the missed count
    self.missed_count -= self.current_misses
    self.render_main_screen_ui(level_manager, block_manager)   
    
  # Draw a rectangle on the game screen
  def draw_rect(self,
                game_surface: pygame.surface.Surface,
                title_surface: pygame.surface.Surface,
                height: int) -> None:
    width = game_surface.get_width() // 2
    title_rect = title_surface.get_rect(center=(width, height))
    game_surface.blit(title_surface, title_rect)
