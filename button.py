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
        
        self.font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 64)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
    # https://pythonprogramming.altervista.org/how-to-make-an-hover-effect-on-a-button-in-pygame/?doing_wp_cron=1681509177.8325688838958740234375
    def apply_hover_effect(self):
        mouse = pygame.mouse.get_pos()
        
        text = self.font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect(center=self.rect.center)
                        
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(self.surface, self.active_color, self.rect)
        else:
            pygame.draw.rect(self.surface, self.inactive_color, self.rect)
        
        self.surface.blit(text, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False