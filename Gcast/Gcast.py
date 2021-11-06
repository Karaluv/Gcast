import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
from render import rendering
import mazeG
from slave import slave
from billy import billy
import threading




FPS = 60
u = 0.5

stepx = 100
stepy = 100
pe = 100

dl = 0.01
density = 0.03

height = 11
width = 27







def input(user_input):


    keys=pygame.key.get_pressed()

    global kw,ks,kd,ka,shift,fire

    for event in user_input:
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
               finished = True
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

        

        bill.Rotate((-W/2 +  pygame.mouse.get_pos()[0])/400)
        pygame.mouse.set_pos((W//2,H//2))
 

        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if fire == 0:
                global slaves 
                slaves = bill.shoot(slaves,map)
                fire = 5
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(sys.path[0],"luger_sound.mp3")))


                    

def draw_stuff():
    global fire
    if fire == 0:
        screen.blit(luger,(W-550,H-luger.get_height()+50))
    else:
        if fire > 2:
            screen.blit(luger_fire,(W-550,H-luger.get_height()+50))
        else:
            screen.blit(luger,(W-550,H-luger.get_height()+50))
        fire = fire -1


def start():


    global pe,height,width
    
    mazeG.height = height
    mazeG.width = width

    mazeG

    slaves = []

    for i in range(160):
        x,y = randint(1,27+3)+0.5,randint(1,11+3)+0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(0,x,y,100,100))

    rend = rendering(0.5,0.006,render_zone,height+4,width+4)

    print("start")
    bill = billy((width)*100+40,(height+2)*100+40,-math.pi/2,"VAn")
    print(mazeG.maze[int(bill.y/100)][int(bill.x/100)])

    return  rend,bill,mazeG.maze,slaves

def update():
    

    global density,u,Tx,Ty,W,H

    bill.update()
    

    slave_data = []
    for i in range(len(slaves)):
        slave_data.append([slaves[i].x,slaves[i].y,3])
    bill.check_fisting(slave_data)

    a = bill.a


    enemies = []
    for i in range(len(slaves)):
        slaves[i].walk(map)
        enemies.append([slaves[i].x,slaves[i].y,slaves[i].type,slaves[i].frame])

    x = rend.render(map,enemies,density,a-u,a+u,0.15,7,bill.x,bill.y)
    final_render = pygame.transform.smoothscale(render_zone,(int(W*render_zone.get_width()/x),int(H+40)))
    screen.blit(final_render,(math.sin(Tx)*10-10,math.cos(Ty)*20-20))
    draw_stuff()




pygame.init()


pygame.mouse.set_visible(False)
infoObject = pygame.display.Info()
W,H = infoObject.current_w, infoObject.current_h
render_zone = pygame.Surface(((W+40)//2,(H+30)//2))

dw = W*0.01 / (2*u) 
fire = 0
Tx = 0
Ty = 0

wh = (255,255,255)
bl = (0,0,0)

luger =  pygame.image.load(os.path.join(sys.path[0],"luger.png"))
luger_fire =  pygame.image.load(os.path.join(sys.path[0],"luger_fire.png"))
luger.set_colorkey(wh)
luger_fire.set_colorkey(wh)

pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(sys.path[0],"gachi_doom.mp3")))


screen = pygame.display.set_mode((W, H))

pygame.display.update()
clock = pygame.time.Clock()

finished = False


rend,bill,map,slaves = start()


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
        bill.Move(0,3*speed,map)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if ks:
        bill.Move(0,-3*speed,map)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if ka:
        bill.Move(-3*speed,0,map)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed
    if kd:
        bill.Move(3*speed,0,map)
        Tx = Tx+0.1*speed
        Ty = Ty+0.1*speed

    
