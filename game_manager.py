# This class manages the entire game including starting the game,
# delegating the various interactions to the appropriate classes
# and managing the overall game state.

import pygame

from level_manager import LevelManager

title = "Ascii Attack"

# TODO: Change this to a singleton
class GameManager:
    def __init__(self, level_manager: LevelManager) -> None:

        # Assign to self object
        self.__game_over = False
        self.__width = 1200
        self.__height = 700
        self.__screen = None
        self.__level_manager = level_manager

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
    def game_over(self):
        return self.__game_over
    
    @property
    def level_manager(self):
        return self.__level_manager

    # Allow game over attribute
    # to be changed through setter
    @game_over.setter
    def game_over(self, value: bool):
        self.__game_over = value

    def __setup(self):

        # Initialize pygame library
        pygame.init()

        # Create the game window
        screen = pygame.display.set_mode((self.width, self.height))
        
        # Modify game title
        pygame.display.set_caption(title)
        
        # Modify game icon
        icon = pygame.image.load('./assets/img/title_icon.png')
        pygame.display.set_icon(icon)
        
        
        # Store a reference to the game screen
        # to access it later
        self.__screen = screen;

    # Start main game loop
    def start(self):
        while not self.game_over:
            
            # Change background color
            self.__screen.fill((0, 0, 0))
            
            # TODO : Move to an event manager class ??
            # Get a list of events happening within the game window
            events = pygame.event.get()
            
            # Check if close button on toolbar was clicked
            for event in events:
                if event.type == pygame.QUIT:
                    self.__game_over = True
            

    # End the game
    def end(self):
        pass
    
    # Close the game window when the 
    # player presses the close button
