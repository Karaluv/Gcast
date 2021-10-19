import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
from render import rendering

FPS = 60
u = 0.5

map = [[1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]]

class billy:
    
    def __init__(self, x,y,a,name):
        self.x = x
        self.y = y
        self.a = a
        self.name = name

    def Rotate(self,a):
        self.a = self.a +a
        global move
        move = True

    def Move(self,l,n):
        a = self.a
        x_ = self.x+l*math.sin(a)+n*math.cos(a)
        y_ = self.y+l*math.cos(a)+n*math.sin(a)
        global map1
        if map[int(y_/100+0.25)][int(x_/100+0.25)] == 0:
            if map[int(y_/100-0.25)][int(x_/100-0.25)] == 0:
                if map[int(y_/100-0.25)][int(x_/100+0.25)] == 0:
                    if map[int(y_/100+0.25)][int(x_/100-0.25)] == 0:
                        self.y = y_
                        self.x = x_



def start():
    global pe

    rend = rendering(0.5,0.01,screen)

    print("start")
    bill = billy(150,150,-math.pi/2,"VAn")
    return  rend,bill 

def input(user_input):


    keys=pygame.key.get_pressed()


    for event in user_input:
        global kw,ks,kd,ka

        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_q:
            #   finished = True
            if event.key == pygame.K_w:
                kw =True
            if event.key == pygame.K_s:
                ks =True
            if event.key == pygame.K_a:
                ka =True
            if event.key == pygame.K_d:
                kd =True

            if event.key == pygame.K_q:
                bill.Rotate(-0.1)
            if event.key == pygame.K_e:
                bill.Rotate(0.1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                kw =False
            if event.key == pygame.K_s:
                ks =False
            if event.key == pygame.K_a:
                ka =False
            if event.key == pygame.K_d:
                kd =False

        

        bill.Rotate((-W/2 +  pygame.mouse.get_pos()[0])/200)
        pygame.mouse.set_pos((W//2,H//2))
 

        if event.type == pygame.QUIT:
            #quit and save part
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #mouse event part
            #shoot(event.pos)
            print("shoot")



def update():
    
    a = bill.a

    rend.render(map,0.01,0.01,a-u,a+u,0.01,7,bill.x,bill.y)




pygame.init()

pygame.mouse.set_visible(False)

infoObject = pygame.display.Info()

W,H = infoObject.current_w, infoObject.current_h

W,H = W // 2,H // 2
ys = 10
h0 = 10000
l0 = 100
w0 = 1
dens = 0.01
dw = W*0.01 / (2*u) 


ston = pygame.image.load(os.path.join(sys.path[0],"stone.png"))
floor =  pygame.image.load(os.path.join(sys.path[0],"floor.jpg"))
floor = pygame.transform.scale(floor,(int(W*8.76/10.1),H//2))

i =0

move = False




#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.FULLSCREEN)

screen = pygame.display.set_mode((infoObject.current_w // 2, infoObject.current_h // 2))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
bl = (0,0,0)
rend,bill = start()
L0 = 25
pe =200
stepx =100
stepy = 100

kw,ks,ka,kd = False,False,False,False

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it



#main loop
while not finished:
    clock.tick(FPS)
    
    input(pygame.event.get())
    update()
    pygame.display.flip()
    screen.fill(bl)

    if kw:
        bill.Move(0,3)
    if ks:
        bill.Move(0,-3)
    if ka:
        bill.Move(-3,0)
    if kd:
        bill.Move(3,0)

    
