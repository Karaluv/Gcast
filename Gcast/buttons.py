import pygame
import sys
import math

font1 = pygame.font.Font("ttf\\MAGNETOB.ttf", 40)

class button():
    def __init__(self, image, W, H, x, y, w, h, f):
        self.W = W
        self.H = H
        self.x = int(x*W)
        self.y = int(y*H)
        self.w = int(w*W)
        self.h = int(h*H)
        self.image = pygame.transform.smoothscale(image, (self.w, self.h))
        self.f = f
        self.click = 0
        self.presence = 0

class inputfield():
    def __init__(self, W, H, x, y, w, h):
        self.W = W
        self.H = H
        self.x = int(x * W)
        self.y = int(y * H)
        self.w = int(w * W)
        self.h = int(h * H)
        self.text = ""
        self.active = False

    def draw(self, screen):
        textsurface = font1.render(self.text, False, (255, 255, 255))
        textsurface.set_colorkey((0, 0, 0))
        screen.blit(textsurface, (self.x, self.y))

        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (self.x + self.w, self.y), 3)
        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y + self.h - 1),
                         (self.x + self.w, self.y + self.h - 1), 3)
        pygame.draw.arc(screen, (255, 255, 0), (self.x - self.h / 2, self.y, self.h, self.h),
                        math.pi / 2, math.pi * 1.5, 3)
        pygame.draw.arc(screen, (255, 255, 0), (self.x + self.w - self.h / 2, self.y, self.h, self.h),
                        3 * math.pi / 2, math.pi / 2, 3)
        #             pygame.draw.rect(screen, (0,0,0), (self.x, self.y+1, self.w, self.h-2), 0, 0)
        if self.active == 1:
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (self.x + self.w, self.y), 5)
            pygame.draw.line(screen, (255, 255, 0), (self.x, self.y + self.h - 1),
                             (self.x + self.w, self.y + self.h - 1), 5)
            pygame.draw.arc(screen, (255, 255, 0), (self.x - self.h / 2, self.y, self.h, self.h),
                            math.pi / 2, math.pi * 1.5, 5)
            pygame.draw.arc(screen, (255, 255, 0),
                            (self.x + self.w - self.h / 2, self.y, self.h, self.h), 3 * math.pi / 2,
                            math.pi / 2, 5)

class just_text():
    def __init__(self, image, W, H, x, y, w, h):
        self.W = W
        self.H = H
        self.x = int(x*W)
        self.y = int(y*H)
        self.w = int(w*W)
        self.h = int(h*H)
        self.image = pygame.transform.smoothscale(image, (self.w, self.h))
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y), (self.x + self.w, self.y), 3)
        pygame.draw.line(screen, (255, 255, 0), (self.x, self.y + self.h - 1),
                         (self.x + self.w, self.y + self.h - 1), 3)
        pygame.draw.arc(screen, (255, 255, 0), (self.x - self.h / 2, self.y, self.h, self.h),
                        math.pi / 2, math.pi * 1.5, 3)
        pygame.draw.arc(screen, (255, 255, 0), (self.x + self.w - self.h / 2, self.y, self.h, self.h),
                        3 * math.pi / 2, math.pi / 2, 3)