import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
import copy



class rendering:



    def __init__(self,u,density,render_surface,height,width):

        self.render_surface = render_surface

        self.u = u
        self.density = density
        W,H = render_surface.get_size()
        self.W , self.H = W ,H
        self.dw = W*density

        self.ston = pygame.image.load(os.path.join(sys.path[0],"locker_room.jpg"))
        floor =  pygame.image.load(os.path.join(sys.path[0],"floor.jpg"))
        self.floor = pygame.transform.scale(floor,(int(W*8.76/10.1),H//2))

        self.pe = 200
        self.stepx =100
        self.stepy = 100




        
        self.sky = pygame.Surface((W,H//2))
        self.ground = pygame.Surface((W,H//2))

        self.gradientRect(self.sky,(220,222,219,255),(0,0,0),pygame.Rect(0,0,W,H//2))
        self.gradientRect(self.ground,(0,0,0),(136,138,137,255),pygame.Rect(0,0,W,H//2))

        #self.empty_map = copy.deepcopy(self.build_matrix(height,width))
        #self.empty_map = [[0]*width]*height
        self.width = width
        self.height = height

    def find_clothest_point(self,map,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        

        while map[int(yc)][int(xc)]!=0:
            l = l -lc
            xc = xc - cos
            yc = yc - sin

        if lc <= lmin:
            return xc+cos,yc+sin,l+lc
        if lc>lmin:
            return self.find_clothest_point(map,l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)

    def find_clothest_gran(self,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        

        while (not int(xc)==xp) or (not int(yc)==yp):
            l = l -lc
            xc = xc - cos
            yc = yc - sin

        if lc <= lmin:
            return xc+10*cos,yc+10*sin,l+10*lc

        if (not(int(xc) == xp) and int(yc)==yp) or (int(xc)==xp and not( int(yc)==yp)):
            return xc,yc,l+lc

        if lc>lmin:
            return self.find_clothest_gran(l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)
        
    def ray_cast(self,map,density,dl,a0,a1,minR,maxR,x0,y0):
        
        pe = self.pe

        stepx = self.stepx
        stepy= self.stepy

        width = self.width
        height = self.height

        mapCH = [[0 for _ in range(width)] for _ in range(height)]
        mapCV = [[0 for _ in range(width)] for _ in range(height)]

        render_data = []

        VM = False

        cos = math.cos(a0)
        sin  = math.sin(a0)

        dcos = (math.cos(a1) - cos)*density*dl
        dsin = (math.sin(a1) - sin)*density*dl

        t = 0
        sin = sin*dl
        cos = cos*dl

        k = 1

        while t < 1:
           
            
            x , y = 0,0
            render_data.append([maxR,1,1])
            l = minR

            xp,yp = int(x+x0/stepx),int(y+y0/stepy)

            while l <maxR:

                rX,rY = int(x+x0/stepx),int(y+y0/stepy)

                if map[rY][rX]>0:

                    xc,yc = x+x0/stepx,y+y0/stepy

                    xc,yc,l = self.find_clothest_point(map,l,xp,yp,xc,yc,cos/10,sin/10,dl/10,0.00001)

                    rY,rX = int(yc),int(xc)

                    dx = abs(rX - xc)
                    dy = abs(rY - yc)


                    if yp != rY and xp != rX:

                        k = max(dy,dx)

                        xp,yp,l_ = self.find_clothest_gran(l,xp,yp,xc,yc,cos/10,sin/10,dl/10,0.00001)

                        yp = int(yp)
                        xp = int(xp)

                    
                    if yp >rY:
                        k = dx
                        VM = False

                    if yp <rY:
                        k = 1-dx
                        VM = False

                    if xp <rX:
                        k = dy
                        VM = True

                    if xp >rX:
                        k = 1-dy
                        VM = True

                    if not VM:
                        mapCH[rY][rX] += 1
                    if VM:
                        mapCV[rY][rX] += 1


                    if not VM:
                        render_data[-1]=[l, mapCH[rY][rX],k]
                    if VM:
                        render_data[-1]=[l, mapCV[rY][rX],k]

                    break

                yp,xp = rY,rX
                y += sin
                x += cos
                l += dl

            cos += dcos
            sin += dsin

            t += density


        return render_data


    def texturize(self,render_data):

        n = []
        texture_data = []
        n_=[]

        ston = self.ston
        dw = self.dw
        pe = self.pe

        x = 0

        for i in range(len(render_data)):

            if render_data[i][1] == 1:
                n.append(i)


        n.append(len(render_data))
    
        for j in range(len(n)-1):
            n_.append(n[j+1]-n[j])

        for j in range(len(n_)):

            k1 = 1
            k2 = 0

            for i in range(x,x+n_[j]):
                

                k1 = min(k1,render_data[i][2])
                k2 = max(k2,render_data[i][2])
            

            if k2<k1:
              k2,k1 = k1, k2




            width,height = ston.get_width(), ston.get_height()
            texture_buffer = pygame.Surface((width*(k2-k1) , height ))
            texture_buffer.blit(ston,(0,0),(k1*width,0,width,height))

            width,height = texture_buffer.get_width(), texture_buffer.get_height()

            for i in range(n_[j]):

                texture_data.append(pygame.Surface((dw, int(2*pe/render_data[x][0])) ))
            
                texture_data[-1].blit(pygame.transform.scale(texture_buffer,(round(dw*n_[j]),int(2*pe/render_data[x][0]))),(0,0),(round(dw*i),0,dw,int(2*pe/render_data[x][0])))
                
                dark = pygame.Surface(texture_data[-1].get_size()).convert_alpha()
                dark.fill((0, 0, 0, render_data[x][0]*255/7))
                texture_data[-1].blit(dark,(0,0))

                x = x+1
        return texture_data



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
            w = w+dw
            i = i+1
        return w-i-dw

    def draw_background(self):
        W,H = self.W,self.H

        self.render_surface.blit(self.sky,(0,0))
        self.render_surface.blit(self.ground,(0,H//2))

    def render(self,map,density,dl,a0,a1,minR,maxR,x0,y0):

        render_wall_data  = self.ray_cast(map,density,dl,a0,a1,minR,maxR,x0,y0)

        self.draw_background()
        return self.draw_wall(a0,a1,density,render_wall_data)

        






    def gradientRect( self,window, left_colour, right_colour, target_rect ):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
        colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
        pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
        pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
        window.blit( colour_rect, target_rect )                                    # paint it




    

