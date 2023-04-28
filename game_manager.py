# This class manages the entire game including starting the game,
# delegating the various interactions to the appropriate classes
# and managing the overall game state.

import pygame

from singleton import Singleton

from level_manager import LevelManager
from ui_manager import UIManager
from block_manager import BlockManager

from view_rules import ViewRules
from welcome_screen import WelcomeScreen
from game_over_screen import GameOverScreen
from leaderboard import Leaderboard


class GameManager(metaclass=Singleton):
    def __init__(self) -> None:

        # Assign to self object
        self.__game_over = False
        self.__game_started = False

        self.__width = 1024
        self.__height = 768
        self.__title = "Ascii Attack"

        self.__screen = None

        # Store references to other class
        # instances for easy access
        self.__level_manager = None
        self.__ui_manager = None
        self.__block_manager = None
        self.__welcome_screen = None

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
    def block_manager(self):
        return self.__block_manager

    @property
    def title(self):
        return self.__title

    @property
    def welcome_screen(self):
        return self.__welcome_screen

    # Allow game over attribute
    # to be changed through setter
    @game_over.setter
    def game_over(self, value: bool):
        self.__game_over = value
        self.handle_quit_game()

    @game_started.setter
    def game_started(self, value: bool):
        self.__game_started = value

    @level_manager.setter
    def level_manager(self, value: LevelManager):
        self.__level_manager = value

    @ui_manager.setter
    def ui_manager(self, value: UIManager):
        self.__ui_manager = value

    @block_manager.setter
    def block_manager(self, value: BlockManager):
        self.__block_manager = value

    @welcome_screen.setter
    def welcome_screen(self, value: WelcomeScreen):
        self.__welcome_screen = value

    def __setup(self):

        # Initialize pygame library
        pygame.init()

        # Initialize the required classes
        self.block_manager = BlockManager(self)
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self)

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
        delay_timer = 3000

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

                self.welcome_screen = welcome_screen

            self.update_display()

    def show_loading_screen(self, msg: str = ""):

        # Change background color
        self.screen.fill((11, 36, 71))

        # Set Title Text and position
        title_font = pygame.font.Font('./assets/fonts/SuperMario256.ttf', 96)
        self.ui_manager.render_font(
            title_font, 150, 260, self.title.upper(), (255, 201, 60))

        # Set Loading Text and position
        loader_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 32)
        
        self.ui_manager.render_font(
            loader_font, 360, 380, "Loading " + msg + " ...")

    def handle_game_start(self, start_timer: int, value: bool, msg: str = ""):
        self.game_started = value if self.level_manager.level_number == 0 else self.game_started

        # TODO: Refactor delay to a method
        # Time to delay in milliseconds
        delay_timer = 4000
        delay_done = False

        # Check if the start button has been clicked
        if self.game_started:
            self.show_loading_screen(msg)

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

            # Load the level
            self.level_manager.load_level()

            # If a level was cleared
            if self.level_manager.level_cleared:

                # If the level number has not reached the max
                # levels in the game, load the next level.
                if self.level_manager.level_number != self.level_manager.max_levels:
                    self.level_manager.level_cleared = False

                    start_timer = pygame.time.get_ticks()
                    level_number = self.level_manager.level_number + 1
                    
                    self.handle_game_start(
                        start_timer, True, "Level " + str(level_number))
                else:
                    print("Max level reached")
                    game_over = GameOverScreen(self, self.ui_manager, "Game Completed!!!")
                    game_over.load_game_over_ui()

    def handle_quit_game(self):
        pygame.quit()

    def handle_view_rules(self):
        # Load the view rules page
        rules = ViewRules(self)
        rules.setup_view_rules_ui()

    def handle_view_leaderboard(self):
        # Load the view rules page
        leaderboard = Leaderboard(self)
        leaderboard.setup_view_leaderboard_ui()

    def has_timer_expired(self, start, current, delay) -> bool:
        return current - start >= delay

    def update_display(self):
        if not self.game_over:
            # Update the display continuously
            pygame.display.update()
