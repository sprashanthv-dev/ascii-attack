import pygame

from ui_manager import UIManager
from welcome_screen import WelcomeScreen
from button import Button

class ViewRules:
  def __init__(self, game_manager):
    self.__game_manager = game_manager
    self.__ui_manager = UIManager()
    
  @property
  def game_manager(self):
    return self.__game_manager
  
  @property
  def ui_manager(self):
    return self.__ui_manager
  
  def setup_view_rules_ui(self):
    
      # Check if back_button was clicked
      back_button_clicked = False
    
      # Load instructions text from file
      instructions_text = self.load_instructions()

      # Assign button position
      button_padding = 10
      button_x = self.game_manager.screen.get_width() - 200 - button_padding
      button_y = self.game_manager.screen.get_height() - 50 - button_padding

      # Add Back button in bottom right corner
      back_button = Button(self.game_manager.screen,
                           "Back",
                           button_x,
                           button_y)

      while not self.game_manager.game_over:

          for event in pygame.event.get():

            # If the player clicks on cross icon in toolbar
            # Or if the player clicks on the quit button
            if event.type == pygame.QUIT:
                self.game_manager.game_over = True

            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.is_clicked(event):
                # Handle "Back" button click by returning to Welcome Screen
                welcome_screen = self.game_manager.welcome_screen
                back_button_clicked = True
           
                # TODO: Activate screen once navigated
                welcome_screen.draw()
                welcome_screen.handle_interactions()

            if not self.game_manager.game_over and not back_button_clicked:
              # Change background color
              self.game_manager.screen.fill((255, 255, 255))

              self.draw_box(instructions_text)

              # Render "Back" button on the screen
              back_button.draw()

          if not self.game_manager.game_over:
            pygame.display.update()

  def load_instructions(self):
      with open("./assets/text_files/instructions.txt") as f:
          instructions_text = f.read()

      # Replace escape sequences with their corresponding characters
      instructions_text = instructions_text.replace('\\n', '\n')

      return instructions_text

  def draw_box(self, instructions: str):
      # Calculate the position of the box
      box_width = 850
      box_height = 500
      box_x = (self.game_manager.screen.get_width() - box_width) // 2
      box_y = (self.game_manager.screen.get_height() - box_height) // 2

      # Display "Instructions" title
      title_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 72)
      self.ui_manager.render_font(
          title_font, box_x + 50, box_y - 80, "Instructions", (255, 201, 60))

      # Create a surface for the instructions box
      box_surface = pygame.Surface((box_width, box_height))
      box_surface.set_alpha(200)  # Set the surface transparency
      box_surface.fill((150, 150, 150))  # Set the surface color

      self.render_instructions_paragraph(box_width,
                                         box_height,
                                         box_surface,
                                         instructions)

      # Blit the box surface onto the screen
      self.game_manager.screen.blit(box_surface, (box_x, box_y))

  def render_instructions_paragraph(self,
                                    width: int,
                                    height: int,
                                    surface: pygame.surface.Surface,
                                    instructions: str):
      # Render the instructions paragraph on the box surface
      paragraph_font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 12)
      paragraph_text = instructions
      paragraph_rect = pygame.Rect(50, 50, width - 100, height - 100)

      self.ui_manager.render_paragraph(
          paragraph_text, paragraph_font, paragraph_rect, surface, (255, 255, 255))
