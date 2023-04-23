import pygame

from singleton import Singleton
from block_manager import BlockManager
from ui_manager import UIManager

# TODO: Notify classes using game_over property when it is updated
# TODO : Check circular import issue with GameManager


class LevelManager(metaclass=Singleton):
    def __init__(self, game_manager):
        self.__level_number = 0

        # TODO: Get from game manager
        self.__high_score = 0

        # TODO: Get from block manager
        self.__blocks_left = 0

        # Static value of 3 for now
        # TODO: Change this based on current level number
        # TODO: Higher the level, lesser is the total misses
        self.__misses_left = 3

        self.__text_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 20)

        self.__ui_manager = UIManager(game_manager)
        self.__game_manager = game_manager

        # TODO: Change this based on current level number
        # TODO: Higher the level, higher the total blocks
        self.__total_blocks = 5
        self.__spawned_blocks = 0

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
    def total_blocks(self):
        return self.__total_blocks

    @property
    def spawned_blocks(self):
        return self.__spawned_blocks

    @property
    def ui_manager(self):
        return self.__ui_manager

    @property
    def game_manager(self):
        return self.__game_manager

    @property
    def block_manager(self):
        return self.__block_manager

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

    def load_level(self):
        # Increment level number
        self.level_number += 1

        # Render main screen ui elements
        self.setup_level_ui()

    def setup_level_ui(self):
        block_created = False

        # TODO: Reset for each new level
        self.spawned_blocks = 0

        # TODO: Reset blocks_x, blocks_y at start of each level

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 3000

        while not self.game_manager.game_over:
            
            self.handle_interactions()
            
            current_timer = pygame.time.get_ticks()

            if not self.game_manager.game_over:
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

                # Update the display
                pygame.display.update()
                       
            if self.blocks_left == 0 and\
                (len(self.block_manager.blocks) == 0) and\
                    (self.ui_manager.missed_count > 0):
                print("Level Cleared")

    # Handle key stroke logic
    def handle_interactions(self):
        for event in pygame.event.get():
            # If the player clicks on cross icon in toolbar
            # Or if the player clicks on the quit button
            if event.type == pygame.QUIT:
                self.game_manager.game_over = True
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                # Reference: https://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
                # Detect key presses on number based blocks
                for i in range(0, 10):
                    if keys[pygame.K_0 + i]:
                        ascii_value = pygame.K_0 + i
                        self.block_manager.destroy_block(ascii_value, 48)
                        
                # Detect key presses on letter based blocks
                for i in range(0, 26):
                    if keys[pygame.K_a + i]:
                        ascii_value = pygame.K_a + i
                        self.block_manager.destroy_block(ascii_value + 10, 97)
                
    def configure_timer(self, start_timer, current_timer, delay_timer):
        self.timer_info = {
            "start_time": start_timer,
            "current_time": current_timer,
            "delay_time": delay_timer
        }

        return self.timer_info
