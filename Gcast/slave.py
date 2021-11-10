import math
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
        if type == 0:
            self.maxFrame  = 37
            self.speed_animation = 0.2
        if type == 1:
            self.maxFrame  = 10
            self.speed_animation = 0.2

        if type == 2:
            self.maxFrame  = 9
            self.speed_animation = 0.2

        self.frame = randint(0,self.maxFrame) 

    def walk(self,map):

        self.frame+=self.speed_animation
        if self.frame > self.maxFrame-1:
            self.frame = 0

        a = self.rotation

        vx = math.cos(a)*self.v
        vy = math.sin(a)*self.v

        x = self.x
        y =self.y

        stepx = self.stepx
        stepy = self.stepy

        x_ = x + vx/stepx
        y_ = y + vy/stepy
        go = False

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