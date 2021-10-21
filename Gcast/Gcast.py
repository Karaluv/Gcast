import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
from render import rendering
import mazeG

FPS = 60
u = 0.5




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
        x_ = self.x-l*math.sin(math.pi - a)+n*math.cos(a)
        y_ = self.y-l*math.cos(math.pi - a)+n*math.sin(a)
        global map1
        if map[int(y_/100+0.05)][int(x_/100+0.05)] == 0:
            if map[int(y_/100-0.05)][int(x_/100-0.05)] == 0:
                if map[int(y_/100-0.05)][int(x_/100+0.05)] == 0:
                    if map[int(y_/100+0.05)][int(x_/100-0.05)] == 0:
                        self.y = y_
                        self.x = x_





def input(user_input):


    keys=pygame.key.get_pressed()


    for event in user_input:
        global kw,ks,kd,ka,shift

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
            if event.key == pygame.K_LSHIFT:
                shift =True

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
            if event.key == pygame.K_LSHIFT:
                shift =False

        

        bill.Rotate((-W/2 +  pygame.mouse.get_pos()[0])/200)
        pygame.mouse.set_pos((W//2,H//2))
 

        if event.type == pygame.QUIT:
            #quit and save part
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #mouse event part
            #shoot(event.pos)
            global fire
            fire = 5

def draw_stuff():
    global fire
    if fire == 0:
        screen.blit(luger,(W-550,H-luger.get_height()+50))
    else:
        screen.blit(luger_fire,(W-550,H-luger.get_height()+50))
        fire = fire -1


def start():
    global pe

    height = 11
    width = 27

    mazeG.height = height
    mazeG.width = width

    mazeG

    maze = [[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,1],[1,0,0,0,1,1,0,1],[1,1,1,1,1,1,1,1]]

    rend = rendering(0.5,0.006,render_zone,height+4,width+4)

    print("start")
    bill = billy((width)*100+50,(height+1)*100+50,-math.pi/2,"VAn")
    print(mazeG.maze[int(bill.y/100)][int(bill.x/100)])

    return  rend,bill,mazeG.maze

def update():
    
    a = bill.a

    x = rend.render(map,0.006,0.03,a-u,a+u,0.15,7,bill.x,bill.y)
    final_render = pygame.transform.smoothscale(render_zone,(int(W*render_zone.get_width()/x),int(H+40)))
    screen.blit(final_render,(math.sin(Tx)*10-10,math.cos(Ty)*20-20))
    draw_stuff()
    #pygame.draw.rect(screen,(128,128,0),(1367,0,800,1080),0)


pygame.init()



pygame.mouse.set_visible(False)

infoObject = pygame.display.Info()

W,H = infoObject.current_w, infoObject.current_h

#W,H = W // 2,H // 2

render_zone = pygame.Surface(((W+40)//2,(H+30)//2))

ys = 10
h0 = 10000
l0 = 100
w0 = 1
dens = 0.01
dw = W*0.01 / (2*u) 
fire = 0


wh = (255,255,255)


luger =  pygame.image.load(os.path.join(sys.path[0],"luger.png"))
luger_fire =  pygame.image.load(os.path.join(sys.path[0],"luger_fire.png"))
luger.set_colorkey(wh)
luger_fire.set_colorkey(wh)
i =0

move = False




#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.FULLSCREEN)

screen = pygame.display.set_mode((W, H))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
bl = (0,0,0)
rend,bill,map = start()
L0 = 25
pe =200
stepx =100
stepy = 100

Tx = 0
Ty = 0

kw,ks,ka,kd,shift = False,False,False,False,False


while not finished:
    clock.tick(FPS)
    
    input(pygame.event.get())
    update()
    pygame.display.flip()
    screen.fill(bl)

    speed = 1

    if shift:
        speed = 2
    else:
        speed = 1
    if kw:
        bill.Move(0,3*speed)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if ks:
        bill.Move(0,-3*speed)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if ka:
        bill.Move(-3*speed,0)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if kd:
        bill.Move(3*speed,0)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed

    
