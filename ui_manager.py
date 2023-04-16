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

  def render_font(self, font: pygame.font.Font, x_coord: int, y_coord: int, text: str):
    font_properties = font.render(text, True, (255, 255, 255))

    # Render title on the screen
    self.game_manager.screen.blit(font_properties, (x_coord, y_coord))
