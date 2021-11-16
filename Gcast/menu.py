import pygame
import sys
class Menu:
    def __init__(self, buttons, surface):
        self.buttons = buttons
        self.surface = surface
        
    
    def check_all(self):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if (
                pos[0] > button.x and
                pos[1] > button.y and
                pos[0] < (button.x + button.w) and
                pos[1] < (button.y + button.h)
                ):
                button.presence = 1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        button.f()
            else:
                button.presence = 0
    
    def draw_all(self):
        for button in self.buttons:
            self.surface.blit(button.image, (button.x, button.y))
            if button.presence == 1:
                pygame.draw.rect(self.surface, (255,255,0), (button.x, button.y, button.w, button.h), 3)

            
            
            
            
            
            
            
            
            
            
            
            
            
            