import math
import pygame
import os
import sys
from random import randint


class slave:

    def __init__(self,type,x,y,stepx,stepy):

        self.type = type
        self.x = x
        self.y = y
        self.v = 2
        self.rotation = randint(0,10)/10*math.pi*2
        self.stepx = stepx
        self.stepy = stepy
        self.r0 = 2
        self.targetting_time = 30

        self.lifes = 2
        self.state = 1

        self.see = True
        if type == 0:
            self.maxFrame = 16
            self.speed_animation = 0.2
            self.shootingframe = 10
            self.lifes = 4
        if type == 1:
            self.maxFrame = 17
            self.speed_animation = 0.2
            self.shootingframe = 13
            self.lifes = 6
        if type == 2:
            self.maxFrame = 13
            self.speed_animation = 0.2
            self.shootingframe = 9
            self.lifes = 8

        self.start_frame = 0
        self.frame = randint(0,self.maxFrame)
        
    def death(self, x0, y0):
        if self.lifes == 0:
            self.v = 0
            x0 /= 100
            y0 /= 100
            r = math.sqrt((x0-self.x)*(x0-self.x) + (y0-self.y)*(y0-self.y))
            if self.type == 0:
                self.start_frame = 17
                self.maxFrame = 21
                pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\music\\slave_1_death_sound.mp3")))
                if r < 2:
                    pygame.mixer.Channel(3).set_volume(1)
                elif r < 4:
                    pygame.mixer.Channel(3).set_volume(0.6)
                else:
                    pygame.mixer.Channel(3).set_volume(0.3)
            if self.type == 1:
                self.start_frame = 18
                self.maxFrame = 25
                pygame.mixer.Channel(4).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\music\\slave_2_death_sound.mp3")))
                if r < 2:
                    pygame.mixer.Channel(4).set_volume(1.5)
                elif r < 4:
                    pygame.mixer.Channel(4).set_volume(0.9)
                else:
                    pygame.mixer.Channel(4).set_volume(0.5)
            if self.type == 2:
                self.start_frame = 14
                self.maxFrame = 30
                pygame.mixer.Channel(5).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\music\\slave_3_death_sound.mp3")))
                if r < 2:
                    pygame.mixer.Channel(5).set_volume(1)
                elif r < 4:
                    pygame.mixer.Channel(5).set_volume(0.6)
                else:
                    pygame.mixer.Channel(5).set_volume(0.3)
            self.frame = self.start_frame
            self.lifes = -1
            self.maxFrame += 1
            return False
        elif self.frame >= self.maxFrame - self.speed_animation*2 and self.lifes < 0:
            return True


    def walk(self, map, x0, y0, slaves,I,online):

        
        self.frame+=self.speed_animation

        
        if self.state == 1 and self.lifes > 0:
            if self.frame >= self.shootingframe:
                self.frame = 0
                
                
        if self.state == 2 and self.lifes > 0:
            if self.frame >= self.maxFrame:
                self.frame = self.shootingframe
                self.state = 1
                self.targetting_time = 30
                
                
        if self.state == 0 and self.lifes > 0:
            self.frame = 0
                

        a = self.rotation
        self.see = True
        
        x0 = x0/100
        y0 = y0/100
        hit = False
        dy,dx = (y0-self.y)/30,(x0-self.x)/30
        
        for i in range(30):
            if map[int(dy * i + self.y)][int(dx * i + self.x)] != 0:
                self.see = False
        r = math.sqrt((x0-self.x)*(x0-self.x) + (y0-self.y)*(y0-self.y))
            

        if self.see and self.lifes > 0:
            if self.targetting_time <= 0:
                self.state = 2
            if self.state == 1:
                vx = self.v*(x0-self.x)/r+randint(0,100)/100
                vy = self.v*(y0-self.y)/r+randint(0,100)/100
            else:
                vx,vy =0,0
            self.targetting_time -= 1

                


            if int(self.frame) == (self.maxFrame+self.shootingframe)//2:
                c = randint(0,1)
                if c==1:
                    hit = True
                    #pygame.mixer.music.load(os.path.join(sys.path[0] + "\\pony\\music\\", "enemy_shoot.mp3"))
                    if self.type == 1 or self.type == 2:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\music\\enemy3_shoot.mp3")))
                        pygame.mixer.Channel(2).set_volume(1)
                    if self.type == 0:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join(sys.path[0], "pony\\music\\enemy2_shoot.mp3")))
                        pygame.mixer.Channel(2).set_volume(1)
                    
        else:
            vx = math.cos(a)*self.v
            vy = math.sin(a)*self.v

        x = self.x
        y = self.y

        stepx = self.stepx
        stepy = self.stepy
        
        go = False
        if r > 1.5:
            if self.state != 2 and self.see:
                self.state = 1
                self.v = 2
            x_ = x + vx/stepx
            y_ = y + vy/stepy
            for i in range(len(slaves)):
                if i != I and math.sqrt((slaves[i].x-x_)**2 + (slaves[i].y-y_)**2) <= 1:
                    x_ = x
                    y_ = y
                    if self.state != 2:
                        self.state = 0
                    go = True
                    break
        else:
            x_ = x
            y_ = y
            if self.state != 2:
                self.state = 0
        
        self.x,self.y = x_,y_
        while not go:

            if map[int(y_+0.25)][int(x_+0.25)] == 0:
                if map[int(y_-0.25)][int(x_-0.25)] == 0:
                    if map[int(y_-0.25)][int(x_+0.25)] == 0:
                        if map[int(y_+0.25)][int(x_-0.25)] == 0:
                            self.x,self.y = x_,y_
                            go = True
            if not go:
                a = randint(0,10)/10*math.pi*2
                vx = math.cos(a)*self.v
                vy = math.sin(a)*self.v

                x_ = x + vx/stepx
                y_ = y + vy/stepy

        self.rotation = a
        return hit