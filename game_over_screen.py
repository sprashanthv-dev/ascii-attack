import pygame
from score_calculator import ScoreCalculator

from button import Button

class GameOverScreen:
    def __init__(self, game_manager, ui_manager):
        self.__game_manager = game_manager
        self.__ui_manager = ui_manager
        
    @property
    def game_manager(self):
        return self.__game_manager
    
    @property
    def ui_manager(self):
        return self.__ui_manager
    
    def load_game_over_ui(self):
        while not self.game_manager.game_over:
            for event in pygame.event.get():
                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True

            if not self.game_manager.game_over:
                # Change background color
                self.game_manager.screen.fill((255, 255, 255))

                # Render "Game Over" text on the screen
                title_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 72)
                title_text = title_font.render("Game Over", True, (255, 0, 0))
                title_rect = title_text.get_rect(center=(self.game_manager.screen.get_width() // 2, 100))
                self.game_manager.screen.blit(title_text, title_rect)

                # Render current score below the "Game Over" text
                score_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 48)
                score_text = score_font.render(f"Score: {self.ui_manager.current_score}", True, (0, 0, 0))
                score_rect = score_text.get_rect(center=(self.game_manager.screen.get_width() // 2, 200))
                self.game_manager.screen.blit(score_text, score_rect)

                pygame.display.update()
                
                

                
              

