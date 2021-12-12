from random import randint
import random
import math
import pygame
import sys
import os
import pygame

pygame.init()
pygame.font.init()
font = pygame.font.Font(sys.path[0]+"\\pony\\hud\\font_elec.ttf", 40)

infoObject = pygame.display.Info()
W, H = infoObject.current_w, infoObject.current_h

class gun:
    def __init__(self, auto, maxammo, fire, idle, reload, reload_sound, fire_sound, screen_x, screen_y, scale, frame_time):
        self.screen_x = screen_x
        self.screen_y = screen_y

        self.sleeve_posx = screen_x
        self.sleeve_posy = screen_y

        self.auto = auto
        self.maxammo = maxammo
        self.ammo = maxammo
        self.frame_time = frame_time
        self.scale = scale

        self.sleeve = []
        self.sleeve.append(pygame.image.load(sys.path[0]+"\\pony\\weapon\\sleeve0.png"))
        self.sleeve.append(pygame.image.load(sys.path[0]+"\\pony\\weapon\\sleeve1.png"))
        self.sleeve.append(pygame.image.load(sys.path[0]+"\\pony\\weapon\\sleeve2.png"))

        self.sleeve_x = 0
        self.sleeve_y = 0

        self.fire_texture = fire
        self.idle_texture = idle
        self.reload_texture = reload

        self.fire_length = len(fire)
        self.reload_length = len(reload)

        for i in range(self.fire_length):
            new_w = self.fire_texture[i].get_width() * self.scale
            new_h = self.fire_texture[i].get_height() * self.scale
            self.fire_texture[i] = pygame.transform.scale(self.fire_texture[i], (new_w, new_h))
        for i in range(self.reload_length):
            new_w = self.reload_texture[i].get_width() * self.scale
            new_h = self.reload_texture[i].get_height() * self.scale
            self.reload_texture[i] = pygame.transform.scale(self.reload_texture[i], (new_w, new_h))
        new_w = self.idle_texture.get_width() * self.scale
        new_h = self.idle_texture.get_height() * self.scale
        self.idle_texture = pygame.transform.scale(self.idle_texture, (new_w, new_h))


        self.frame_counter = 0
        self.counter = 0

        self.fire_sound = fire_sound
        self.reload_sound = reload_sound

        self.reloading = False
        self.shooting = False

        self.last_frames = False

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.frame_counter == 0 and self.ammo != self.maxammo:
                self.reloading = True
                self.frame_counter = self.reload_length
                self.counter = 0
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.reload_sound))
                pygame.mixer.Channel(1).set_volume(2)
        if event.type == pygame.MOUSEBUTTONDOWN and self.frame_counter == 0 and self.ammo > 0 and not self.last_frames:
            self.sleeve_x = self.sleeve_y = 0
            self.shooting = True
            self.frame_counter = self.fire_length
            self.counter = 0
        if event.type == pygame.MOUSEBUTTONUP and self.auto and self.shooting:
            self.shooting = False
            self.last_frames = True


    def update(self):
        self.counter += 1

        if self.ammo == 0 and not self.reloading and self.frame_counter == 0: # Если кончились патроны
            self.reloading = True
            self.last_frames = False
            self.frame_counter = self.reload_length
            self.counter = 0
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.reload_sound))
            pygame.mixer.Channel(1).set_volume(2)

        if self.frame_counter > 0 and self.reloading: # Если в процессе перезарядки
            if self.counter % self.frame_time == 0:
                self.frame_counter -= 1

            if self.frame_counter == 0:
                self.ammo = self.maxammo

        if self.frame_counter > 0 and (self.shooting or self.last_frames): # Если в процессе стрельбы
            if self.counter % self.frame_time == 0:
                self.frame_counter -= 1

        if self.frame_counter == self.fire_length and self.shooting and self.counter == 1: # Только что выстрелили
            self.ammo -= 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(self.fire_sound))
            pygame.mixer.Channel(1).set_volume(2)


        if not self.shooting and not self.reloading and self.auto and not self.last_frames:
            self.frame_counter = 0

        if self.frame_counter == 0: # Анимация чего-либо закончилась
            if self.shooting and not self.auto:
                self.shooting = False
            if self.shooting and self.auto and self.ammo > 0:
                self.frame_counter = self.fire_length
                self.counter = 0
                self.sleeve_x = self.sleeve_y = 0

            if self.shooting and self.auto and self.ammo == 0:
                self.shooting = False

            self.last_frames = False
            self.reloading = False
            


    def draw(self, screen, Tx, Ty):
        screen_pos = (round(screen.get_width()*self.screen_x + math.sin(Tx)*20), round(screen.get_height()*self.screen_y + math.cos(Ty)*20))
        if self.frame_counter > 0 and (self.shooting or self.last_frames):
            screen.blit(self.fire_texture[self.fire_length - self.frame_counter], screen_pos)
        elif self.frame_counter > 0 and self.reloading:
            screen.blit(self.reload_texture[self.reload_length - self.frame_counter], screen_pos)
        else:
            screen.blit(self.idle_texture, screen_pos)

        if self.shooting or self.last_frames:
            self.sleeve_x += 25
            self.sleeve_y -= 10
            screen.blit(self.sleeve[self.frame_counter%3], (round(self.sleeve_posx * screen.get_width() + self.sleeve_x), round(self.sleeve_posy * screen.get_height() + self.sleeve_y)))


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

        self.speed = 1
        self.sens = 2000
        self.z = 1
        self.Tx = 0
        self.Ty = 0

        self.kw = False
        self.ks = False
        self.ka = False
        self.kd = False

        # Загрузка текстурок для худа и прочего
        self.bullet = pygame.image.load(sys.path[0]+"\\pony\\hud\\bullet.png")
        self.bullet.set_colorkey((0, 0, 0))

        self.hp_bar = pygame.image.load(sys.path[0]+"\\pony\\hud\\hp_bar.png")

        self.ammo_bar = pygame.image.load(sys.path[0]+"\\pony\\hud\\ammo_bar.png")

        self.scope = pygame.image.load(sys.path[0]+"\\pony\\hud\\scope.png")
        self.scope = pygame.transform.rotozoom(self.scope, 0, 0.5)

        self.hitmark = pygame.image.load(sys.path[0]+"\\pony\\hud\\hitmark.png")
        self.hitmark = pygame.transform.rotozoom(self.hitmark, 0, 0.1)


        def load(arr,name):
            '''
            arr - array in which pictures are loaded
            name - files folder
            '''
            path = os.path.join(sys.path[0],name)
            print(path)
            files = next(os.walk(path))
            onlyfiles = next(os.walk(path)) 
            for i in range(len(onlyfiles[2])):
                print(files[0]+"\\"+onlyfiles[2][i])
                arr.append(pygame.image.load(files[0]+"\\"+"("+str(i+1)+").png").convert_alpha())
            return arr
        
        def load_gun(folder,args):
            idle = pygame.image.load(sys.path[0]+"\\pony\\weapon\\"+folder+"\\idle.png")
            shoot1 = []
            shoot1 = load(shoot1,"pony\\weapon\\"+folder+"\\shoot")
            reload1 = []
            reload1 = load(reload1,"pony\\weapon\\"+folder+"\\reload")
            reload_sound = pygame.mixer.Sound(sys.path[0]+"\\pony\\weapon\\"+folder+"\\reload.mp3")
            shoot_sound = pygame.mixer.Sound(sys.path[0]+"\\pony\\weapon\\"+folder+"\\shoot.mp3")
            gun_ = gun(args[0], args[1], shoot1, idle, reload1, reload_sound, shoot_sound, args[2], args[3], args[4], args[5])
            gun_.sleeve_posx = args[6]
            gun_.sleeve_posy = args[7]
            return gun_
        
        scale = W/1536

        self.ak = load_gun("ak",(True,30,0.4*scale,0.13*scale,1,2,1,1))
        self.svt = load_gun("svt",(False,10,0.3*scale,0.13*scale,1,2,0.82,0.77))
        self.pm = load_gun("makarov",(False,8,0.3*scale,0.13*scale,1,2,0.62,0.67))
        
        self.pm.sleeve_posx = 0.82

        self.WEAPONS = [self.ak, self.svt,self.pm]
        self.CURRENT_WEAPON = 0


        # Создание миникарты
        self.res = 20
        self.minimap = pygame.Surface((len(self.map[0])*self.res + 200, len(self.map)*self.res + 200))
        for i in range(len(self.map[0])):
            for j in range(len(self.map)):
                if self.map[i][j] != 0:
                    pygame.draw.rect(self.minimap, (100, 100, 100), (i*self.res + 100, j*self.res + 100, self.res, self.res))
        self.minimap_circle = pygame.image.load(sys.path[0]+"\\pony\\hud\\minimap.png")

    def is_shoot(self):
        if self.WEAPONS[self.CURRENT_WEAPON].shooting and self.WEAPONS[self.CURRENT_WEAPON].frame_counter == self.WEAPONS[self.CURRENT_WEAPON].fire_length:
            self.z += 0.05  # РАЗКОММЕНТИТЬ ДЛЯ ОТДАЧИ
            self.a += (random.random() - 0.5)/10
            return True
        else:
            return False

    def Rotate(self, a):
        self.a = self.a + a
        global move
        move = True

    def Move(self, l, n, slaves):
        a = self.a
        x_ = self.x - l * math.sin(math.pi - a) + n * math.cos(a)
        y_ = self.y - l * math.cos(math.pi - a) + n * math.sin(a)

        delta_x = (x_ - self.x) * 2
        delta_y = (y_ - self.y) * 2


        logic = 1
        for i in range(len(slaves)):
            if math.sqrt((slaves[i].x - x_ / 100) ** 2 + (slaves[i].y - y_ / 100) ** 2) <= 0.8 and slaves[
                i].lifes >= 1:
                logic = 0
        if logic == 1:
            new_tile_coords = [int((y_ + delta_y)/ 100), int((x_ + delta_x) / 100)]
            old_tile_coords = [int(self.y / 100), int(self.x / 100)]
            if self.map[new_tile_coords[0]][new_tile_coords[1]] == 0:
                self.y = y_
                self.x = x_
            elif self.map[new_tile_coords[0]][old_tile_coords[1]] == 0:
                self.y = y_
            elif self.map[old_tile_coords[0]][new_tile_coords[1]] == 0:
                self.x = x_
        
        self.Ty += 0.2
        self.Tx += 0.1


    def check_fisting(self,slaves):
        x,y = self.x/self.stepx,self.y/self.stepy
        for i in range(0,len(slaves),3):
            if abs(slaves[i]-x)<0.3 and abs(slaves[i+1]-y)<0.3:
                print(slaves[i+2])


    def update(self, slaves):
        self.a = self.a % self.pi_2
        
        self.Rotate((-W / 2 + pygame.mouse.get_pos()[0]) / self.sens)
        
        self.z -= (-H / 2 + pygame.mouse.get_pos()[1]) / self.sens
        self.z = min(self.z,1.5)
        self.z = max(self.z,0.5)
        pygame.mouse.set_pos((W // 2, H // 2))

        self.WEAPONS[self.CURRENT_WEAPON].update()

        if self.kw:
            self.Move(0, 3 * self.speed, slaves)
        if self.ks:
            self.Move(0, -3 * self.speed, slaves)
        if self.ka:
            self.Move(-3 * self.speed, 0, slaves)
        if self.kd:
            self.Move(3 * self.speed, 0, slaves)


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
            if event.key == pygame.K_1:
                if len(self.WEAPONS) > 0:
                    self.CURRENT_WEAPON = 0
            if event.key == pygame.K_2:
                if len(self.WEAPONS) > 1:
                    self.CURRENT_WEAPON = 1
            if event.key == pygame.K_3:
                if len(self.WEAPONS) > 2:
                    self.CURRENT_WEAPON = 2
            if event.key == pygame.K_4:
                if len(self.WEAPONS) > 3:
                    self.CURRENT_WEAPON = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.kw = False
            if event.key == pygame.K_s:
                self.ks = False
            if event.key == pygame.K_a:
                self.ka = False
            if event.key == pygame.K_d:
                self.kd = False

        self.WEAPONS[self.CURRENT_WEAPON].input(event)


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
        text = font.render(str(round(self.WEAPONS[self.CURRENT_WEAPON].ammo)), True, (80, 80, 80))
        text_red = font.render(str(round(self.WEAPONS[self.CURRENT_WEAPON].ammo)), True, (110, 30, 30))
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

        self.WEAPONS[self.CURRENT_WEAPON].draw(screen, self.Tx, self.Ty)

    def shoot(self, slaves, map):
        a = self.a

        maxR = self.maxR
        find = False
        dl = self.dl

        x = self.x / self.stepx
        y = self.y / self.stepy

        dcos = math.cos(a) * dl
        dsin = math.sin(a) * dl

        l = 0
        
        while not find and l < maxR:

            if map[int(y)][int(x)] > 0:
                find = True
                break
            else:
                for j in range(len(slaves)):
                    r = math.sqrt((slaves[j].x-self.x/100)**2 + (slaves[j].y-self.y/100)**2)
                    z_2 = (slaves[j].x - x) ** 2 + (slaves[j].y - y) ** 2

                    if z_2 < 0.01 and slaves[j].lifes != -1 and (-self.z - 0.9/r) < -1 and (self.z - 0.3/r) < 1:
                        find = True
                        slaves[j].lifes -= 1
                        if (self.z - 0.1/r) > 1:
                            slaves[j].lifes -= 1
                        self.hitmark_counter = 15
                        break

            l = dl + l
            x = x + dcos
            y = y + dsin
        return slaves

