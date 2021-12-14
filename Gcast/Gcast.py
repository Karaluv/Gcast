import math
import os
import sys
import time
from random import randint
from threading import Thread

import cv2
import moviepy.editor as mp
import pygame
from pygame import display
from pygame.locals import Color

import mazeG
from billy import billy
from buttons import button, inputfield, just_text
from menu import Menu
from online import Client, Server
from render import rendering
from slave import slave

# parameters for the program
# target core fps
FPS = 30
FPS = FPS + 1
# field of view
u = 0.7
# sizing numbers
stepx = 100
stepy = 100
pe = 100
# render quality
dl = 0.3
density = 0.009
# maze size
height = 15
width = 15

# init some stuff for printing out stats
pygame.font.init()
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(os.path.join(
    sys.path[0] + "\\ttf\\", "MAGNETOB.ttf"), 40)
fps_text = font.render("FPS: ", True, (255, 255, 255))
fps_text_r = font.render("FPS: ", True, (255, 255, 255))
# FPS core timer
counter = 0


# def for creating text


def textsurf(text):
    '''
    text - text string
    '''
    textsurface = font1.render(text, False, (255, 255, 255))
    textsurface.set_colorkey((0, 0, 0))
    s = pygame.Surface(textsurface.get_size(), pygame.SRCALPHA)
    s.blit(textsurface, (0, 0))
    return s


# def for user input in menues


def input_menu(user_input):
    '''
    user_input - pygame ivents
    '''
    # varibales which sets which menu is opened
    global finished, game_paused
    keys = pygame.key.get_pressed()
    for event in user_input:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                finished = True
            if event.key == pygame.K_ESCAPE:
                game_paused = game_reset_mode(game_paused)

        if event.type == pygame.QUIT:
            finished = True


# def for user input in menues


