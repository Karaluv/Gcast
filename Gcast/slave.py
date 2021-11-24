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
        self.shooting = False
        self.r0 = 2
        self.targetting_time = 30
        see = True
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


        self.frame = randint(0,self.maxFrame) 

    def walk(self, map, x0, y0):

        self.frame+=self.speed_animation
        if self.frame >= self.maxFrame-1:
            self.frame =0

        a = self.rotation
        see = True
        
        x0 = x0/100
        y0 = y0/100
        hit = False
        dy,dx = (y0-self.y)/30,(x0-self.x)/30
        
        for i in range(30):
            
            if(map[int(dy*i+self.y)][int(dx*i+self.x)] != 0):
                see = False
        r = math.sqrt((x0-self.x)*(x0-self.x) + (y0-self.y)*(y0-self.y))
            

        if see:
            if self.frame < self.shootingframe-1:
                vx = self.v*(x0-self.x)/r+randint(0,100)/100
                vy = self.v*(y0-self.y)/r+randint(0,100)/100
            else:
                vx,vy =0,0
                

 
            if int(self.frame) == (self.maxFrame+self.shootingframe)//2:
                c = randint(0,1)
                if c==1:
                    hit = True
                    
        else:
            vx = math.cos(a)*self.v
            vy = math.sin(a)*self.v

        x = self.x
        y = self.y

        stepx = self.stepx
        stepy = self.stepy

        x_ = x + vx/stepx
        y_ = y + vy/stepy
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

    def hitted(self,z,l,a,z0,y0):
        #get position of bullet, if it got on weak point,like head
        pass
        
