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
from buttons import button
from buttons import inputfield
from menu import Menu

from threading import Thread

FPS = 30
FPS = FPS +1
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

fps_text_r = font.render("FPS: ", True, (255, 255, 255))

counter = 0



def input_menu(user_input):
    global finished,game_paused

    keys = pygame.key.get_pressed()

    for event in user_input:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                finished = True
            if event.key == pygame.K_ESCAPE:
                game_paused = game_reset_mode(game_paused)

        if event.type == pygame.QUIT:
            finished = True


def input_game(user_input):
    global finished,game_paused

    keys = pygame.key.get_pressed()

    global kw, ks, kd, ka, shift, fire

    for event in user_input:
        if bill.keyinput(event):
            global slaves
            slaves = bill.shoot(slaves, map)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                finished = True
            if event.key == pygame.K_ESCAPE:
                game_paused = game_reset_mode(game_paused)

        if event.type == pygame.QUIT:
            finished = True

def draw_stuff():
    screen.blit(fps_text, (30, 30))
    screen.blit(fps_text_r, (30, 60))
    bill.draw(screen)
    pygame.display.flip()


def start():


    global pe,height,width,W,H,density,dl
    

    mazeG.main(height,width)

    mazeG.maze = tuple(tuple(i) for i in mazeG.maze)

    slaves = []

    for i in range(height*width//2):
        x,y = randint(2,height)+0.5,randint(2,width)+0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(randint(0,2),x,y,100,100))

    rend = rendering(0.5,density,dl,render_zone,height+2,width+2,update_render,redraw_all)
    #rend.daemon = True
    

    print("start")
    
    bill = billy((width - 1) * 100 + 40, height * 100 + 40, 2 * math.pi / 2, "VAn", W, H, mazeG.maze)
    if mazeG.maze[int(bill.y / 100)][int(bill.x / 100)] != 0:
        bill = billy((width - 2) * 100 + 40, height * 100 + 40, 2 * math.pi / 2, "VAn", W, H, mazeG.maze)

    return  rend,bill,mazeG.maze,slaves


def update_render():
    global u,enemies,map
    a = bill.a
    x0,y0 =bill.x,bill.y
    return map,enemies,math.cos(a-u),math.sin(a-u),math.cos(a+u),math.sin(a+u),0.15,7,bill.x,bill.y


def redraw_all():
    global W,H,start_time_r,counter_r,fps_text_r

    counter_r += 1

    if counter_r == 10:
        fps_text_r = font.render("REND CORE FPS: " + str(round(counter_r / (time.time() - start_time_r))), True, (255, 255, 255))
        counter_r = 0
        start_time_r = time.time()

    x = rend.xs
    final_render = pygame.transform.scale(render_zone,(int(W*render_zone.get_width()/x),int(H+40)))
    screen.blit(final_render,(math.sin(bill.Tx)*15-15,math.cos(bill.Ty)*15-20))
    thread_draw_stuff = Thread(target = draw_stuff, args = ())
    thread_draw_stuff.start()



def update():
    

    global density,u,Tx,Ty,W,H,get

    global enemies

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



    #rend.map,rend.enemies,rend.cos0,rend.sin0,rend.cos1,rend.sin1,rend.minR,rend.maxR,rend.x0,rend.y0=(map,enemies,math.cos(a-u),math.sin(a-u),math.cos(a+u),math.sin(a+u),0.15,7,bill.x,bill.y)


pygame.init()

#pygame.mouse.set_visible(False)
infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h
render_zone = pygame.Surface((700, 200))



wh = (255, 255, 255)
bl = (0, 0, 0)

