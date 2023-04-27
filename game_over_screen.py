import pygame
# from score_calculator import ScoreCalculator
# from leaderboard import Leaderboard

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
        # Need to write logic to get the exact score of player after game over
        player_score = 20
        name = ''
        input_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 32)
        input_text = input_font.render("Enter your name:", True, (0, 0, 0))
        input_rect = input_text.get_rect(center=(self.game_manager.screen.get_width() // 2, 300))

        # Create the Quit and Restart buttons
         # Assign button positions
        button_padding = 10
        quit_button_x = self.game_manager.screen.get_width() - 200 - button_padding
        restart_button_x = 50 + button_padding
        button_y = self.game_manager.screen.get_height() - 250 - button_padding

        # Add Quit button in bottom right corner
        quit_button = Button(self.game_manager.screen,
                            "Quit",
                            quit_button_x,
                            button_y)
                
        # Add Restart button in bottom left corner
        restart_button = Button(self.game_manager.screen,
                                "Restart",
                                restart_button_x,
                                button_y)
        
        while not self.game_manager.game_over:
            for event in pygame.event.get():
                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True
                # If the player types a key
                elif event.type == pygame.KEYDOWN:
                    # If the key is a letter, add it to the name
                    if event.unicode.isalpha():
                        name += event.unicode
                    # If the key is the backspace key, remove the last letter from the name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    # If the key is the enter key, store the name and go back to the main menu
                    elif event.key == pygame.K_RETURN:
                        self.game_manager.player_name = name
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
                score_text = score_font.render(f"Score: {player_score}", True, (0, 0, 0))
                score_rect = score_text.get_rect(center=(self.game_manager.screen.get_width() // 2, 200))
                self.game_manager.screen.blit(score_text, score_rect)

                # Render input text and name on the screen
                self.game_manager.screen.blit(input_text, input_rect)
                name_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 32)
                name_text = name_font.render(name, True, (0, 0, 0))
                name_rect = name_text.get_rect(center=(self.game_manager.screen.get_width() // 2, 350))
                self.game_manager.screen.blit(name_text, name_rect)
                
                # Add the name and score to highscores.json file
                # leaderboard = Leaderboard(game_manager)
                # leaderboard.add_score(name, player_score) 


                # Draw the Quit and Restart buttons on the screen
                quit_button.draw()
                restart_button.draw()

                pygame.display.update()
                

