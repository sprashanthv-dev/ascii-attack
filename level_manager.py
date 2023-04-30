import pygame
from pygame import mixer

from singleton import Singleton
from block_manager import BlockManager
from ui_manager import UIManager

# TODO: Notify classes using game_over property when it is updated
# TODO : Check circular import issue with GameManager


class LevelManager(metaclass=Singleton):
    def __init__(self, game_manager):
        self.__level_number = 0
        self.__level_cleared = False
        self.__is_bg_music_active = False
        
        # TODO: Reset back to 10 after testing
        self.__max_levels = 5

        # TODO: Get from game manager
        self.__high_score = 0

        self.__blocks_left = 0

        self.__misses_left = 3

        self.__text_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 20)
        self.__message_font = pygame.font.Font('./assets/fonts/SuperMario256.ttf', 64)
                
        self.__block_hit_sound = mixer.Sound('./assets/sounds/block_hit.mp3')
        self.__block_miss_sound = mixer.Sound('./assets/sounds/block_miss.wav')
        self.__level_complete_sound = mixer.Sound('./assets/sounds/level_complete.wav')

        self.__ui_manager = UIManager(game_manager)
        self.__game_manager = game_manager

        self.__total_blocks = 0
        self.__spawned_blocks = 0
        self.__block_multiplier = 5

        self.timer_info = {}

        self.__block_manager: BlockManager = self.game_manager.block_manager

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
    def high_score(self):
        return self.__high_score

    @property
    def text_font(self):
        return self.__text_font
    
    @property
    def message_font(self):
        return self.__message_font
    
    @property
    def is_bg_music_active(self):
        return self.__is_bg_music_active
     
    @property
    def block_hit_sound(self):
        return self.__block_hit_sound
    
    @property
    def block_miss_sound(self):
        return self.__block_miss_sound
    
    @property
    def level_complete_sound(self):
        return self.__level_complete_sound

    @property
    def total_blocks(self):
        return self.__total_blocks

    @property
    def spawned_blocks(self):
        return self.__spawned_blocks
    
    @property
    def level_cleared(self):
        return self.__level_cleared
    
    @property
    def max_levels(self):
        return self.__max_levels
    
    @property
    def block_multiplier(self):
        return self.__block_multiplier

    @property
    def ui_manager(self):
        return self.__ui_manager

    @property
    def game_manager(self):
        return self.__game_manager

    @property
    def block_manager(self):
        return self.__block_manager
    
    @is_bg_music_active.setter
    def is_bg_music_active(self, value: bool):
        self.__is_bg_music_active = value

    @level_number.setter
    def level_number(self, value: int):
        self.__level_number = value

    @blocks_left.setter
    def blocks_left(self, value: int):
        self.__blocks_left = value

    @misses_left.setter
    def misses_left(self, value: int):
        self.__misses_left = value

    @total_blocks.setter
    def total_blocks(self, value: int):
        self.__total_blocks = value

    @spawned_blocks.setter
    def spawned_blocks(self, value: int):
        self.__spawned_blocks = value
        
    @level_cleared.setter
    def level_cleared(self, value: bool):
        self.__level_cleared = value

    def load_level(self): 
        # Increment level number
        self.level_number += 1
        
        # Calculate total blocks spawned in the current level
        self.total_blocks = self.level_number * self.block_multiplier
                        
        if not self.is_bg_music_active:
            mixer.music.load('./assets/sounds/in_game.mp3')
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)
            self.is_bg_music_active = True

        # Render main screen ui elements
        if not self.game_manager.game_over and not self.game_manager.quit_game:
            self.setup_level_ui()     

    def setup_level_ui(self):
        block_created = False
        is_level_sound_played = False

        self.spawned_blocks = 0

        self.block_manager.blocks = []

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 2200 - (self.level_number * 200)

        while not self.level_cleared and not self.game_manager.game_over and not self.game_manager.quit_game:
            
            self.handle_interactions()
            
            current_timer = pygame.time.get_ticks()

            if not self.level_cleared and not self.game_manager.quit_game:
                # Change background color
                self.game_manager.screen.fill((246, 241, 241))

                # Configure the timer object
                self.timer_info = self.configure_timer(
                    start_timer,
                    current_timer,
                    delay_timer)
                
                # Create a block if a block has already not been
                # created or if the specified interval of time
                # has elapsed since a block has been instantiated
                if not block_created or self.block_manager.spawn_next_block(
                        self.timer_info,
                        self.spawned_blocks,
                        self.total_blocks):

                    self.block_manager.create_block()
                    block_created = True

                    self.spawned_blocks += 1

                    # Reference: https://stackoverflow.com/questions/20023709/resetting-pygames-timer
                    # Advance start to current time to enable creation of the next block
                    start_timer = current_timer

                # If a block has been created and the total spawned blocks
                # has not reached the allowed blocks for the current level
                if block_created and not self.block_manager.block_count_reached(
                        self.spawned_blocks - 1,
                        self.total_blocks):

                    # Display the created blocks on the ui
                    self.ui_manager.render_blocks(self, self.block_manager)
               
            # Check if level is cleared        
            if self.blocks_left == 0 and\
                (len(self.block_manager.blocks) == 0) and\
                    (self.ui_manager.missed_count > 0):
                        
                # Display level cleared message
                self.ui_manager.render_font(self.message_font, 150, 320, 'LEVEL CLEARED!!!', (83,145,101))
                
                # Play level cleared sound
                if not is_level_sound_played:
                    self.level_complete_sound.play()
                    is_level_sound_played = True
                    
                # Wait until the sound is finished playing
                # Reference: https://stackoverflow.com/questions/54444765/check-if-a-pygame-mixer-channel-is-playing-a-sound
                if not mixer.Channel(0).get_busy():
                    # Indicate that the level is cleared
                    self.level_cleared = True
                    
            if (not self.level_cleared) and (
                not self.game_manager.game_over) and (
                not self.game_manager.quit_game
            ):
                # Update the display
                pygame.display.update()

    # Handle key stroke logic
    def handle_interactions(self):
        for event in pygame.event.get():
            # If the player clicks on cross icon in toolbar
            # Or if the player clicks on the quit button
            if event.type == pygame.QUIT:
                self.game_manager.quit_game = True
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                # Reference: https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
                # Detect key presses on number based blocks
                for i in range(0, 10):
                    if keys[pygame.K_0 + i]:
                        ascii_value = pygame.K_0 + i
                        self.block_manager.destroy_block(ascii_value, 48)
                        self.block_hit_sound.play()
                        
                # Detect key presses on letter based blocks
                for i in range(0, 26):
                    if keys[pygame.K_a + i]:
                        ascii_value = pygame.K_a + i
                        self.block_manager.destroy_block(ascii_value + 10, 97)
                        self.block_hit_sound.play()

    def configure_timer(self, start_timer, current_timer, delay_timer):
        self.timer_info = {
            "start_time": start_timer,
            "current_time": current_timer,
            "delay_time": delay_timer
        }

        return self.timer_info
