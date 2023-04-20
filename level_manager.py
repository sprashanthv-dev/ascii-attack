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
        self.__misses_left = 0

        self.__text_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 20)

        self.__ui_manager = UIManager(game_manager)
        self.__game_manager = game_manager

        # TODO: Change this based on current level number
        # TODO: Higher the level, higher the total blocks
        self.__total_blocks = 5
        self.__spawned_blocks = 0

        self.timer_info = {}

        self.__score_calculator = self.game_manager.score_calculator
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

    @property
    def score_calculator(self):
        return self.__score_calculator

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

        # Create a block
        # block = self.block_manager.create_block()
        # print("Block " + block)

    def setup_level_ui(self):
        block_created = False

        # TODO: Reset for each new level
        self.spawned_blocks = 0

        # TODO: Reset blocks_x, blocks_y at start of each level
        # TODO : A level ends when blocks spawned == total blocks in that level
        # TODO : Destroy the block that the player fails to clear
        # TODO: Track each block's movement and move it until it hits
        #       the ground or is cleared by the player

        # Start timer
        start_timer = pygame.time.get_ticks()

        # Time to delay in milliseconds
        delay_timer = 3000

        while not self.game_manager.game_over:
            for event in pygame.event.get():
                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True

            current_timer = pygame.time.get_ticks()

            if not self.game_manager.game_over:
                # Change background color
                self.game_manager.screen.fill((0, 0, 0))

                # Display main screen ui
                self.ui_manager.render_main_screen_ui(self)

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

                    block = self.block_manager.create_block()
                    block_created = True
                    
                    self.spawned_blocks += 1

                    # Reference: https://stackoverflow.com/questions/20023709/resetting-pygames-timer
                    # Advance start to current time to enable
                    # creation of the next block
                    start_timer = current_timer
                    
                    print(self.spawned_blocks)

                if block_created and not self.block_manager.block_count_reached(
                    self.spawned_blocks - 1,
                    self.total_blocks):
                    
                    for block in self.block_manager.blocks:

                        self.game_manager.screen.blit(
                            block.sprite,
                            (block.x_pos, block.y_pos)
                        )

                        block.y_pos += block.speed

                # Update the display
                pygame.display.update()

    def handle_key_stroke(self):
        # Placeholder for handling key stroke logic
        pass

    def handle_missed_block(self):
        # Placeholder for handling missed block logic
        pass

    def configure_timer(self, start_timer, current_timer, delay_timer):
        self.timer_info = {
            "start_time": start_timer,
            "current_time": current_timer,
            "delay_time": delay_timer
        }

        return self.timer_info
