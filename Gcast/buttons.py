import pygame
import sys
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