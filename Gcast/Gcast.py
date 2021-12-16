import math
import os
import sys
import time
from random import randint
from threading import Thread
import cv2
import pygame
import mazeG
from billy import billy
from online import Client, Server
from render import rendering
from slave import slave
from menu_create import create_menus

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

me_shoot = 0
last_enemy_coords_x = 0
last_enemy_coords_y = 0

# init some stuff for printing out stats
pygame.font.init()
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(os.path.join(
    sys.path[0] + "\\ttf\\", "MAGNETOB.ttf"), 40)
fps_text = font.render("FPS: ", True, (255, 255, 255))
fps_text_r = font.render("FPS: ", True, (255, 255, 255))
# FPS core timer
counter = 0

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
    screen.blit(final_render, (math.sin(bill.x) *
                0 - 0, math.cos(bill.Ty) * 0 - 0))
    thread_draw_stuff = Thread(target=draw_stuff, args=())
    thread_draw_stuff.start()

# def which is called by render core and updates render data


def update_render():
    global u, enemies, map
    a = bill.a
    x0, y0 = bill.x, bill.y
    return map, enemies, math.cos(a - u), math.sin(a - u), math.cos(a + u), math.sin(
        a + u), 0.15, 7, bill.x, bill.y, bill.z


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
    if multiplayer:
        if len(slaves) > 0:
            slaves[0].walk(map, bill.x, bill.y, [], 0, True)
            
            if slaves[0].death(bill.x,bill.y):
                slaves[0] = slave(randint(0, 2), 1.5, 1.5, 100, 100)
                

    for i in range(len(slaves)):
        if not multiplayer:
            if slaves[i - l].walk(map, bill.x, bill.y, slaves, i-l, False):
                bill.hp -= 0.5
        enemies += ((slaves[i - l].x, slaves[i - l].y,
                     slaves[i - l].type, slaves[i - l].frame))

        if (slaves[i - l].death(bill.x, bill.y)):
            del (slaves[i - l])
            l += 1


