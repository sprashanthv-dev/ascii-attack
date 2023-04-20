import pygame

from singleton import Singleton
# TODO: Check circular import issue with Game Manager
class UIManager(metaclass=Singleton):
  
  def __init__(self, game_manager):
    self.__game_manager = game_manager
    
  @property
  def game_manager(self):
    return self.__game_manager
  
  def get_welcome_screen_button_params(self, width: int, height: int):

    button_params = {
        "spacing": 80,
        "width": 200,
        "height": 50,
    }

    button_params["x"] = (width / 2) - (button_params["width"] / 2)
    button_params["y"] = (height / 2) - (button_params["height"] / 2)

    return button_params

  def render_font(self, font: pygame.font.Font, x_coord: int, y_coord: int, text: str, color = (255,255,255)):
    font_properties = font.render(text, True, color)

    # Render title on the screen
    self.game_manager.screen.blit(font_properties, (x_coord, y_coord))
    
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
  
  def render_main_screen_ui(self, level_manager, block_manager):
    x_coord = block_manager.block_x_limit
    y_coord = block_manager.y_start
    y_offset = block_manager.offset
    
    font = level_manager.text_font
    
    # Display Level number
    level_number = level_manager.level_number
    self.render_font(font, x_coord, y_coord, "Level: " + str(level_number))
    
    # Display Current Score
    current_score = level_manager.score_calculator.score
    y_pos = y_coord + y_offset
    self.render_font(font, x_coord, y_pos, "Score: " + str(current_score))
    
    # Display Blocks Left
    y_pos = y_pos + y_offset
    blocks_left = level_manager.total_blocks - level_manager.spawned_blocks
    self.render_font(font, x_coord, y_pos, "Blocks Left: " + str(blocks_left))
    
    # Display Allowed Misses
    y_pos = y_pos + y_offset
    misses_left = level_manager.misses_left
    self.render_font(font, x_coord, y_pos, "Misses Left: " + str(misses_left))
    
    # Display High Score
    y_pos = y_pos + y_offset
    high_score = level_manager.high_score
    self.render_font(font, x_coord, y_pos, "High Score: " + str(high_score))
    
    
  def render_blocks(self, level_manager, block_manager):
    font = level_manager.text_font
    
    block_x = block_manager.block_x_limit
    y_start = block_manager.y_start
    y_offset = block_manager.offset
    
    # Render each block on the screen
    for block in block_manager.blocks:
      self.game_manager.screen.blit(
          block.sprite,
          (block.x_pos, block.y_pos)
      )

      # Update block's y_coordinate so that
      # it moves down at a constant speed
      if block_manager.can_block_move(block):
        block.y_pos += block.speed
      else:
        # Reference: https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame
        # Remove the block from the game, if it is touching 
        # the bottom of the game window
        if block_manager.is_touching_ground(block):
          image = pygame.Surface(
            [self.game_manager.width, self.game_manager.height], 
            pygame.SRCALPHA, 
            32)
        
          block.sprite = image
          misses_left = level_manager.misses_left - 1
          
          level_manager.misses_left = misses_left
          
          # Update misses left count on the ui
          self.render_font(font, block_x, ((y_offset * 3) + y_start), "Misses Left: " + str(misses_left))
        
    # Update blocks_left count on the ui
    blocks_left = level_manager.total_blocks - level_manager.spawned_blocks
    level_manager.blocks_left = blocks_left
    self.render_font(font, block_x, ((y_offset * 2) + y_start), "Blocks Left: " + str(blocks_left))