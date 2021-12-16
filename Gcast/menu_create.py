import os
import sys
import pygame
from buttons import button, inputfield, just_text
from menu import Menu

font1 = pygame.font.Font(os.path.join(
    sys.path[0] + "\\ttf\\", "MAGNETOB.ttf"), 40)


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


def create_menus(screen, game_start, game_finish, game_return, game_resume, multiplayer_start_join,
                 multiplayer_start_create):
    # gets display size
    Wdisp, Hdisp = screen.get_size()
    # creates arrays of buttons
    buttons1 = [0] * 3
    buttons2 = [0] * 3

    # sets buttons for menues

    buttons1[0] = button(textsurf(' Singleplayer '), Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_start)

    buttons1[1] = button(textsurf(' Multiplayer '), Wdisp, Hdisp, 0.375, 0.44,
                         0.25, 0.08, open_multiplayer_menu1)

    buttons2[1] = button(textsurf(' Main menu '), Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, game_return)

    buttons1[2] = button(textsurf('    Quit    '), Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)
    buttons2[2] = button(textsurf('    Quit    '), Wdisp, Hdisp, 0.375, 0.58, 0.25, 0.08, game_finish)

    buttons2[0] = button(textsurf('Resume'), Wdisp, Hdisp, 0.375, 0.3, 0.25, 0.08, game_resume)
    # sets menues
    menu1 = Menu(buttons1, screen)
    menu2 = Menu(buttons2, screen)

    # Меню где выбираем, создаем сервер или присоединяемся
    buttons3 = [0] * 3

    buttons3[0] = button(textsurf('Create server'), Wdisp, Hdisp, 0.375, 0.3,
                         0.25, 0.08, create_server_menu)

    buttons3[1] = button(textsurf('Join server'), Wdisp, Hdisp, 0.375, 0.44,
                         0.25, 0.08, join_server_menu)

    buttons3[2] = button(textsurf('   Back   '), Wdisp, Hdisp, 0.375, 0.58,
                         0.25, 0.08, back_to_menu)

    menu3 = Menu(buttons3, screen)

    # Меню где создаем сервер(пока нету)
    buttons4 = [0] * 2
    input = inputfield(Wdisp, Hdisp, 0.375, 0.30,
                       0.25, 0.08, 'Enter port')

    buttons4[0] = button(textsurf('Create server'), Wdisp, Hdisp, 0.375, 0.44, 0.25,
                         0.08, multiplayer_start_create)

    buttons4[1] = button(textsurf('    Back    '), Wdisp, Hdisp, 0.375, 0.58,
                         0.25, 0.08, back_to_menu)
    menu4 = Menu(buttons4, screen, [input])

    # Меню где подключаемся к серверу
    buttons5 = [0] * 2
    input1 = inputfield(Wdisp, Hdisp, 0.375, 0.30, 0.25, 0.08, 'Enter port')
    input2 = inputfield(Wdisp, Hdisp, 0.375, 0.44, 0.25, 0.08, 'Enter ip')

    buttons5[0] = button(textsurf('Join server'), Wdisp, Hdisp, 0.375, 0.58,
                         0.25, 0.08, multiplayer_start_join)

    buttons5[1] = button(textsurf('    Back    '), Wdisp, Hdisp, 0.375, 0.72,
                         0.25, 0.08, back_to_menu)
    menu5 = Menu(buttons5, screen, [input1, input2])

    return menu1, menu2, menu3, menu4, menu5
