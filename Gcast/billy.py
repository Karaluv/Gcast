from random import randint
import math
import pygame
import sys
import os
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.Font("pony\\hud\\font_elec.ttf", 40)

infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h

class billy:
    def __init__(self, x, y, a, name, W, H, map):
        self.map = map
        self.x = x
        self.y = y
        self.a = a
        self.name = name

        self.hitmark_counter = 0
        self.hp = 100

        self.W = W
        self.H = H

        self.maxR = 7
        self.dl = 0.01

        self.stepx = 100
        self.stepy = 100

        self.pi_2 = math.pi * 2

        self.makarov = []

        self.shoot_frame = 0

        self.max_shoot_frame = 8

        self.shoot_speed = 0.5

        self.B_shoot = False
        self.B_reload = False

        self.reload_frame = 0

        self.max_reload_frame = 42

        self.reload_speed = 0.5

        self.ammo = 8

        self.max_ammo = 8

        self.speed = 1
        self.sens = 2000

        self.Tx = 0
        self.Ty = 0

        self.kw = False
        self.ks = False
        self.ka = False
        self.kd = False

        self.bullet = pygame.image.load("pony\\hud\\bullet.png")
        self.bullet.set_colorkey((0, 0, 0))

        self.hp_bar = pygame.image.load("pony\\hud\\hp_bar.png")

        self.ammo_bar = pygame.image.load("pony\\hud\\ammo_bar.png")

        self.scope = pygame.image.load("pony\\hud\\scope.png")
        self.scope = pygame.transform.rotozoom(self.scope, 0, 0.5)

        self.hitmark = pygame.image.load("pony\\hud\\hitmark.png")
        self.hitmark = pygame.transform.rotozoom(self.hitmark, 0, 0.1)

        self.makarov.append([])
        path = os.path.join(sys.path[0], "pony\\weapon\\makarov\\stay")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path))
        # print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            self.makarov[-1].append(pygame.image.load(files[0] + "\\" + onlyfiles[2][i]).convert_alpha())

        self.makarov.append([])
        path = os.path.join(sys.path[0], "pony\\weapon\\makarov\\shoot")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path))
        # print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            self.makarov[-1].append(pygame.image.load(files[0] + "\\(" + str(i + 1) + ").png").convert_alpha())

        self.makarov.append([])
        path = os.path.join(sys.path[0], "pony\\weapon\\makarov\\reload")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path))
        # print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            self.makarov[-1].append(pygame.image.load(files[0] + "\\ (" + str(i + 1) + ").png").convert_alpha())

        self.res = 20
        self.minimap = pygame.Surface((len(self.map[0])*self.res + 200, len(self.map)*self.res + 200))
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if self.map[i][j] != 0:
                    pygame.draw.rect(self.minimap, (100, 100, 100), (i*self.res + 100, j*self.res + 100, self.res, self.res))


        self.minimap_circle = pygame.image.load("pony\\hud\\minimap.png")


    def Rotate(self, a):
        self.a = self.a + a
        global move
        move = True

    def Move(self, l, n):
        a = self.a
        x_ = self.x - l * math.sin(math.pi - a) + n * math.cos(a)
        y_ = self.y - l * math.cos(math.pi - a) + n * math.sin(a)

        if self.map[int(y_ / 100 + 0.05)][int(x_ / 100 + 0.05)] == 0:
            if self.map[int(y_ / 100 - 0.05)][int(x_ / 100 - 0.05)] == 0:
                if self.map[int(y_ / 100 - 0.05)][int(x_ / 100 + 0.05)] == 0:
                    if self.map[int(y_ / 100 + 0.05)][int(x_ / 100 - 0.05)] == 0:
                        self.y = y_
                        self.x = x_


        self.Ty += 0.2
        self.Tx += 0.1


    def check_fisting(self,slaves):
        x,y = self.x/self.stepx,self.y/self.stepy
        for i in range(0,len(slaves),3):
            if abs(slaves[i]-x)<0.3 and abs(slaves[i+1]-y)<0.3:
                print(slaves[i+2])


    def update(self):
        self.a = self.a % self.pi_2
        
        self.Rotate((-W / 2 + pygame.mouse.get_pos()[0]) / self.sens)
        pygame.mouse.set_pos((W // 2, H // 2))

        if self.shoot_frame > 0:
            self.shoot_frame += self.shoot_speed
            if self.shoot_frame >= self.max_shoot_frame - 1:
                self.shoot_frame = 0
                self.B_shoot = False
        elif self.reload_frame > 0:
            self.reload_frame += self.reload_speed
            if self.reload_frame >= self.max_reload_frame - 1:
                self.reload_frame = 0
                self.B_reload = False
                self.ammo = self.max_ammo
        if self.kw:
            self.Move(0, 3 * self.speed)
        if self.ks:
            self.Move(0, -3 * self.speed)
        if self.ka:
            self.Move(-3 * self.speed, 0)
        if self.kd:
            self.Move(3 * self.speed, 0)

       

    def keyinput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.kw = True
            if event.key == pygame.K_s:
                self.ks = True
            if event.key == pygame.K_a:
                self.ka = True
            if event.key == pygame.K_d:
                self.kd = True
            if event.key == pygame.K_r and self.ammo < self.max_ammo:
                self.reload()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.kw = False
            if event.key == pygame.K_s:
                self.ks = False
            if event.key == pygame.K_a:
                self.ka = False
            if event.key == pygame.K_d:
                self.kd = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shoot_frame == 0 and not self.B_reload:
                self.shoot_frame = 1
                return True

        return False

    def draw(self, screen):
        minimap_small = pygame.Surface.copy(self.minimap.subsurface((self.y/100*self.res, self.x/100*self.res, 200, 200)))
        minimap_small = pygame.transform.flip(minimap_small, False, True)
        minimap_rotated = pygame.Surface.copy(pygame.transform.rotozoom(pygame.Surface.copy(minimap_small), self.a * 180/ math.pi, 1))
        blit_coord = 200 * (1 - abs(math.sin(self.a)) - abs(math.cos(self.a)))/2

        minimap_rotated.blit(self.minimap_circle, (-blit_coord, -blit_coord))
        minimap_rotated.set_colorkey((0, 0, 0))
        surface = pygame.Surface((200, 200))
        surface.blit(minimap_rotated, (blit_coord, blit_coord))
        surface.set_alpha(200)
        surface.set_colorkey((0, 0, 0))

        screen.blit(surface, (screen.get_width() - 200, 0))

        pygame.draw.circle(screen, (255, 0, 0), (screen.get_width() - 100, 100), 5)
        pygame.draw.circle(screen, (100, 100, 100), (screen.get_width() - 100, 100), 102, 4)

        W, H = self.W, self.H

        #text = font.render("Ammo: " + str(self.ammo), True, (255, 255, 255))
        #screen.blit(text, (30, 90))
        hp_bar_y = screen.get_height() - self.hp_bar.get_height()
        screen.blit(self.hp_bar, (20, hp_bar_y))
        text = font.render(str(round(self.hp)), True, (80, 80, 80))
        text_red = font.render(str(round(self.hp)), True, (110, 30, 30))
        text_x = 20 + (self.hp_bar.get_width() - text.get_width())/2
        screen.blit(text, (text_x + 2, hp_bar_y + (self.hp_bar.get_height() - text.get_height())/2 + 2))
        screen.blit(text_red, (text_x, hp_bar_y + (self.hp_bar.get_height() - text.get_height()) / 2))


        ammo_bar_y = screen.get_height() - self.ammo_bar.get_height()
        screen.blit(self.ammo_bar, (25 + self.hp_bar.get_width(), ammo_bar_y))
        text = font.render(str(round(self.ammo)), True, (80, 80, 80))
        text_red = font.render(str(round(self.ammo)), True, (110, 30, 30))
        text_x = 25 + self.hp_bar.get_width() + (self.ammo_bar.get_width() - text.get_width()) / 2
        screen.blit(text, (text_x + 2, hp_bar_y + (self.ammo_bar.get_height() - text.get_height()) / 2 + 2))
        screen.blit(text_red, (text_x, hp_bar_y + (self.ammo_bar.get_height() - text.get_height()) / 2))

        screen.blit(self.scope, ((screen.get_width() - self.scope.get_width())/2, (screen.get_height() - self.scope.get_height())/2))
        if self.hitmark_counter > 0:
            screen.blit(self.hitmark, (
            (screen.get_width() - self.scope.get_width()) / 2, (screen.get_height() - self.scope.get_height()) / 2))
            self.hitmark_counter -= 1
        #for i in range(self.ammo):
        #    screen.blit(self.bullet, (30 + self.bullet.get_width()*i, 130))

        if self.B_shoot:
            screen.blit(self.makarov[1][int(self.shoot_frame - 1)], (
                screen.get_width() // 2 * 1.2 - self.makarov[0][0].get_width() // 2,
                screen.get_height() - self.makarov[0][0].get_height()))
        elif self.B_reload:
            if self.reload_frame == 7:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\weapon\\makarov\\reload.mp3")))
                pygame.mixer.Channel(1).set_volume(2)
            screen.blit(self.makarov[2][int(self.reload_frame - 1)], (
                screen.get_width() // 2 * 1.2 - self.makarov[0][0].get_width() // 2,
                screen.get_height() - self.makarov[0][0].get_height()))
        else:
            screen.blit(self.makarov[0][0], (screen.get_width() // 2 * 1.2 - self.makarov[0][0].get_width() // 2,
                                             screen.get_height() - self.makarov[0][0].get_height()))


    def reload(self):
        self.ammo = 0
        self.reload_frame = 1
        self.B_reload = True


    def shoot(self, slaves, map):
        a = self.a

        maxR = self.maxR
        find = False
        dl = self.dl

        x = self.x / self.stepx
        y = self.y / self.stepy

        dcos = math.cos(a) * dl
        dsin = math.sin(a) * dl

        pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\weapon\\makarov\\shoot.mp3")))
        pygame.mixer.Channel(1).set_volume(2)

        l = 0

        self.ammo -= 1
        self.B_shoot = True
        if self.ammo == 0:
            self.reload()

        while not find and l < maxR:

            if map[int(y)][int(x)] > 0:
                find = True
                break
            else:
                for j in range(len(slaves)):
                    z_2 = (slaves[j].x - x) ** 2 + (slaves[j].y - y) ** 2

                    if z_2 < 0.01:
                        find = True
                        del slaves[j]
                        self.hitmark_counter = 15
                        break

            l = dl + l
            x = x + dcos
            y = y + dsin
        return slaves

