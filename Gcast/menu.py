import pygame
import sys
import math

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
#             pygame.draw.rect(self.surface, (255,255,0), (button.x, button.y, button.w, button.h), 1)
            pygame.draw.line(self.surface, (255,255,0), (button.x, button.y), (button.x + button.w, button.y), 3)
            pygame.draw.line(self.surface, (255,255,0), (button.x, button.y + button.h - 1), (button.x + button.w, button.y + button.h - 1), 3)
            pygame.draw.arc(self.surface, (255,255,0), (button.x - button.h/2, button.y, button.h, button.h),math.pi/2,math.pi*1.5, 3)
            pygame.draw.arc(self.surface, (255,255,0), (button.x + button.w- button.h/2, button.y, button.h, button.h),3*math.pi/2,math.pi/2, 3)
#             pygame.draw.rect(self.surface, (0,0,0), (button.x, button.y+1, button.w, button.h-2), 0, 0)
            if button.presence == 1:
                pygame.draw.line(self.surface, (255,255,0), (button.x, button.y), (button.x + button.w, button.y), 5)
                pygame.draw.line(self.surface, (255,255,0), (button.x, button.y + button.h - 1), (button.x + button.w, button.y + button.h - 1), 5)
                pygame.draw.arc(self.surface, (255,255,0), (button.x - button.h/2, button.y, button.h, button.h),math.pi/2,math.pi*1.5, 5)
                pygame.draw.arc(self.surface, (255,255,0), (button.x + button.w- button.h/2, button.y, button.h, button.h),3*math.pi/2,math.pi/2, 5)

            
            
            
            
            
            
            
            
            
            
            
            
            
            