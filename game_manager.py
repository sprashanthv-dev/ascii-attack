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
from score_calculator import ScoreCalculator

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
        self.__score_calculator = None
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
    def score_calculator(self):
        return self.__score_calculator
    
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
        
    @score_calculator.setter
    def score_calculator(self, value: ScoreCalculator):
        self.__score_calculator = value
        
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
        self.score_calculator = ScoreCalculator()
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

            self.update_display()

    def show_loading_screen(self):

        # Change background color
        self.screen.fill((11, 36, 71))
        
        # Set Title Text and position
        title_font = pygame.font.Font('./assets/fonts/SuperMario256.ttf', 96)
        self.ui_manager.render_font(title_font, 150, 260, self.title.upper(), (255, 201, 60))

        # Set Loading Text and position
        loader_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 32)
        self.ui_manager.render_font(loader_font, 420, 380, "Loading ...")

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

            # Load the level
            self.level_manager.load_level()

    def handle_quit_game(self):
        pygame.quit()
        
    def handle_view_rules(self):
        # Load the view rules page
        rules = ViewRules(self)
        rules.setup_view_rules_ui()
        
    def has_timer_expired(self, start, current, delay) -> bool:
        return current - start >= delay
        
    def update_display(self):
        if not self.game_over:
            # Update the display continuously
            pygame.display.update()
