import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
from render import rendering

from slave import slave
from billy import billy
import multiprocessing

from multiprocessing import Process

import mazeG

FPS = 20
u = 0.7

stepx = 100
stepy = 100
pe = 100

dl = 0.3
density = 0.009

height = 15
width = 15








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
            if event.key == pygame.K_r:
                if bill.shoot_frame == 0 and not bill.B_reload:
                    bill.reload()



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

        

        bill.Rotate((-W/2 +  pygame.mouse.get_pos()[0])/800)
        pygame.mouse.set_pos((W//2,H//2))
 

        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bill.shoot_frame == 0 and not bill.B_reload:
                global slaves 
                slaves = bill.shoot(slaves,map)
                bill.shoot_frame = 1


                    

def draw_stuff():
    global fire
    bill.draw(screen)



def start():


    global pe,height,width,W,H,density,dl
    

    mazeG.main(height,width)

    slaves = []

    for i in range(height*width//2):
        x,y = randint(2,height)+0.5,randint(2,width)+0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(randint(0,2),x,y,100,100))

    rend = rendering(0.5,density,dl,render_zone,height+2,width+2)

    print("start")
    
    bill = billy((width-1)*100+40,(height)*100+40,2*math.pi/2,"VAn",W,H)
    if mazeG.maze[int(bill.y/100)][int(bill.x/100)] != 0 :
        bill = billy((width-2)*100+40,(height)*100+40,2*math.pi/2,"VAn",W,H)
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

    rend.render(map,enemies,a-u,a+u,0.15,7,bill.x,bill.y)


    x = rend.xs
    final_render = pygame.transform.smoothscale(render_zone,(int(W*render_zone.get_width()/x),int(H+40)))
    screen.blit(final_render,(math.sin(Tx)*10-10,math.cos(Ty)*18-20))
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


pygame.mixer.music.load(os.path.join(sys.path[0]+"\\pony\\music\\","main_theme.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((W, H))

pygame.display.update()
clock = pygame.time.Clock()

finished = False

rend,bill,map,slaves = start()


kw,ks,ka,kd,shift = False,False,False,False,False

import time

start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0



while not finished:
    clock.tick(FPS)
    
    input(pygame.event.get())
    update()
    pygame.display.flip()
    screen.fill(bl)


    counter+=1
    if (time.time() - start_time) > x :
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()

    speed = 0.5

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

    
