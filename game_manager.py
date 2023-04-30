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
        self.__quit_game = False

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
        self.__game_over_ref = None
        self.__leaderboard = None

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
    def quit_game(self):
        return self.__quit_game

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
    def game_over_ref(self):
        return self.__game_over_ref

    @property
    def title(self):
        return self.__title

    @property
    def welcome_screen(self):
        return self.__welcome_screen
    
    @property
    def leaderboard(self):
        return self.__leaderboard


    # Allow game over attribute
    # to be changed through setter
    @game_over.setter
    def game_over(self, value: bool):
        self.__game_over = value

    @game_started.setter
    def game_started(self, value: bool):
        self.__game_started = value
        
    @quit_game.setter
    def quit_game(self, value: bool):
        self.__quit_game = value
        self.handle_quit_game()

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
        
    @game_over_ref.setter
    def game_over_ref(self, value: GameOverScreen):
        self.__game_over_ref = value

    @leaderboard.setter
    def leaderboard(self, value: Leaderboard):
        self.__leaderboard = value
        
    def __setup(self):

        # Initialize pygame library
        pygame.init()

        # Initialize the required classes
        self.block_manager = BlockManager(self)
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self)

        # Create the game window
        screen = self.init_game_window()

        # Store a reference to the game screen
        # to access it later
        self.__screen = screen

    # Start main game loop
    def start(self):

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 3000

        while not self.game_over and not self.quit_game:

            self.show_loading_screen()

            # TODO : Move to an event manager class ??
            # Get a list of events happening within the game window
            events = pygame.event.get()

            # Check if close button on toolbar was clicked
            for event in events:
                # Close the game window when the
                # player presses the close button
                if event.type == pygame.QUIT:
                    self.quit_game = True

            current_time = pygame.time.get_ticks()

            # Reference : https://stackoverflow.com/questions/
            # 18839039/how-to-wait-some-time-in-pygame
            if current_time - start_timer >= delay_timer:
                welcome_screen = WelcomeScreen(self)

                welcome_screen.draw()
                welcome_screen.handle_interactions()

                self.welcome_screen = welcome_screen

            self.update_display()
         
        if not self.quit_game:   
            game_over = GameOverScreen(self, self.ui_manager, "Game Over") if\
                self.game_over_ref is None else self.game_over_ref
            
            if self.game_over_ref is None:
                self.game_over_ref = game_over
                
            self.game_over_ref.load_game_over_ui()
            
            # Add to leaderboard if name was entered
            # and then quit was pressed
            if len(self.game_over_ref.name) > 0 and not self.game_over_ref.is_input_entered:
                # Add to leaderboard here
                print("Name entered and quit button pressed")
                print("Adding to leaderboard .....")
                leaderboard = Leaderboard(self)
                leaderboard.add_score(self.game_over_ref.name, self.game_over_ref.player_score)
        
    def init_game_window(self) -> pygame.surface.Surface:
        
        # Create the game window
        screen = pygame.display.set_mode((self.width, self.height))

        # Modify game title
        pygame.display.set_caption(self.__title)

        # Modify game icon
        icon = pygame.image.load('./assets/img/title_icon.png')
        pygame.display.set_icon(icon)
        
        return screen

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
                    game_over = GameOverScreen(self, self.ui_manager, "Game Completed!!!") if self.game_over_ref is None else self.game_over_ref
                    
                    if self.game_over_ref is None:
                        self.game_over_ref = game_over
                    
                    self.game_over_ref.load_game_over_ui()
                    
    def add_to_leaderboard(self):
        # Add to leaderboard here
        # game_manager - self, 
        # player score - self.game_over.player_score, 
        # player_name = self.game_over.name
        
        if len(self.game_over_ref.name) > 0:
            print("Inside add to leaderboard - game manager")
            print(f"Name added: {self.game_over_ref.name} with score : {self.game_over_ref.player_score}")
            leaderboard = Leaderboard(self)
            leaderboard.add_score(self.game_over_ref.name, self.game_over_ref.player_score)

    def handle_quit_game(self):
        if self.quit_game:
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
        if not self.game_over and not self.quit_game:
            # Update the display continuously
            pygame.display.update()
            
    def restart_game(self):
        # print("restarting game")
        self.level_manager.level_number = 0
        self.game_over = False
        #TODO: Reset game score
        start_timer = pygame.time.get_ticks()   
        level_number = self.level_manager.level_number + 1
        self.handle_game_start(start_timer, True, "Level " + str(level_number))