import pygame

from singleton import Singleton
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
        self.__misses_left = 0

        self.__text_font = pygame.font.Font('./assets/fonts/NiceSugar.ttf', 20)

        self.__ui_manager = UIManager(game_manager)
        self.__game_manager = game_manager

        self.__score_calculator = self.game_manager.score_calculator
        self.__block_manager = self.game_manager.block_manager

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

    def load_view_rules(self):
        self.setup_view_rules_ui()

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

        while not self.game_manager.game_over:

            for event in pygame.event.get():

                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True

            if not self.game_manager.game_over:
                # Change background color
                self.game_manager.screen.fill((0, 0, 0))

                # Display main screen ui
                self.ui_manager.render_main_screen_ui(self)

                # TODO: Introduce delay to aid block creation
                # not block_created or time has elapsed
                # If a block has not already been created
                if not block_created:
                    block = self.block_manager.create_block()
                    block_created = True

                if block_created:
                    self.game_manager.screen.blit(
                        block.sprite, (block.x_pos, block.y_pos))
                    block.y_pos += block.speed

                # Update the display
                pygame.display.update()

    def setup_view_rules_ui(self):
        x_coord = 100
        y_coord = 100

        while not self.game_manager.game_over:

            for event in pygame.event.get():

                # If the player clicks on cross icon in toolbar
                # Or if the player clicks on the quit button
                if event.type == pygame.QUIT:
                    self.game_manager.game_over = True

            if not self.game_manager.game_over:
                # Change background color
                self.game_manager.screen.fill((0, 0, 0))

                # Create a surface for the instructions box
                box_width = 800
                box_height = 500
                box_surface = pygame.Surface((box_width, box_height))
                box_surface.set_alpha(200)  # Set the surface transparency
                box_surface.fill((150, 150, 150))  # Set the surface color

                # Render the instructions paragraph on the box surface
                paragraph_font = pygame.font.Font(
                    "./assets/fonts/NiceSugar.ttf", 12)
                paragraph_text = "Welcome to ASCII Attack! \nGet ready to dodge falling letters and numbers as they fly through the air in black and white.\n The shadows loom large as you aim to clear each level before your health expires.\n Press start game to start!."
                paragraph_rect = pygame.Rect(
                    50, 50, box_width - 100, box_height - 100)
                self.ui_manager.render_paragraph(
                    paragraph_text, paragraph_font, paragraph_rect, box_surface, (255, 255, 255))

                # Blit the box surface onto the screen
                box_x = self.game_manager.screen.get_width() - box_width - 50
                box_y = y_coord + 100
                self.game_manager.screen.blit(box_surface, (box_x, box_y))

                # Display "Instructions" title
                title_font = pygame.font.Font(
                    "./assets/fonts/SuperMario256.ttf", 72)
                self.ui_manager.render_font(
                    title_font, x_coord, y_coord, "Instructions", (255, 201, 60))

                pygame.display.update()

    def handle_key_stroke(self):
        # Placeholder for handling key stroke logic
        pass

    def handle_missed_block(self):
        # Placeholder for handling missed block logic
        pass
