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
        self.shooting = False
        self.r0 = 2
        self.targetting_time = 30
        self.lifes = 2
        self.see = True
        if type == 0:
            self.maxFrame  = 16
            self.speed_animation = 0.2
            self.shootingframe = 10
        if type == 1:
            self.maxFrame  = 17
            self.speed_animation = 0.2
            self.shootingframe = 13
        if type == 2:
            self.maxFrame  = 13
            self.speed_animation = 0.2
            self.shootingframe = 9

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
            

    def walk(self, map, x0, y0):

        self.frame+=self.speed_animation
        if self.frame >= self.maxFrame - self.speed_animation:
            self.frame = self.start_frame

        a = self.rotation
        self.see = True
        
        x0 = x0/100
        y0 = y0/100
        hit = False
        dy,dx = (y0-self.y)/30,(x0-self.x)/30
        
        for i in range(30):
            
            if(map[int(dy*i+self.y)][int(dx*i+self.x)] != 0):
                self.see = False
        r = math.sqrt((x0-self.x)*(x0-self.x) + (y0-self.y)*(y0-self.y))
            

        if self.see and self.lifes != -1:
            if self.frame < self.shootingframe-1:
                vx = self.v*(x0-self.x)/r+randint(0,100)/100
                vy = self.v*(y0-self.y)/r+randint(0,100)/100
            else:
                vx,vy =0,0
                

 
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
        if r > 0.5:
            x_ = x + vx/stepx
            y_ = y + vy/stepy
        else:
            x_ = x
            y_ = y
        go = False
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