def start():
    # loads global variables
    global pe, height, width, W, H, density, dl
    # creates maze

    mazeG.main(height, width)
    map_ = mazeG.maze.copy()
    mazeG.maze = tuple(tuple(i) for i in mazeG.maze)
    # spawns slaves
    map = mazeG.maze
    slaves = []
    for i in range(height * width // 2):
        x, y = randint(3, height - 1) + 0.5, randint(3, width - 1) + 0.5
        if map_[int(y)][int(x)] == 0:
            map_[int(y)][int(x)] += 1
            slaves.append(slave(randint(0, 2), x, y, 100, 100))
    # inits render core

    rend = rendering(0.5, density, dl, render_zone, height +
                     2, width + 2, update_render, redraw_all, 1)
    # creates bill
    bill = billy((width - 1) * 100 + 40, height * 100 + 40,
                 2 * math.pi / 2, "VAn", W, H, map)
    if map[int(bill.y / 100)][int(bill.x / 100)] != 0:
        bill = billy((width - 2) * 100 + 40, height * 100 + 40,
                     3 * math.pi / 2, "VAn", W, H, map)
    # returns new variables
    return rend, bill, map, slaves


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


def multiplayer_start_create():
    global server_info
    global game_st, W, H
    global rend, bill, slaves, map
    global Tx, Ty
    global multiplayer
    global server
    global is_server
    global enemies

    multiplayer, is_server = True, True
    rend, bill, map, slaves, Tx, Ty = 0, 0, 0, 0, 0, 0

    map = [[1, 5, 5, 5, 5, 5, 5, 5, 5, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 2, 2, 0, 0, 2, 2, 0, 1], [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 3, 3, 0, 0, 0, 0, 3, 3, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
           [1, 0, 2, 2, 0, 0, 2, 2, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 4, 4, 4, 4, 4, 4, 4, 4, 1]]
    map = tuple(tuple(i) for i in map)
    rend = rendering(0.5, density, dl, render_zone, len(
        map), len(map[0]), update_render, redraw_all, 1)
    bill = billy((len(map[0])-2) * 100 + 40, (len(map)-2)
                 * 100 + 40, 2 * math.pi / 2, "VAn", W, H, map)

    slaves = [slave(randint(0, 2), 150, 150, 100, 100)]

    server = Server(2, int(server_info[0]), map, 150, 150,
                    delegate_data)  # Создаем сервак и отправляем сразу карту
    # и координаты спавна врага
    print("server created")
    slaves[0].lifes = 100
    update()
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()

    if not server.is_alive():
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

    slaves = []  # Готовим массив для врага
    slaves.append(
        slave(randint(0, 2), (width - 1) * 100 + 40, height * 100 + 40, 100, 100))  # Создаем врага, владелец сервака
    # всегда спавнится в начале лабиринта
    # подключаемся к серваку
    client = Client(server_info[1], int(server_info[0]), delegate_data)

    map = client.map  # запоминаем карту по инфе с сервака
    rend = rendering(0.5, density, dl, render_zone, len(
        map), len(map[0]), update_render, redraw_all, 1)
    bill = billy(client.start_x, client.start_x,
                 2 * math.pi / 2, "VAn", W, H, map)  # создаем игрока по координатам от сервака

    bill.map = map
    slaves[0].lifes = 100
    update()

    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()
    if not client.is_alive():
        client.start()

# def which sends data to online


def delegate_data():
    global me_shoot

    if len(slaves) > 0:
        if me_shoot == 1:
            me_shoot = 0
            return bill.x, bill.y, slaves[0].lifes, 1, bill.moving
        else:
            return bill.x, bill.y, slaves[0].lifes, 0, bill.moving
    else:
        return 0, 0, 0, 0, 0


def game_finish():
    global finished
    finished = True


def game_resume():
    global game_paused
    game_paused = game_reset_mode(game_paused)


def back_to_menu():
    global game_st
    game_st = 0


def open_multiplayer_menu1():
    global game_st
    game_st = 3


def create_server_menu():
    global game_st
    game_st = 4


def join_server_menu():
    global game_st
    game_st = 5


def game_return():
    global game_st
    game_st = 0
    if multiplayer:
        if is_server == True:
            server.stop()
            server.join()
        else:
            client.stop()
            client.join()
    pygame.mouse.set_visible(True)
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


# starts out game and inits parametrs
pygame.init()

infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h
Wdisp, Hdisp = infoObject.current_w, infoObject.current_h
render_zone = pygame.Surface((700, 200))

# sets white and black
wh = (255, 255, 255)
bl = (0, 0, 0)

# plays intro sound
pygame.mixer.music.load(os.path.join(
    sys.path[0] + "\\pony\\music\\", "Intro_sound.mp3"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)


# plays intro
# loads video for intro
cap = cv2.VideoCapture(os.path.join(
    sys.path[0] + "\\pony\\video\\", "Intro_video_resized.mp4"))
success, img = cap.read()
shape = img.shape[1::-1]
wn = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
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


start_time = time.time()
start_time_r = time.time()
counter_r = 0
game_paused = False
game_st = 0

main_screen = pygame.image.load(os.path.join(
    sys.path[0] + "\\pony\\", "main_screen.png"))
main_screen = pygame.transform.scale(main_screen, (Wdisp, Hdisp))


menu1, menu2, menu3, menu4, menu5 = create_menus(screen, game_start, game_finish, game_return, game_resume, multiplayer_start_join,
                                                 multiplayer_start_create, back_to_menu, open_multiplayer_menu1, create_server_menu, join_server_menu)

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

            if len(slaves) > 0:
                slaves[0].x = server.data[0]/100
                slaves[0].y = server.data[1]/100

                bill.hp = server.data[2]
                is_enemy_shooting = server.data[3]*2
                is_enemy_moving = server.data[4]

                if is_enemy_shooting == 2:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound(
                        os.path.join(sys.path[0], "pony\\music\\enemy3_shoot.mp3")))
                    pygame.mixer.Channel(2).set_volume(1)

                slaves[0].state = max(is_enemy_moving, is_enemy_shooting)

                if bill.is_shoot():
                    slaves = bill.shoot(slaves, map)
                    me_shoot = 1
        elif not is_server:  # если мы клиент
            input_game(pygame.event.get())
            if len(slaves) > 0:
                slaves[0].x = client.data[0] / 100
                slaves[0].y = client.data[1] / 100

                bill.hp = client.data[2]
                is_enemy_shooting = client.data[3]*2
                is_enemy_moving = client.data[4]

                slaves[0].state = max(is_enemy_moving, is_enemy_shooting)

                if is_enemy_shooting == 2:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound(
                        os.path.join(sys.path[0], "pony\\music\\enemy3_shoot.mp3")))
                    pygame.mixer.Channel(2).set_volume(1)

                if bill.is_shoot():
                    slaves = bill.shoot(slaves, map)
                    me_shoot = 1
        if not bill.died or multiplayer:
            update()
        else:
            game_st = 0
            game_return()
    if game_st == 0:
        screen.blit(main_screen, (0, 0))
        menu1.run()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 2:
        pygame.draw.rect(screen, (233, 0, 0), (int(
            Wdisp * 0.375 - 0.1 * Hdisp), 0, int(0.25 * Wdisp + 0.2 * Hdisp), Hdisp), 0)
        menu2.run()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 3:
        screen.blit(main_screen, (0, 0))
        menu3.run()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 4:
        screen.blit(main_screen, (0, 0))
        server_info = menu4.run()
        input_menu(pygame.event.get())
        pygame.display.update()
    if game_st == 5:
        screen.blit(main_screen, (0, 0))
        server_info = menu5.run()
        input_menu(pygame.event.get())
        pygame.display.update()

    if game_st == 1 and bill.y < 150 and not multiplayer:
        # loads video for intro
        cap = cv2.VideoCapture(os.path.join(
            sys.path[0] + "\\pony\\video\\", "Ending_video_resized.mp4"))
        success, img = cap.read()
        shape = img.shape[1::-1]

        ending_time = 0
        h = -3330
        file = os.path.join(sys.path[0] + "\\pony\\", "titles.txt")
        titles = []
        with open(os.path.join(sys.path[0] + "\\pony\\", "titles.txt")) as file:
            inp = open(os.path.join(
                sys.path[0] + "\\pony\\", "titles.txt"), 'r')
            while True:
                line = inp.readline()
                line = line.replace('\n', ' ')
                s = pygame.Surface((Wdisp, 90), pygame.SRCALPHA)
                myfont = pygame.font.SysFont('arial', 60)
                textsurface = myfont.render(line, False, (125, 125, 125))
                u1 = myfont.size(line)
                s.blit(textsurface, (int((Wdisp - u1[0])/2), 0))
                titles.append(s)
                if not line:
                    break

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
            if ending_time >= 1900:
                for i in range(len(titles)):
                    screen.blit(titles[i], (0, h + 90*i))
                h += 2
            pygame.display.update()
            ending_time += 1
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
