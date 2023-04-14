import pygame

# https://pythonprogramming.altervista.org/buttons-in-pygame/?doing_wp_cron=1681507916.7993800640106201171875
class Button:
    def __init__(self, surface, text, x, y, font, width=200, height=50, inactive_color=(255,255,255), active_color=(200,200,200)):
        self.surface = surface
        self.text = text
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.font = font
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    # https://pythonprogramming.altervista.org/how-to-make-an-hover-effect-on-a-button-in-pygame/?doing_wp_cron=1681509177.8325688838958740234375
    def draw(self, font, outline=2):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(self.surface, self.active_color, self.rect)
        else:
            pygame.draw.rect(self.surface, self.inactive_color, self.rect)
        
        text = font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect(center=self.rect.center)
        self.surface.blit(text, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False