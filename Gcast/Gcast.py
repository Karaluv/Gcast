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
import mazeG

FPS = 40
u = 0.7

stepx = 100
stepy = 100
pe = 100

dl = 0.3
density = 0.009

height = 15
width = 15

pygame.font.init()
font = pygame.font.Font(None, 30)
fps_text = font.render("FPS: ", True, (255, 255, 255))

counter = 0






def input(user_input):
    global finished

    keys = pygame.key.get_pressed()

    global kw, ks, kd, ka, shift, fire

    for event in user_input:
        if bill.keyinput(event):
            global slaves
            slaves = bill.shoot(slaves, map)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                finished = True


        if event.type == pygame.QUIT:
            finished = True


                    

def draw_stuff():
    global fire
    bill.draw(screen)



def start():


    global pe,height,width,W,H,density,dl
    

    mazeG.main(height,width)

    mazeG.maze = tuple(tuple(i) for i in mazeG.maze)

    slaves = []

    for i in range(height*width//2):
        x,y = randint(2,height)+0.5,randint(2,width)+0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(randint(0,2),x,y,100,100))

    rend = rendering(0.5,density,dl,render_zone,height+2,width+2)

    print("start")
    
    bill = billy((width - 1) * 100 + 40, height * 100 + 40, 2 * math.pi / 2, "VAn", W, H, mazeG.maze)
    if mazeG.maze[int(bill.y / 100)][int(bill.x / 100)] != 0:
        bill = billy((width - 2) * 100 + 40, height * 100 + 40, 2 * math.pi / 2, "VAn", W, H, mazeG.maze)

    return  rend,bill,mazeG.maze,slaves

def update():
    

    global density,u,Tx,Ty,W,H

    bill.update()
    

    slave_data = ()
    for i in range(len(slaves)):
        slave_data += ((slaves[i].x,slaves[i].y,3))
    bill.check_fisting(slave_data)

    a = bill.a


    enemies = ()
    for i in range(len(slaves)):
        slaves[i].walk(map)
        enemies += ((slaves[i].x,slaves[i].y,slaves[i].type,slaves[i].frame))



    rend.render(map,enemies,math.cos(a-u),math.sin(a-u),math.cos(a+u),math.sin(a+u),0.15,7,bill.x,bill.y)


    x = rend.xs
    final_render = pygame.transform.scale(render_zone,(int(W*render_zone.get_width()/x),int(H+40)))
    screen.blit(final_render,(math.sin(Tx)*10-10,math.cos(Ty)*18-20))
    draw_stuff()




pygame.init()



pygame.mouse.set_visible(False)
infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h
render_zone = pygame.Surface((700, 200))

render_w = 355
render_h = 200

fire = 0
Tx = 0
Ty = 0

wh = (255, 255, 255)
bl = (0, 0, 0)

pygame.mixer.music.load(os.path.join(sys.path[0] + "\\pony\\music\\", "main_theme.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((W, H))

pygame.display.update()
clock = pygame.time.Clock()

finished = False

rend, bill, map, slaves = start()

kw, ks, ka, kd, shift = False, False, False, False, False

import time

start_time = time.time()

while not finished:
    clock.tick(FPS)

    input(pygame.event.get())
    update()
    screen.blit(fps_text, (30, 30))
    pygame.display.flip()
    # screen.fill(bl) - Это можно убрать

    counter += 1

    if counter == 10:
        fps_text = font.render("FPS: " + str(round(counter / (time.time() - start_time))), True, (255, 255, 255))
        counter = 0
        start_time = time.time()