def input_game(user_input):
    '''
    user_input - pygame ivents
    '''
    # varibales which sets which menu is opened
    global finished, game_paused
    keys = pygame.key.get_pressed()

    for event in user_input:
        bill.keyinput(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                finished = True
            if event.key == pygame.K_ESCAPE:
                game_paused = game_reset_mode(game_paused)

        if event.type == pygame.QUIT:
            finished = True


# def which redraws some on sreen images


def draw_stuff():
    screen.blit(fps_text, (30, 30))
    screen.blit(fps_text_r, (30, 60))
    bill.draw(screen)
    pygame.display.flip()


# def that starts gameplay and inits all stuff


def start():
    # loads global variables
    global pe, height, width, W, H, density, dl
    # creates maze
    mazeG.main(height, width)
    mazeG.maze = tuple(tuple(i) for i in mazeG.maze)
    # spawns slaves
    slaves = []
    for i in range(height * width // 2):
        x, y = randint(3, height - 1) + 0.5, randint(3, width - 1) + 0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(randint(0, 2), x, y, 100, 100))
    # inits render core
    rend = rendering(0.5, density, dl, render_zone, height +
                     2, width + 2, update_render, redraw_all, 1)
    # creates bill
    bill = billy((width - 1) * 100 + 40, height * 100 + 40,
                 2 * math.pi / 2, "VAn", W, H, mazeG.maze)
    if mazeG.maze[int(bill.y / 100)][int(bill.x / 100)] != 0:
        bill = billy((width - 2) * 100 + 40, height * 100 + 40,
                     3 * math.pi / 2, "VAn", W, H, mazeG.maze)
    # returns new variables
    return rend, bill, mazeG.maze, slaves


# def which is called by render core and updates render data


def update_render():
    global u, enemies, map
    a = bill.a
    x0, y0 = bill.x, bill.y
    return map, enemies, math.cos(a - u), math.sin(a - u), math.cos(a + u), math.sin(
        a + u), 0.15, 7, bill.x, bill.y, bill.z


# def which draws stuff too


def redraw_all():
    # takes global variables
    global W, H, start_time_r, counter_r, fps_text_r
    # prints out fps
    counter_r += 1
    if counter_r == 10:
        fps_text_r = font.render(
            "REND CORE FPS: " + str(round(counter_r / (time.time() - start_time_r))), True, (255, 255, 255))
        counter_r = 0
        start_time_r = time.time()
    # blits rendered image
    x = rend.xs
    final_render = pygame.transform.scale(
        render_zone, (int(W * render_zone.get_width() / x), int(H)))
    screen.blit(final_render, (math.sin(bill.x) * 0 - 0, math.cos(bill.Ty) * 0 - 0))
    thread_draw_stuff = Thread(target=draw_stuff, args=())
    thread_draw_stuff.start()


# def which updates parametrs of enemies and all other stuff by every tick of main core
def update():
    # loads global variables
    global density, u, Tx, Ty, W, H, get
    global enemies, bill
    # updtae bill
    bill.update(slaves)
    # update enemy data
    slave_data = ()
    for i in range(len(slaves)):
        slave_data += ((slaves[i].x, slaves[i].y, 3))

    # check if slaves shoot at main hero
    enemies = ()
    l = 0

    for i in range(len(slaves)):
        if not multiplayer:
            if slaves[i - l].walk(map, bill.x, bill.y):
                bill.hp -= 0.5
        enemies += ((slaves[i - l].x, slaves[i - l].y,
                     slaves[i - l].type, slaves[i - l].frame))
        if (slaves[i - l].death(bill.x, bill.y)):
            del (slaves[i - l])
            l += 1


# starts out game and inits parametrs
pygame.init()

infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h
Wdisp, Hdisp = infoObject.current_w, infoObject.current_h
render_zone = pygame.Surface((700, 200))

# sets white and black
wh = (255, 255, 255)
bl = (0, 0, 0)

# loads video for intro
cap = cv2.VideoCapture(os.path.join(
    sys.path[0] + "\\pony\\video\\", "Intro_video_resized.mp4"))
success, img = cap.read()
shape = img.shape[1::-1]
wn = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# plays intro sound
pygame.mixer.music.load(os.path.join(
    sys.path[0] + "\\pony\\music\\", "Intro_sound.mp3"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)

# plays intro
while success:
    clock.tick(24)
    success, img = cap.read()
    if (img is None):
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                success = False
    wn.blit(pygame.transform.scale(pygame.image.frombuffer(
        img.tobytes(), shape, "BGR"), (Wdisp, Hdisp)), (0, 0))
    pygame.display.update()

# sets ingame music
pygame.mixer.music.load(os.path.join(
    sys.path[0] + "\\pony\\music\\", "main_theme.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# resets creen and pygame
screen = pygame.display.set_mode((W, H), pygame.SRCALPHA)
pygame.display.update()
# for timer data
clock = pygame.time.Clock()

# sets ingame varibles again
finished = False
rend = 0
bill = 0
map = 0
slaves = 0
render_w = 355
render_h = 200
Tx, Ty = 0, 0



# def for buttons


def game_start():
    global game_st, W, H
    global rend, bill, slaves, map
    global Tx, Ty
    global multiplayer

    multiplayer = False
    rend = 0
    bill = 0
    map = 0
    slaves = 0
    Tx = 0
    Ty = 0
    rend, bill, map, slaves = start()

    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()


def delegate_data():
    return (bill.x, bill.y, slaves[0].lifes)


def multiplayer_start_create():
    global server_info
    global game_st, W, H
    global rend, bill, slaves, map
    global Tx, Ty
    global multiplayer
    global server
    global is_server
    global enemies

    multiplayer = True
    is_server = True
    rend = 0
    bill = 0
    map = 0
    slaves = 0
    Tx = 0
    Ty = 0

    rend, bill, map, slaves = start()  # генерируем все кроме врагов
    slaves = []  # готовим пустой массив для противника
    for i in range(height * width // 2):  # ищем свободное место для спавна противника
        x, y = randint(3, height - 1) + 0.5, randint(3, width - 1) + 0.5
        if mazeG.maze[int(y)][int(x)] == 0:
            slaves.append(slave(randint(0, 2), x, y, 100, 100))
            break  # Когда находим, создаем врага и прерываем цикл
    server = Server(2, int(server_info[0]), map, x * 100, y * 100,
                    delegate_data)  # Создаем сервак и отправляем сразу карту
    # и координаты спавна врага
    print("server created")

    update()
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()

    if not server.is_alive():
        print("ok")
        server.start()


def multiplayer_start_join():
    global server_info
    global game_st, W, H
    global rend, bill, slaves, map
    global Tx, Ty
    global multiplayer
    global client
    global is_server

    multiplayer = True
    is_server = False
    rend = 0
    bill = 0
    map = 0
    slaves = 0
    Tx = 0
    Ty = 0

    rend, bill, map, slaves = start()  # создаем рендер просто из старта
    slaves = []  # Готовим массив для врага
    
    slaves.append(
        slave(randint(0, 2), (width - 1) * 100 + 40, height * 100 + 40, 100, 100))  # Создаем врага, владелец сервака
    # всегда спавнится в начале лабиринта
    client = Client(server_info[1], int(server_info[0]), delegate_data)  # подключаемся к серваку
    bill = billy(client.start_x, client.start_x,
                 2 * math.pi / 2, "VAn", W, H, mazeG.maze)  # создаем игрока по координатам от сервака
    map = client.map  # запоминаем карту по инфе с сервака
    bill.map = map
    bill.recreate_minimap()
    
    update()
    
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()
    if not client.is_alive():
        print("ok")
        client.start()


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
    return not paused


def open_multiplayer_menu1():
    global game_st
    game_st = 3


# gets display size
Wdisp, Hdisp = screen.get_size()
# creates arrays of buttons
buttons1 = [0] * 3
buttons2 = [0] * 3

# sets buttons for menues
s = textsurf(' Singleplayer ')
buttons1[0] = button(s, Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_start)
s = textsurf(' Multiplayer ')
buttons1[1] = button(s, Wdisp, Hdisp, 0.375, 0.44,
                     0.25, 0.08, open_multiplayer_menu1)
s = textsurf(' Main menu ')
buttons2[1] = button(s, Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, game_return)
s = textsurf('    Quit    ')
buttons1[2] = button(s, Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)
buttons2[2] = button(s, Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)
s = textsurf('Resume')
buttons2[0] = button(s, Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_resume)
# sets menues
menu1 = Menu(buttons1, screen)
menu2 = Menu(buttons2, screen)

# Меню где выбираем, создаем сервер или присоединяемся
buttons3 = [0] * 3


def create_server_menu():
    global game_st
    game_st = 4


def join_server_menu():
    global game_st
    game_st = 5


s = textsurf('Create server')
buttons3[0] = button(s, Wdisp, Hdisp, 0.375, 0.3,
                     0.25, 0.08, create_server_menu)

s = textsurf('Join server')
buttons3[1] = button(s, Wdisp, Hdisp, 0.375, 0.44,
                     0.25, 0.08, join_server_menu)


def back_to_menu():
    global game_st
    game_st = 0


s = textsurf('   Back   ')
buttons3[2] = button(s, Wdisp, Hdisp, 0.375, 0.58,
                     0.25, 0.08, back_to_menu)

menu3 = Menu(buttons3, screen)

# Меню где создаем сервер(пока нету)
buttons4 = [0] * 2
input = inputfield(Wdisp, Hdisp, 0.375, 0.30,
                   0.25, 0.08, 'Enter port')
s = textsurf('Create server')
buttons4[0] = button(s, Wdisp, Hdisp, 0.375, 0.44, 0.25,
                     0.08, multiplayer_start_create)
s = textsurf('    Back    ')
buttons4[1] = button(s, Wdisp, Hdisp, 0.375, 0.58,
                     0.25, 0.08, back_to_menu)
menu4 = Menu(buttons4, screen, [input])

# Меню где подключаемся к серверу
buttons5 = [0] * 2
input1 = inputfield(Wdisp, Hdisp, 0.375, 0.30, 0.25, 0.08, 'Enter port')
input2 = inputfield(Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, 'Enter ip')
s = textsurf('Join server')
buttons5[0] = button(s, Wdisp, Hdisp, 0.375, 0.58,
                     0.25, 0.08, multiplayer_start_join)
s = textsurf('    Back    ')
buttons5[1] = button(s, Wdisp, Hdisp, 0.375, 0.72,
                     0.25, 0.08, back_to_menu)
menu5 = Menu(buttons5, screen, [input1, input2])

start_time = time.time()
start_time_r = time.time()
counter_r = 0
game_paused = False
game_st = 0
main_screen = pygame.image.load(os.path.join(
    sys.path[0] + "\\pony\\", "main_screen.png"))
main_screen = pygame.transform.scale(main_screen, (Wdisp, Hdisp))

# main core loop
while not finished:
    clock.tick(FPS)
    # checks which of menues is opened
    if game_st == 1:
        if not multiplayer:  # Если одиночная игра то все как обычно
            input_game(pygame.event.get())
            if bill.is_shoot():
                slaves = bill.shoot(slaves, map)
        elif is_server:  # если мы сервак
            input_game(pygame.event.get())
            slaves[0].x = server.data[0]/100
            slaves[0].y = server.data[1]/100
            bill.hp = server.data[2]
            if bill.is_shoot():
                slaves = bill.shoot(slaves, map)
        elif not is_server:  # если мы клиент
            input_game(pygame.event.get())
            slaves[0].x = client.data[0]/100
            slaves[0].y = client.data[1]/100
            bill.hp = client.data[2]

            if bill.is_shoot():
                slaves = bill.shoot(slaves, map)
        update()
    if game_st == 0:
        screen.blit(main_screen, (0, 0))
        menu1.draw_all()
        menu1.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 2:
        pygame.draw.rect(screen, (233, 0, 0), (int(
            Wdisp * 0.375 - 0.1 * Hdisp), 0, int(0.25 * Wdisp + 0.2 * Hdisp), Hdisp), 0)
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
    if game_st == 4:
        screen.blit(main_screen, (0, 0))
        menu4.draw_all()
        server_info = menu4.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 5:
        screen.blit(main_screen, (0, 0))
        menu5.draw_all()
        server_info = menu5.check_all()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 1 and bill.y < 150:
        # loads video for intro
        cap = cv2.VideoCapture(os.path.join(
            sys.path[0] + "\\pony\\video\\", "Ending_video_resized.mp4"))
        success, img = cap.read()
        shape = img.shape[1::-1]

        wn = pygame.display.set_mode((Wdisp, Hdisp))
        clock = pygame.time.Clock()

        # plays intro sound
        pygame.mixer.music.load(os.path.join(
            sys.path[0] + "\\pony\\music\\", "Ending_sound.mp3"))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(1)

        game_return()
        # plays intro
        while success:
            clock.tick(30)
            success, img = cap.read()
            if (img is None):
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    success = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        success = False
            wn.blit(pygame.transform.scale(pygame.image.frombuffer(
                img.tobytes(), shape, "BGR"), (Wdisp, Hdisp)), (0, 0))
            pygame.display.update()
        pygame.mouse.set_visible(True)
        pygame.mixer.music.load(os.path.join(
            sys.path[0] + "\\pony\\music\\", "main_theme.mp3"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    # fps counter
    counter += 1
    if counter == 10:
        fps_text = font.render(
            "MAIN CORE FPS: " + str(round(counter / (time.time() - start_time))), True, (255, 255, 255))
        counter = 0
        start_time = time.time()

pygame.quit()
