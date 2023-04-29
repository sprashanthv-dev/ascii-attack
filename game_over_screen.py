import pygame
from score_calculator import ScoreCalculator
# from leaderboard import Leaderboard

from button import Button


class GameOverScreen:
    def __init__(self, game_manager, ui_manager, title_text: str):
        pygame.init()

        self.__game_manager = game_manager
        self.__ui_manager = ui_manager
        self.__title_text = title_text
        self.__game_over_active = True
        self.__screen = None

        self.__title_font = pygame.font.Font(
            "./assets/fonts/SuperMario256.ttf", 72)
        self.__text_font = pygame.font.Font(
            "./assets/fonts/SuperMario256.ttf", 32)
        
        self.__button_padding = 10

        self.__player_score = ScoreCalculator().score

    @property
    def game_manager(self):
        return self.__game_manager

    @property
    def ui_manager(self):
        return self.__ui_manager
    
    @property
    def screen(self):
        return self.__screen

    @property
    def title_font(self):
        return self.__title_font

    @property
    def text_font(self):
        return self.__text_font

    @property
    def title_text(self):
        return self.__title_text

    @property
    def player_score(self):
        return self.__player_score
    
    @property
    def button_padding(self):
        return self.__button_padding

    @property
    def game_over_active(self):
        return self.__game_over_active

    @screen.setter
    def screen(self, screen: pygame.surface.Surface):
        self.__screen = screen

    @game_over_active.setter
    def game_over_active(self, value: bool):
        self.__game_over_active = value
        self.handle_quit_game()

    def load_game_over_ui(self):
        width = self.game_manager.width
        height = self.game_manager.height
        
        self.screen = self.get_game_screen()

        # Need to write logic to get the exact score of player after game over
        name = ''
        input_text = self.text_font.render("Enter your name:", True, (0, 0, 0))
        input_rect = input_text.get_rect(center=(width // 2, 400))

        # Create the Quit and Restart buttons
        # Assign button positions
        button_y = height - 150 - self.button_padding
        
        quit_button_x = width - 200 - self.button_padding
        restart_button_x = 50 + self.button_padding

        # Add Quit button in bottom right corner
        quit_button = self.create_button("Quit", quit_button_x, button_y)

        # Add Restart button in bottom left corner
        restart_button = self.create_button("Restart", restart_button_x, button_y)

        while self.game_over_active:
            for event in pygame.event.get():
                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_over_active = False
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

            if self.game_over_active:
                self.screen.fill((255, 255, 255))
                # self.game_manager.screen.fill((255, 255, 255))

                # Render title text on the screen
                title_text_color = (
                    255, 0, 0) if self.title_text == "Game Over" else (83, 145, 101)

                title_text = self.title_font.render(
                    self.title_text, True, title_text_color)
                self.ui_manager.draw_rect(self.screen, title_text, 200)

                # Render current score below the title text
                score_text = self.text_font.render(
                    f"Score: {self.player_score}", True, (0, 0, 0))
                self.ui_manager.draw_rect(self.screen, score_text, 300)

                # Render input text and name on the screen
                self.screen.blit(input_text, input_rect)

                name_text = self.text_font.render(name, True, (0, 0, 0))
                self.ui_manager.draw_rect(self.screen, name_text, 450)
                
                # Add the name and score to highscores.json file
                # leaderboard = Leaderboard(game_manager)
                # leaderboard.add_score(name, player_score)

                # Draw the Quit and Restart buttons on the screen
                quit_button.draw()
                restart_button.draw()

                pygame.display.update()
                                
    def get_game_screen(self) -> pygame.surface.Surface:
        screen: pygame.surface.Surface
        
        if self.game_manager.game_over:
            screen = self.game_manager.init_game_window()
        else:
            screen = self.game_manager.screen
            
        return screen
    
    def create_button(self, text: str, x_coord: int, y_coord: int) -> Button:
        return Button(self.screen, text, x_coord, y_coord)
    
    def handle_quit_game(self):
        if not self.game_over_active:
            pygame.quit()