pygame.mixer.music.load(os.path.join(sys.path[0] + "\\pony\\music\\", "main_theme.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((W, H), pygame.SRCALPHA)

pygame.display.update()
clock = pygame.time.Clock()

finished = False

get = True
kw, ks, ka, kd, shift = False, False, False, False, False
rend = 0
bill = 0
map =0
slaves =0
render_w = 355
render_h = 200
Tx,Ty =0,0
import time


def game_start():
    global game_st,W,H
    global rend,bill,slaves,map
    global kw, ks, ka, kd, shift
    global Tx,Ty
    global multiplayer

    multiplayer = False
    rend = 0
    bill = 0
    map =0
    slaves =0
    Tx = 0
    Ty = 0
    rend, bill, map, slaves = start()

    kw, ks, ka, kd, shift = False, False, False, False, False
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()


def multiplayer_start():
    global game_st, W, H
    global rend, bill, slaves, map
    global kw, ks, ka, kd, shift
    global Tx, Ty
    global multiplayer

    multiplayer = True
    rend = 0
    bill = 0
    map = 0
    slaves = 0
    Tx = 0
    Ty = 0
    rend, bill, map = start()


    kw, ks, ka, kd, shift = False, False, False, False, False
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()

    
def game_finish():
    global finished
    finished = True
    
def game_resume():
    global game_paused
    game_paused = game_reset_mode(game_paused)
def game_return():
    global game_st
    game_st = 0
    rend.stop()
    rend.join()
    screen.fill(bl)
    
def game_reset_mode(paused):
    global game_st
    if paused == False:
        game_st = 2
        pygame.mouse.set_visible(True)
        rend.pause()
    if paused == True:
        game_st = 1
        pygame.mouse.set_visible(False)
        rend.resume()
    #pygame.mouse.set_pos((W//2,H//2))
    return not paused

def open_multiplayer_menu1():
    global game_st
    game_st = 3


Wdisp, Hdisp = screen.get_size()

buttons1 = [0]*3
buttons2 = [0]*3

font1 = pygame.font.Font(os.path.join(sys.path[0] + "\\ttf\\", "MAGNETOB.ttf"), 40)
textsurface = font1.render(' Singleplayer ', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.blit(textsurface,(0,0))


buttons1[0] = button(s, Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_start)


textsurface = font1.render(' Multiplayer ', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.fill((0,0,0,0))
s.blit(textsurface,(0,0))
buttons1[1] = button(s, Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, open_multiplayer_menu1)

textsurface = font1.render(' Main menu ', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.fill((0,0,0,0))
s.blit(textsurface,(0,0))
buttons2[1] = button(s, Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, game_return)


textsurface = font1.render('    Quit    ', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.blit(textsurface,(0,0))

buttons1[2] = button(s, Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)
buttons2[2] = button(s, Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)


textsurface = font1.render('Resume', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.blit(textsurface,(0,0))

buttons2[0] = button(s, Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_resume)

menu1 = Menu(buttons1, screen)
menu2 = Menu(buttons2, screen)

# Меню где выбираем, создаем сервер или присоединяемся
buttons3 = [0]*2

textsurface = font1.render('Create server', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.blit(textsurface,(0,0))
buttons3[0] = button(s, Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_start)

textsurface = font1.render('Join server', False, (255, 255, 255))
textsurface.set_colorkey((0,0,0))
s = pygame.Surface(textsurface.get_size(),pygame.SRCALPHA)
s.blit(textsurface,(0,0))
buttons3[1] = button(s, Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, game_start)

input = inputfield(Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08,)
menu3 = Menu(buttons3, screen, [input])



# Меню где создаем сервер(пока нету)


start_time = time.time()
start_time_r = time.time()
counter_r = 0
game_paused = False
game_st = 0
main_screen = pygame.image.load(os.path.join(sys.path[0] + "\\pony\\", "main_screen.png"))
main_screen = pygame.transform.scale(main_screen, (Wdisp, Hdisp))

#rend.start()

while not finished:
    
    clock.tick(FPS)
    
    if game_st == 1:
        input_game(pygame.event.get())
        update()
    if game_st == 0:
        screen.blit(main_screen, (0,0))
        menu1.draw_all()
        menu1.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 2:
        pygame.draw.rect(screen, (233,0,0), (int(Wdisp*0.375-0.1*Hdisp),0,int(0.25*Wdisp+0.2*Hdisp),Hdisp),0)
        menu2.draw_all()
        menu2.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 3:
        screen.blit(main_screen, (0, 0))
        menu3.draw_all()
        menu3.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    
    counter += 1

    if counter == 10:
        fps_text = font.render("MAIN CORE FPS: " + str(round(counter / (time.time() - start_time))), True, (255, 255, 255))
        counter = 0
        start_time = time.time()

pygame.quit()