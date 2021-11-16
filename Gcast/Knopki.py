import pygame as pg
import sys

def game_start():
    game_st = 1
    rend.start()

buttons1 = [0]*3
buttons2 = [0]*3
s = pg.Surface((100,40), pg.SRCALPHA)

s.fill((0,0,0))
font = pg.font.SysFont('arial', 20)
textsurface = font.render('Singleplayer', False, (255, 255, 255))
u = font.size('Singleplayer')
s.blit(textsurface,(int((100 - u[0])/2),0))
W, H = screen.get_size()
buttons1[0] = button(s, W, H, 0.4, 0.3, 0.2, 0.05, game_start)
menu1 = Menu(buttons1, screen)