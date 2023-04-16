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
  