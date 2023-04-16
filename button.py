import pygame

# https://pythonprogramming.altervista.org/buttons-in-pygame/?doing_wp_cron=1681507916.7993800640106201171875
class Button:    
    def __init__(self, surface, text, x_coord, y_coord):
        self.initialize_attributes(surface, text, x_coord, y_coord)
        
    def initialize_attributes(self, surface, text, x_coord, y_coord):
        self.surface = surface
        self.text = text
        
        self.x = x_coord
        self.y = y_coord
                
        self.width = 200
        self.height = 50
        
        self.inactive_color = (255,255,255)
        self.active_color = (200,200,200)
        
        self.font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 48)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
    # https://pythonprogramming.altervista.org/how-to-make-an-hover-effect-on-a-button-in-pygame/?doing_wp_cron=1681509177.8325688838958740234375
    def apply_hover_effect(self):
        mouse = pygame.mouse.get_pos()
    
        text = self.font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect()
        
        # Set the position of the text rectangle to be the same as the button's position
        text_rect.center = self.rect.center
        
        # Increase the width and height of the text rectangle to cover the entire text
        text_width = text_rect.width
        text_height = text_rect.height
        text_rect.width = text_width
        text_rect.height = text_height
        
        if text_rect.collidepoint(mouse):
            # Draw a rectangle over the entire text with the active color
            pygame.draw.rect(self.surface, self.active_color, text_rect)
        else:
            # Draw a rectangle over the entire text with the inactive color
            pygame.draw.rect(self.surface, self.inactive_color, text_rect)
        
        # Render the text on top of the rectangle
        self.surface.blit(text, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False