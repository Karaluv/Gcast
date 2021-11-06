from random import randint
import math

class billy:
    
    def __init__(self, x,y,a,name):
        self.x = x
        self.y = y
        self.a = a
        self.name = name


        self.maxR = 7
        self.dl = 0.01

        self.stepx = 100
        self.stepy = 100

        self.pi_2 = math.pi*2

    def Rotate(self,a):
        self.a = self.a +a
        global move
        move = True

    def Move(self,l,n,map):
        a = self.a
        x_ = self.x-l*math.sin(math.pi - a)+n*math.cos(a)
        y_ = self.y-l*math.cos(math.pi - a)+n*math.sin(a)
        
        if map[int(y_/100+0.05)][int(x_/100+0.05)] == 0:
            if map[int(y_/100-0.05)][int(x_/100-0.05)] == 0:
                if map[int(y_/100-0.05)][int(x_/100+0.05)] == 0:
                    if map[int(y_/100+0.05)][int(x_/100-0.05)] == 0:
                        self.y = y_
                        self.x = x_

    def check_fisting(self,slaves):
        x,y = self.x/self.stepx,self.y/self.stepy
        for i in range(len(slaves)):
            if abs(slaves[i][0]-x)<0.3 and abs(slaves[i][1]-y)<0.3:
                print(slaves[i][2])


    def update(self):
        self.a = self.a % self.pi_2

    def shoot(self,slaves,map):
        a = self.a

        maxR = self.maxR
        find = False
        dl = self.dl

        x = self.x/self.stepx
        y = self.y/self.stepy

        dcos = math.cos(a)*dl
        dsin = math.sin(a)*dl

        l = 0
    

        while not find and l<maxR:
            l = dl+l
            x = x+dcos
            y = y+dsin


            if map[int(y)][int(x)] == 1:
                find = True
                break
            else:
                for j in range(len(slaves)):
                    z_2 = (slaves[j].x-x)**2+(slaves[j].y-y)**2
                
                    if z_2<0.01:
                        print("kill")
                        find = True
                        del slaves[j]
                        break
        return slaves
