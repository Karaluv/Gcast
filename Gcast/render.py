import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display


FPS = 60
u = 0.5



class rendering:

    def __init__(self,u,density,render_surface):

        self.render_surface = render_surface

        self.u = u
        self.density = density
        W,H = render_surface.get_size()
        self.W , self.H = W ,H
        self.dw = W*density / (2*u) 

        self.ston = pygame.image.load(os.path.join(sys.path[0],"stone.png"))
        floor =  pygame.image.load(os.path.join(sys.path[0],"floor.jpg"))
        self.floor = pygame.transform.scale(floor,(int(W*8.76/10.1),H//2))

        self.pe = 200
        self.stepx =100
        self.stepy = 100


        
    def ray_cast(self,map,density,dl,a0,a1,minR,maxR,x0,y0):
        
        pe = self.pe

        blockpos = (0,0)

        stepx = self.stepx
        stepy= self.stepy
    
        mapC =[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
        mapP = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

        render_data = []
        render_pol = []

        a = a0

        while a < a1:
            
            mapP = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
            
            x , y = 0,0
            render_data.append([8,1,1])
            l = minR
            
            sin =math.sin(a)*dl
            cos=math.cos(a)*dl

            up = True
            left =True
            right = True
            down = True

            render_pol_buffer = []
            previous = (0,0)

            yp,xp = int(y+y0/stepy),int(x+x0/stepx)
            

            #if abs((int(y0/stepy)-y0/stepy) / sin)<abs((int(x0/stepx)-x0/stepx) / cos):
             #   k = 1
            #else:
             #   k =-1
            

            

            while l <maxR:

                

                renderZ = map[int(y+y0/stepy)][int(x+x0/stepx)]

                if mapP[int(y+y0/stepy)][int(x+x0/stepx)] == 0:
                    mapP[int(y+y0/stepy)][int(x+x0/stepx)] += 1
                    
                    render_pol_buffer.append(l)

                #if yp !=int(y+y0/stepy) or xp != int(x+x0/stepx):
                    #k = -k

                

                if renderZ>0:
                    #k = -k


                    dx = int(x+x0/stepx) - x - x0/stepx
                    dy = int(y+y0/stepy) - y - y0/stepy

                    k = 0

                    if yp >int(y+y0/stepy):
                        k = abs(dx)
                    if yp <int(y+y0/stepy):
                        k = 1-abs(dx)

                    if xp <int(x+x0/stepx):
                        k = abs(dy)
                    if xp >int(x+x0/stepx):
                        k = 1-abs(dy)



                    #if a<=math.pi/2:
                    #    dy = int(y+y0/stepy) - y - y0/stepy

                    #if a>math.pi/2:

                   


                    

                    mapC[int(y+y0/stepy)][int(x+x0/stepx)] = mapC[int(y+y0/stepy)][int(x+x0/stepx)] + 1
                    render_pol.append(render_pol_buffer)
                    render_data[-1]=[l, mapC[int(y+y0/stepy)][int(x+x0/stepx)],k]
                    

                    break

                yp,xp = int(y+y0/stepy),int(x+x0/stepx)

                y = y + sin
                x = x + cos
                l = l+dl

                

            a = a + density
            #print(len(render_data),len(render_pol))
        return render_data,render_pol


    def texturize(self,render_data):

        n = []
        stone = []
        n_=[]

        ston = self.ston
        dw = self.dw
        pe = self.pe

        for i in range(len(render_data)):

            if render_data[i][1] == 1:
                n.append(i)

        n.append(len(render_data))
    
        for j in range(len(n)-1):
            n_.append(n[j+1]-n[j])
        x = 0
        for j in range(len(n_)):

            k1 = render_data[x][2]
            k2 = render_data[x+n_[j]-1][2]


            

            if k2<k1:
              k2,k1 = k1, k2

            #k1 = 0
            #k2 = 1






            width,height = ston.get_width(), ston.get_height()
            ston_ = pygame.Surface((width*(k2-k1) , height ))
            ston_.blit(ston,(0,0),(k1*width,0,width,height))

            width,height = ston_.get_width(), ston_.get_height()
            #ston_ = ston
            for i in range(n_[j]):

                stone.append(pygame.Surface((dw, int(2*pe/render_data[x][0])) ))
            
                stone[-1].blit(pygame.transform.scale(ston_,(round(dw*n_[j]),int(2*pe/render_data[x][0]))),(0,0),(round(dw*i),0,dw,int(2*pe/render_data[x][0])))
                dark = pygame.Surface(stone[-1].get_size()).convert_alpha()
                dark.fill((0, 0, 0, render_data[x][0]*255/7))
                stone[-1].blit(dark,(0,0))
                x = x+1
        return stone

 

    def draw_poll(self,a0,a1,density,render_pol):
        i = 0
    
 
        w = 0
        
        W = self.W
        H = self.H
        pe = self.pe
        dw = self.dw

        cl1 = (255,188,255)
        cl2 =(100,100,255)

        while w<W-1:

            for j in range(len(render_pol[i])):

                cl1_ = render_pol[i][j]/7*cl1[0],render_pol[i][j]/7*cl1[1],render_pol[i][j]/7*cl1[2]
                cl2_ = render_pol[i][j]/7*cl2[0],render_pol[i][j]/7*cl2[1],render_pol[i][j]/7*cl2[2]

                cl1__ = cl1[0] - cl1_[0],cl1[1] - cl1_[1],cl1[2] - cl1_[2]
                cl2__ = cl2[0] - cl2_[0],cl2[1] - cl2_[1],cl2[2] - cl2_[2]

                pygame.draw.line(self.render_surface,cl1__,(w-i,H//2+ pe/render_pol[i][j]),(w+dw-i,H//2+ pe/render_pol[i][j]),2)
                pygame.draw.line(self.render_surface,cl2__,(w-i,H//2- pe/render_pol[i][j]),(w+dw-i,H//2 -  pe/render_pol[i][j]),2)
            w = w+dw
            i=i+1


    def draw_wall(self,a0,a1,density,render_data):

        W= self.W
        H = self.H
        pe = self.pe
        dw = self.dw
        i = 0
    
 
        w = 0
        

        stone = self.texturize(render_data)


        while w < W-1:
            self.render_surface.blit(stone[i],(w-i,int(H//2-pe/render_data[i][0])))
            #pygame.draw.rect(self.render_surface,(128,255,128),(w,H//2-pe/render_data[i][0],dw,2*pe/render_data[i][0]),0)
            w = w+dw
        
            i = i+1

    def draw_background(self):
        W,H = self.W,self.H
        self.gradientRect(self.render_surface,(0,0,0),(128,50,128),pygame.Rect(0,H//2,W,H//2))
        self.gradientRect(self.render_surface,(128,50,50),(0,0,0),pygame.Rect(0,0,W,H//2))


    def render(self,map,density,dl,a0,a1,minR,maxR,x0,y0):

        render_wall_data , render_poll_data = self.ray_cast(map,density,dl,a0,a1,minR,maxR,x0,y0)

        self.draw_background()
        self.draw_wall(a0,a1,density,render_wall_data)
        self.draw_poll(a0,a1,density,render_poll_data)








    def gradientRect( self,window, left_colour, right_colour, target_rect ):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
        colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
        pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
        pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
        window.blit( colour_rect, target_rect )                                    # paint it




    

