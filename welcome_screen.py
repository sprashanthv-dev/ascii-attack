import pygame
from button import Button
from pygame.locals import *

# TODO: Change to singleton
class WelcomeScreen:
    counter : int = 0
    
    def __init__(self, game_manager):   
        
        self.__game_manager = game_manager
        self.__ui_manager = self.game_manager.ui_manager
        
        self.initialize_attributes()
        self.add_background()   
              
        self.game_manager.play_background_music()
        self.initialize_buttons()
        
    @property
    def game_manager(self):
        return self.__game_manager
    
    @property
    def ui_manager(self):
        return self.__ui_manager
              
    def initialize_attributes(self):        
        self.screen = self.game_manager.screen
        self.title = self.game_manager.title
        self.width = self.game_manager.width
        self.height = self.game_manager.height
        
    def add_background(self):
        self.background_image = pygame.image.load("./assets/img/main_menu2.png")
        
        # ? What does this statement do
        self.background_image = pygame.transform.scale(
            self.background_image, (self.width, self.height))
        
    def initialize_buttons(self):
        
        button_params = self.ui_manager \
            .get_welcome_screen_button_params(
                self.width, self.height
            );
                
        self.start_game = Button(self.screen, "New Game", button_params["x"], button_params["y"])
        self.view_rules = Button(self.screen, "Rules", button_params["x"], button_params["y"] + button_params["spacing"])
        self.view_leaderboard = Button(self.screen, "Leaderboard", button_params["x"], button_params["y"] + 2 * button_params["spacing"])
        self.quit_game = Button(self.screen, "Quit", button_params["x"], button_params["y"] + 3 * button_params["spacing"])

    # TODO: Observer pattern implementation here ??
    def handle_interactions(self):
        for event in pygame.event.get():
            
            # If the player clicks on cross icon in toolbar
            # Or if the player clicks on the quit button
            if event.type == QUIT or self.quit_game.is_clicked(event):
                self.game_manager.game_over = True
            if self.start_game.is_clicked(event):
                # Start timer
                start_timer = pygame.time.get_ticks()
                self.game_manager.handle_game_start(start_timer, True) 
            if self.view_rules.is_clicked(event):
                # TODO: Handle view rules action
                pass
            if self.view_leaderboard.is_clicked(event):
                # TODO: Handle view leaderboard action
                pass

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        
        title_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 96)
        title_text = title_font.render(self.title, True, (255, 201, 60))
        self.screen.blit(title_text, (150, 180))
        
        self.start_game.apply_hover_effect()
        self.view_rules.apply_hover_effect()
        self.view_leaderboard.apply_hover_effect()
        self.quit_game.apply_hover_effect()