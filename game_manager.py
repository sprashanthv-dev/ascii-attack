# This class manages the entire game including starting the game,
# delegating the various interactions to the appropriate classes
# and managing the overall game state.

import pygame
import sys

from level_manager import LevelManager

# TODO: Change this to a singleton
class GameManager:
    def __init__(self, level_manager: LevelManager) -> None:

        # Assign to self object
        self.__game_over = False
        self.__width = 1024
        self.__height = 768
        self.__screen = None
        self.__level_manager = level_manager
        self.__title = "Ascii Attack"

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

        # Load the background music file
        pygame.mixer.music.load('./assets/sounds/in_game.mp3')

        # Set the volume of the background music
        pygame.mixer.music.set_volume(0.5)

        # Play the background music on loop
        pygame.mixer.music.play(-1)

        # Create the game window
        screen = pygame.display.set_mode((self.width, self.height))
        
        # Modify game title
        pygame.display.set_caption(self.__title)
        
        # Modify game icon
        icon = pygame.image.load('./assets/img/title_icon.png')
        pygame.display.set_icon(icon)
        
        # Store a reference to the game screen
        # to access it later
        self.__screen = screen;

    # Start main game loop
    def start(self):
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
                    self.__game_over = True
                    
            # Update the display continuously
            pygame.display.update();
                    
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
        
    # End the game
    def end(self):
        pass