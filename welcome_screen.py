import pygame
from button import Button
from pygame.locals import *
from game_manager import GameManager

class WelcomeScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen = self.game_manager.screen
        self.title = self.game_manager.title
        self.width = self.game_manager.width
        self.height = self.game_manager.height
        self.background_image = pygame.image.load("./assets/img/main_menu.png")
        self.background_sound = pygame.mixer.Sound("./assets/sounds/ingame.wav")
        self.background_sound.play(-1)
        self.main_menu_title = "Main Menu"
        font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 64)
        self.start_game = Button(self.screen, "New Game", 514, 200, font)
        self.view_rules = Button(self.screen, "Rules", 514, 250, font)
        self.view_leaderboard = Button(self.screen, "Leaderboard", 514, 300, font)
        self.quit_game = Button(self.screen, "Quit", 514, 350, font)

    def handle_interactions(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if self.start_game.is_clicked(event):
                # TODO: Handle start game action
                pass
            if self.view_rules.is_clicked(event):
                # TODO: Handle view rules action
                pass
            if self.view_leaderboard.is_clicked(event):
                # TODO: Handle view leaderboard action
                pass
            if self.quit_game.is_clicked(event):
                pygame.quit()
        self.draw()
        pygame.display.update()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 96)
        title_text = font.render(self.title, True, (255, 201, 60))
        self.screen.blit(title_text, (150, 100))
        
        font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 64)
        main_menu_text = font.render(self.main_menu_title, True, (255, 255, 255))
        self.screen.blit(main_menu_text, (450, 250))
        
        self.start_game.draw()
        self.view_rules.draw()
        self.view_leaderboard.draw()
        self.quit_game.draw()
        
        pygame.display.update()