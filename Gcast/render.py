import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
import copy
import threading

from functools import lru_cache


class rendering:



    def __init__(self,u,density,dl,render_surface,height,width):

        self.render_surface = render_surface
        self.dl = dl
        self.u = u
        self.density = density
        W,H = render_surface.get_size()
        self.W , self.H = W ,H
        self.dw = W*density

        self.ston =[]

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\cia")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\flag")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\enter")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\exit")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())

        self.sprites =[]

        self.sprites.append([])
        path = os.path.join(sys.path[0],"pony\\sprites\\slave1")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.sprites[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
        self.sprites.append([])
        path = os.path.join(sys.path[0],"pony\\sprites\\slave2")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.sprites[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())

        self.sprites.append([])
        path = os.path.join(sys.path[0],"pony\\sprites\\slave3")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.sprites[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())



        self.pe = 200
        self.stepx =100
        self.stepy = 100

        self.pi_2 = math.pi*2

        maxR = 7
        
        self.sky = pygame.Surface((W,H//2-maxR/self.pe))
        self.ground = pygame.Surface((W,H//2-maxR/self.pe))

        self.gradientRect(self.sky,(153, 153, 102),(0,0,0),pygame.Rect(0,0,W,H//2-maxR/self.pe))
        self.gradientRect(self.ground,(0,0,0),(135,62,35),pygame.Rect(0,0,W,H//2-maxR/self.pe))

        self.width = width
        self.height = height

    @lru_cache()
    def find_clothest_point(self,map,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        

        while map[int(yc)][int(xc)]!=0:
            l = l -lc
            xc = xc - cos
            yc = yc - sin

        if lc <= lmin:
            return xc+cos,yc+sin,l+lc
        if lc>lmin:
            return self.find_clothest_point(map,l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)

    @lru_cache()
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

    
    def enemy_ray_caster(self,wall_data,enemies,a0,a1,minR,maxR,x0,y0):

        enemy_render_data = []


        density,pe,stepx ,stepy=self.density,self.pe,self.stepx,self.stepy


        density = self.density
        pe = self.pe
        stepx =self.stepx
        stepy = self.stepy

        for i in range(len(enemies)):
            x,y = enemies[i][0], enemies[i][1]
            if abs(x - x0/stepx)<maxR:
                if abs(y - y0/stepy)<maxR:
                    l_2 = (x-x0/stepx)**2+(y-y0/stepy)**2
                    l = math.sqrt(l_2)

                    sin = (y-y0/stepy)/l
                    cos = (x -x0/stepx)/l

                    ch = (cos*sin0 - sin*cos0)
                    zn = sin*(cos1-cos0)-cos*(sin1 - sin0)

                    k = ch / zn
                    w = k / density
                    if ch<0 and zn<0:
                        if wall_data[min(int(w),len(wall_data)-1)][0]>l:
                            enemy_render_data.append([l+0.3,w,enemies[i][2],enemies[i][3]])

        return enemy_render_data


    @lru_cache()
    def ray_cast(self,map,a0,a1,minR,maxR,x0,y0):

        # тут создаешь как хочешь tuple размером (int(1/density)+1) строк и в каждой строке 6 элементов: все из них по умолчанию 0 
        #в этой функции ты лишь записываешь и меняешь первые 5 из них l, t*w-d,mapCV[rY][rX],k,map[rY][rX]
        
        dl = self.dl
        pe = self.pe
        stepx = self.stepx
        stepy= self.stepy
        width = self.width
        height = self.height
        density = self.density
        w = self.W

        history =[]
        

        mapCH = [[0 for _ in range(width)] for _ in range(height)]
        mapCV = [[0 for _ in range(width)] for _ in range(height)]


        render_data = []

        VM = False

        cos = math.cos(a0)
        sin  = math.sin(a0)
        dcos = (math.cos(a1) - cos)*density*dl
        dsin = (math.sin(a1) - sin)*density*dl
        sin = sin*dl
        cos = cos*dl

        t = 0
        k = 1
        d = 0

        ugol = 1

        sc = 4
        x,y =0,0

        rX,rY = int(x+x0/stepx),int(y+y0/stepy)
        minR_ = minR

        while t < 1:

            if ugol != 0:
                pass
            else:
                sc = 1


            l = minR

            x , y = 0,0
            
            
            xp,yp = rX,rY

            render_data.append([maxR,t*w-d,1,1,1])
            history.append([0,0,True])

            
            
            while l <maxR:
                rX,rY = int(x+x0/stepx),int(y+y0/stepy)

                #этот if можешь закоментить если сложно
                if ugol == 0:
                    if l>render_data[-2][0]+0.9:


                        n = int(0.9/dl)+1
                        if l - n*dl*1.1>minR:
                            
                            ugol = 1

                            sc =4

                            sin -= (ugol+1)*dsin
                            cos -=(ugol+1)*dcos

                            d -=(ugol+1)
                            t -= (ugol+1)*density

                            del render_data[-(ugol+1):]
                            del history[-(ugol+1):]

                            if len(history)>3:
                                rX,rY,VM = history[-(3)][0],history[-(3)][1],history[-(3)][2]

                            elif len(history)>2:
                                rX,rY,VM = history[-(2)][0],history[-(2)][1],history[-(2)][2]
                            else:
                                rX,rY,VM = history[-(1)][0],history[-(1)][1],history[-(1)][2]

                            ugol +=1
                            break
                    
                if map[rY][rX]>0:


                    xc,yc = x+x0/stepx,y+y0/stepy
                    xc,yc,l = self.find_clothest_point(map,l,xp,yp,xc,yc,cos/10/sc,sin/10/sc,dl/10/sc,dl/100/sc)
                    rY,rX = int(yc),int(xc)
                    dx = abs(rX - xc)
                    dy = abs(rY - yc)

                    if yp != rY and xp != rX:
                        k = max(dy,dx)
                        xp,yp,l = self.find_clothest_gran(l,xp,yp,xc,yc,cos/10/sc,sin/10/sc,dl/10/sc,dl/100/sc)
                        yp = int(yp)
                        xp = int(xp)

                    if yp >rY:
                        k = dx
                        VM = False

                    elif yp <rY:
                        k = 1-dx
                        VM = False

                    elif xp <rX:
                        k = dy
                        VM = True

                    elif xp >rX:
                        k = 1-dy
                        VM = True

                    if not VM:
                        mapCH[rY][rX] += 1
                    else:
                        mapCV[rY][rX] += 1



                    if not VM:
                        render_data[-1]=[l, t*w-d,mapCH[rY][rX],k,map[rY][rX]]
                    else:
                        render_data[-1]=[l, t*w-d,mapCV[rY][rX],k,map[rY][rX]]
                    


                    history[-1]=[rX,rY,VM]

                    #этот if можешь закоментить если сложно
                    if ugol == 0:
                        if len(render_data)>3:
                            if l<render_data[-2][0]-0.9 or history[-2][2] != VM:

  
                                n = int(0.9/dl)+1
                                if l - n*dl*1.1>minR:

                                    ugol = min(int(dl/density),len(render_data)-2)
                                
                                    for i in range(len(render_data)-ugol,len(render_data)):

                                        if history[i][2]:
                                            mapCV[history[i][1]][history[i][0]] -= 1
                                        if not history[i][2]:
                                            mapCH[history[i][1]][history[i][0]] -= 1
                                
                                    sc = 4
  
                                    sin -= (ugol+1)*dsin
                                    cos -=(ugol+1)*dcos

                                    d -= (ugol+1)
                                    t -= (ugol+1)*density
                                
                                    del render_data[-(ugol+1):]
                                    del history[-(ugol+1):]

                                    if len(history)>3:
                                        rX,rY,VM = history[-(3)][0],history[-(3)][1],history[-(3)][2]

                                    elif len(history)>2:
                                        rX,rY,VM = history[-(2)][0],history[-(2)][1],history[-(2)][2]
                                    else:
                                        rX,rY,VM = history[-(1)][0],history[-(1)][1],history[-(1)][2]

                                    ugol +=2

                                    break

                                if ugol >0:
                                   ugol-=1



                    break

                yp,xp = rY,rX
                y += sin/sc
                x += cos/sc
                l += dl/sc

                if l>=maxR:
                    if ugol >0:
                       ugol-=1

            

            cos += dcos
            sin += dsin

            t += density
            
            d+= 1

        render_data = tuple(tuple(i) for i in render_data)

        return render_data





    def draw_wall(self,a0,a1,render_data,enemies):
        sprites= self.sprites

        W= self.W
        H = self.H
        pe = self.pe
        dw = self.dw

        density = self.density

        i = 0
        w = 0
        j = 0
        
        i_max = int(1 / density)
        while i <= i_max:
            if j<len(enemies):
                if render_data[i][0]<enemies[j][0]:
                    render_image = pygame.transform.scale(sprites[enemies[j][2]][int(enemies[j][3])],(int(pe/enemies[j][0]),int(pe/enemies[j][0]*1.4)))

                    render_mask = pygame.mask.from_surface(render_image)
                    render_mask = render_mask.to_surface()
                    dark = pygame.Surface(render_image.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, enemies[j][0]*255/30))
                    render_image.blit(dark,(0,0))

                    render_image.blit(render_image, (0, 0), None, pygame.BLEND_RGBA_MULT)
                    render_mask.set_colorkey((255,255,255))
                    render_image.blit(render_mask, (0, 0))
                    render_image.set_colorkey((0,0,0))

                    self.render_surface.blit(render_image,(int(enemies[j][1]*(dw-1)-pe/enemies[j][0]/2),int(H//2-pe/enemies[j][0]*0.4)))
                    j += 1

            self.render_surface.blit(render_data[i][5],(render_data[i][1],int(H//2-pe/render_data[i][0])))
            w = w+dw
            i = i+1

        return w-i-dw

    def draw_background(self):
        maxR = 7
        W,H = self.W,self.H
        self.render_surface.blit(self.sky,(0,0))
        self.render_surface.blit(self.ground,(0,H//2+maxR/self.pe))

    def render(self,map,enemies,a0,a1,minR,maxR,x0,y0):

        

        render_wall_data = [list(item) for item in self.ray_cast(map,a0,a1,minR,maxR,x0,y0)]

        # на это похуй
        self.draw_background()

        enemy_render_data = self.enemy_ray_caster(render_wall_data,enemies,a0,a1,minR,maxR,x0,y0)

        # в этой функции меняется 6й элемент массива - surface
        render_wall_data = self.texturize(render_wall_data)
        
        # блок сортировки переделать под tuple с сортировкой строк по первому элементу в порядке убывания
        render_wall_data.sort(key=lambda item: item[0], reverse = True)
        enemy_render_data.sort(key=lambda item: item[0], reverse = True)


        res = self.draw_wall(a0,a1,render_wall_data, enemy_render_data)

        self.xs = res
     
    def gradientRect( self,window, left_colour, right_colour, target_rect ):
        colour_rect = pygame.Surface( ( 2, 2 ) )                          
        pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            
        pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            
        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) ) 
        window.blit( colour_rect, target_rect )      
    
    def texturize(self,render_data):
        n = []
        texture_data = []
        n_=[]

        ston = self.ston
        dw = self.dw
        pe = self.pe

        w,H = self.W,self.H

        x = 0

        for i in range(len(render_data)):
            if render_data[i][2] == 1:
                n.append(i)

        n.append(len(render_data))
    
        for j in range(len(n)-1):
            n_.append(n[j+1]-n[j])

        for j in range(len(n_)):
            k1 = 1
            k2 = 0

            for i in range(x,x+n_[j]):
                k1 = min(k1,render_data[i][3])
                k2 = max(k2,render_data[i][3])
            
            if k2<k1:
              k2,k1 = k1, k2

            width,height = ston[render_data[i][4]-1][0].get_width(), ston[render_data[i][4]-1][0].get_height()
            texture_buffer = pygame.Surface((width*(k2-k1) , height ))
            texture_buffer.blit(ston[render_data[i][4]-1][0],(0,0),(k1*width,0,width,height))

            width,height = texture_buffer.get_width(), texture_buffer.get_height()

            for i in range(n_[j]):
                h = int(2*pe/render_data[x][0])
                if h>H:
                    texture_data = pygame.Surface((dw, H))
                    texture_buffer_ = texture_buffer.subsurface((0, ((h-H)//2/h)*texture_buffer.get_height(), texture_buffer.get_width(), H/h*texture_buffer.get_height()))
                    texture_data.blit(pygame.transform.scale(texture_buffer_,(round(dw*n_[j]),H)),(0,0),(round(dw*i),0,dw,H))
                    dark = pygame.Surface(texture_data.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, render_data[x][0]*255/7))
                    texture_data.blit(dark,(0,0))
                    render_data[x][0] = 2*pe/H
                    render_data[x]= render_data[x]+[texture_data]
                else:
                    texture_data = pygame.Surface((dw, int(2*pe/render_data[x][0])))
                    texture_data.blit(pygame.transform.scale(texture_buffer,(round(dw*n_[j]),h)),(0,0),(round(dw*i),0,dw,h))
                
                    dark = pygame.Surface(texture_data.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, render_data[x][0]*255/7))
                    texture_data.blit(dark,(0,0))
                    render_data[x]= render_data[x]+[texture_data]

                x = x+1

        return render_data
