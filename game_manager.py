# This class manages the entire game including starting the game,
# delegating the various interactions to the appropriate classes
# and managing the overall game state.

import pygame

from level_manager import LevelManager
from singleton import Singleton
from ui_manager import UIManager
from welcome_screen import WelcomeScreen

class GameManager(metaclass=Singleton):
    def __init__(self) -> None:

        # Assign to self object
        self.__game_over = False
        self.__game_started = False

        self.__width = 1024
        self.__height = 768
        self.__title = "Ascii Attack"

        self.__screen = None
        
        self.__level_manager = LevelManager()        
        self.__ui_manager = UIManager()

        self.__setup()
        self.start()

    # @property - create read-only attributes
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def screen(self):
        return self.__screen

    @property
    def game_started(self):
        return self.__game_started

    @property
    def game_over(self):
        return self.__game_over

    @property
    def level_manager(self):
        return self.__level_manager

    @property
    def ui_manager(self):
        return self.__ui_manager

    @property
    def title(self):
        return self.__title

    # Allow game over attribute
    # to be changed through setter
    @game_over.setter
    def game_over(self, value: bool):
        self.__game_over = value
        self.handle_quit_game()

    @game_started.setter
    def game_started(self, value: bool):
        self.__game_started = value

    def __setup(self):

        # Initialize pygame library
        pygame.init()

        # Add background music in loop
        self.play_background_music()

        # Create the game window
        screen = pygame.display.set_mode((self.width, self.height))

        # Modify game title
        pygame.display.set_caption(self.__title)

        # Modify game icon
        icon = pygame.image.load('./assets/img/title_icon.png')
        pygame.display.set_icon(icon)

        # Store a reference to the game screen
        # to access it later
        self.__screen = screen

    # Start main game loop
    def start(self):

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 4000

        while not self.game_over:

            self.show_loading_screen()

            # TODO : Move to an event manager class ??
            # Get a list of events happening within the game window
            events = pygame.event.get()

            # Check if close button on toolbar was clicked
            for event in events:
                # Close the game window when the
                # player presses the close button
                if event.type == pygame.QUIT:
                    self.game_over = True

            current_time = pygame.time.get_ticks()

            # Reference : https://stackoverflow.com/questions/
            # 18839039/how-to-wait-some-time-in-pygame
            if current_time - start_timer >= delay_timer:
                welcome_screen = WelcomeScreen(self)

                welcome_screen.draw()
                welcome_screen.handle_interactions()

            self.update_display()

    def show_loading_screen(self):

        # Change background color
        self.__screen.fill((11, 36, 71))

        # TODO : Refactor this to a method
        # Set Title Text and position
        title_font = pygame.font.Font('./assets/fonts/SuperMario256.ttf', 96)

        title_x = 150
        title_y = 260
        title_text = self.__title.upper()

        title = title_font.render(title_text, True, (255, 201, 60))

        # Render loading text on the screen
        self.__screen.blit(title, (title_x, title_y))

        # Set Loading Text and position
        loader_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 32)

        loader_x = 420
        loader_y = 380
        loader_text = "Loading ..."

        loader = loader_font.render(loader_text, True, (255, 255, 255))

        # Render title on the screen
        self.__screen.blit(loader, (loader_x, loader_y))

    def play_background_music(self):
        # Load the background music file
        pygame.mixer.music.load('./assets/sounds/in_game.mp3')

        # Set the volume of the background music
        pygame.mixer.music.set_volume(0.5)

        # Play the background music on loop
        pygame.mixer.music.play(-1)

    def handle_game_start(self, start_timer: int, value: bool):
        self.game_started = value

        # TODO: Refactor delay to a method
        # Time to delay in milliseconds
        delay_timer = 4000
        delay_done = False

        # Check if the start button has been clicked
        if self.game_started:
            self.show_loading_screen()

            # While the delay has not expired
            while not delay_done:
                current_timer = pygame.time.get_ticks()
                time_difference = current_timer - start_timer

                # Keep updating the display until 
                # the delay has not expired
                if time_difference <= delay_timer:
                    pygame.display.update()
                    
                # Once the delay has expired
                # end the while loop
                if time_difference > delay_timer:
                    delay_done = True

    def handle_quit_game(self):
        pygame.quit()

    def update_display(self):
        if not self.game_over:
            # Update the display continuously
            pygame.display.update()
