import pygame

from singleton import Singleton

from level_manager import LevelManager
from ui_manager import UIManager
from block_manager import BlockManager

from view_rules import ViewRules
from welcome_screen import WelcomeScreen
from game_over_screen import GameOverScreen
from leaderboard import Leaderboard
from score_calculator import ScoreCalculator


# The GameManager class controls the entire game including starting 
# the game,delegating the various interactions to the appropriate 
# classes and managing the overall game state.
class GameManager(metaclass=Singleton):
    def __init__(self) -> None:

        # Assign to self object
        self.__game_over = False
        self.__game_started = False
        self.__quit_game = False
        self.__level_loaded = False

        # Define the game window attributes
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
    def level_loaded(self):
        return self.__level_loaded

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


    # Allow game over attribute to be changed through setter
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
        
    @level_loaded.setter
    def level_loaded(self, value: bool):
        self.__level_loaded = value

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
       
    # Perform the necessary initialization steps 
    def __setup(self):

        # Initialize pygame library
        pygame.init()

        # Initialize the required classes
        self.block_manager = BlockManager(self)
        self.level_manager = LevelManager(self)
        self.ui_manager = UIManager(self)

        # Create the game window
        screen = self.init_game_window()

        # Store a reference to the game 
        # screen to access it later
        self.__screen = screen

    # Start main game loop
    def start(self):

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 3000

        # While game is not over and quit icon is not pressed
        while not self.game_over and not self.quit_game:

            # Show the loading screen
            self.show_loading_screen()

            # Get a list of events happening within the game window
            events = pygame.event.get()

            # Check if close button on toolbar was clicked
            for event in events:
                # Close the game window when the
                # player presses the close button
                if event.type == pygame.QUIT:
                    self.quit_game = True

            # Get the time elapsed in milliseconds
            # since the start of the game
            current_time = pygame.time.get_ticks()

            # Reference : https://stackoverflow.com/questions/
            # 18839039/how-to-wait-some-time-in-pygame
            # If the specified amount of delay time has expired
            if current_time - start_timer >= delay_timer:
                # Load the welcome screen
                welcome_screen = WelcomeScreen(self)

                welcome_screen.draw()
                welcome_screen.handle_interactions()

                self.welcome_screen = welcome_screen

            # Update the game loop's display
            self.update_display()
         
        # If game is over and the quit icon is not pressed
        if not self.quit_game:   
                
            # Initialize the game over screen        
            game_over = GameOverScreen(self, self.ui_manager, "Game Over") if\
                self.game_over_ref is None else self.game_over_ref
            
            if self.game_over_ref is None:
                self.game_over_ref = game_over
                
            self.game_over_ref.load_game_over_ui()
            
            # Add to leaderboard if name was 
            # entered and then quit was pressed
            if len(self.game_over_ref.name) > 0 and\
                not self.game_over_ref.is_input_entered:
                print("Name entered and quit button pressed")
                print("Adding to leaderboard .....")
                
                # Add the current player's score to the leaderboard
                leaderboard = Leaderboard(self)
                leaderboard.add_score(self.game_over_ref.name, self.game_over_ref.player_score)
        
    # Creates the game window
    def init_game_window(self) -> pygame.surface.Surface:
        
        # Create the game window
        screen = pygame.display.set_mode((self.width, self.height))

        # Modify game title
        pygame.display.set_caption(self.__title)

        # Modify game icon
        icon = pygame.image.load('./assets/img/title_icon.png')
        pygame.display.set_icon(icon)
        
        return screen

    # Shows the loading screen
    def show_loading_screen(self, msg: str = ""):

        # Change background color
        self.screen.fill((11, 36, 71))

        # Set Title Text and position
        title_font = pygame.font.Font('./assets/fonts/SuperMario256.ttf', 96)
        self.ui_manager.render_font(
            title_font, 150, 260, self.title.upper(), (255, 201, 60))

        # Set Loading Text and position
        loader_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 32)
        
        # Render the loading text on the screen
        self.ui_manager.render_font(
            loader_font, 360, 380, "Loading " + msg + " ...")

    # Handler function when the player clicks on New Game button
    def handle_game_start(self, start_timer: int, value: bool, msg: str = ""):
        self.game_started = value if self.level_manager.level_number == 0 else self.game_started

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
                    
                    # Increment the level number for the next level
                    level_number = self.level_manager.level_number + 1
                    
                    # Invoke the handler function again to load the 
                    # next level.
                    self.handle_game_start(
                        start_timer, True, "Level " + str(level_number))
                else:
                    # If the player has cleared all levels load
                    # the game over screen with a different message.
                    print("Max level reached")
                    game_over = GameOverScreen(self, self.ui_manager, "Game Completed!!!") if self.game_over_ref is None else self.game_over_ref
                    
                    if self.game_over_ref is None:
                        self.game_over_ref = game_over
                    
                    self.game_over_ref.load_game_over_ui()
           
    # This methods invokes the leaderboard add method
    # to save the current player score to our file.         
    def add_to_leaderboard(self):
        if len(self.game_over_ref.name) > 0:
            print(f"Name added: {self.game_over_ref.name} with score : {self.game_over_ref.player_score}")
            leaderboard = Leaderboard(self)
            leaderboard.add_score(self.game_over_ref.name, self.game_over_ref.player_score)

    # Handles Quit game functionality
    def handle_quit_game(self):
        if self.quit_game:
            pygame.quit()

    # Loads the view rules page
    def handle_view_rules(self):
        rules = ViewRules(self)
        rules.setup_view_rules_ui()

    # Loads the view rules page
    def handle_view_leaderboard(self):
        leaderboard = Leaderboard(self)
        leaderboard.setup_view_leaderboard_ui()

    # Returns True if the specified amount of delay
    # has expired since start, False otherwise.
    def has_timer_expired(self, start, current, delay) -> bool:
        return current - start >= delay

    # Updates the game display
    def update_display(self):
        if not self.game_over and not self.quit_game:
            # Update the display continuously
            pygame.display.update()
         
    # Handler for restart functionality   
    def restart_game(self):
        # Reset the level number
        self.level_manager.level_number = 0
        
        # Indicate that the game is not over
        self.game_over = False
        
        # Indicate that a level has not been loaded
        self.level_loaded = False
        
        # Reset player score
        score_calc = ScoreCalculator()
        score_calc.score = 0
                
        # Restart the game by invoking the handler function
        start_timer = pygame.time.get_ticks()   
        level_number = self.level_manager.level_number + 1
        self.handle_game_start(start_timer, True, "Level " + str(level_number))
        
        # Once the game is over after restart, update the score
        # to be displayed in the game over screen.
        self.game_over_ref.player_score = ScoreCalculator().score
        self.game_over_ref.name = ''
        self.game_over_ref.is_input_entered = False