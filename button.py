import pygame
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
        self.inactive_color = (255, 255, 255)
        self.active_color = (200, 200, 200)
        self.font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 48)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
    def apply_hover_effect(self):
        mouse = pygame.mouse.get_pos()
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        text_width = text_rect.width
        text_height = text_rect.height
        text_rect.width = text_width
        text_rect.height = text_height
        
        if text_rect.collidepoint(mouse):
            pygame.draw.rect(self.surface, self.active_color, text_rect)
        else:
            pygame.draw.rect(self.surface, self.inactive_color, text_rect)
        self.surface.blit(text, text_rect)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False
    
    def draw(self):
        self.apply_hover_effect()