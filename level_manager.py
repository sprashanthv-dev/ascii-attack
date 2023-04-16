import pygame

from singleton import Singleton
from ui_manager import UIManager

# TODO: Notify classes using game_over property when it is updated
# TODO : Check circular import issue with GameManager
class LevelManager(metaclass=Singleton):
    def __init__(self, game_manager):
        self.__level_number = 0
        self.__blocks_left = 0
        self.__misses_left = 0
        self.__text_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 32)
        
        self.__ui_manager = UIManager(game_manager)
        self.__game_manager = game_manager
        
    @property
    def level_number(self):
        return self.__level_number
    
    @property
    def blocks_left(self):
        return self.__blocks_left
    
    @property
    def misses_left(self):
        return self.__misses_left
    
    @property
    def text_font(self):
        return self.__text_font
    
    @property
    def ui_manager(self):
        return self.__ui_manager
    
    @property
    def game_manager(self):
        return self.__game_manager
    
    @level_number.setter
    def level_number(self, value: int):
        self.__level_number = value
        
    @blocks_left.setter
    def blocks_left(self, value: int):
        self.__blocks_left = value
        
    @misses_left.setter
    def misses_left(self, value: int):
        self.__misses_left = value

    def load_level(self):
        # Placeholder for loading level logic  
        self.level_number += 1
        self.setup_level_ui()

    def setup_level_ui(self):
        while not self.game_manager.game_over:
            
            for event in pygame.event.get():
            
                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True
                    
            if not self.game_manager.game_over:
                # Change background color
                self.game_manager.screen.fill((0, 0, 0))

                # Display Level number
                self.ui_manager.render_font(self.text_font, 860, 50, "Level: " + str(self.level_number))
                
                # Update the display
                pygame.display.update()
        
    def handle_key_stroke(self):
        # Placeholder for handling key stroke logic
        pass

    def handle_missed_block(self):
        # Placeholder for handling missed block logic
        pass