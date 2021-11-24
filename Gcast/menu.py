import pygame
import sys
import math

class Menu:
    def __init__(self, buttons, surface, inputfields = [], texts = []):
        self.texts = texts
        self.inputfields = inputfields
        self.buttons = buttons
        self.surface = surface
        
    
    def check_all(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if (
                        button.x < pos[0] < (button.x + button.w) and
                        button.y < pos[1] < (button.y + button.h)
                    ):
                    button.presence = 1
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        button.f()
                else:
                    button.presence = 0

            for inputfield in self.inputfields:
                    pos = pygame.mouse.get_pos()
                    if (
                            inputfield.x < pos[0] < (inputfield.x + inputfield.w) and
                            inputfield.y < pos[1] < (inputfield.y + inputfield.h)
                    ):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                             inputfield.active = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        inputfield.active = False
                    if inputfield.active:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                inputfield.text = inputfield.text[0:-1]
                            else:
                                inputfield.text += event.unicode

    
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
        for inputfield in self.inputfields:
            inputfield.draw(self.surface)
        for text in self.texts:
            text.draw(self.surface)