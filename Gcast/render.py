import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display
import copy
import threading

#from numba import jit, cuda
from functools import lru_cache

class StopThread(StopIteration): pass

threading.SystemExit = SystemExit, StopThread
 
class rendering(threading.Thread):

    def __init__(self,u,density,dl,render_surface,height,width,update,redraw,elevation):

        #block which defines variables for class
        self.render_surface = render_surface
        self.dl = dl
        self.density = density
        W,H = render_surface.get_size()
        self.W , self.H = W ,H
        self.dW = (W*density-1)
        self.elevation = elevation
        self.width = width
        self.height = height

        #def that loads wall pictures
        def load_wall(arr,name):
            '''
            arr - array in which pictures are loaded
            name - files folder
            '''
            arr.append([])
            path = os.path.join(sys.path[0],name)
            files = next(os.walk(path))
            onlyfiles = next(os.walk(path)) 
            for i in range(len(onlyfiles[2])):
                arr[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
                arr[-1][-1] = pygame.transform.scale(arr[-1][-1],(200,200))
            return arr

        #def that loads enemy animations
        def load_slaves(arr,name):
            '''
            arr - array in which pictures are loaded
            name - files folder
            '''
            arr.append([])
            path = os.path.join(sys.path[0],name)
            files = next(os.walk(path))
            onlyfiles = next(os.walk(path)) 
            for i in range(len(onlyfiles[2])):
                print(files[0]+"\\"+onlyfiles[2][i])
                arr[-1].append(pygame.image.load(files[0]+"\\"+"  ("+str(i+1)+").png").convert_alpha())
            return arr
        
        #block which loads all data
        self.ston =[]
        self.sprites =[]

        self.ston = load_wall(self.ston,"pony\\wall\\cia")
        self.ston = load_wall(self.ston,"pony\\wall\\flag")
        self.ston = load_wall(self.ston,"pony\\wall\\flagblood")
        self.ston = load_wall(self.ston,"pony\\wall\\enter")
        self.ston = load_wall(self.ston,"pony\\wall\\exit")

        self.sprites = load_slaves(self.sprites,"pony\\sprites\\slave1")
        self.sprites = load_slaves(self.sprites,"pony\\sprites\\slave2")
        self.sprites = load_slaves(self.sprites,"pony\\sprites\\slave3")
        
        self.sprites = tuple(tuple(i) for i in self.sprites)
        self.ston = tuple(tuple(i) for i in self.ston)


        #target fps
        self.fps = 60
        #some variables for normal work
        self.pe = 100
        self.stepx =100
        self.stepy = 100
        maxR = 7
        self.xs = (int(1/density)+1)*self.dW
        
        #multi threading block
        self.update = update
        self.redraw = redraw

        self.blit = False

        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
        
        threading.Thread.__init__(self)


    #everlasting loop def, that just rerenders everything
    def run(self):
        import time
        clock = pygame.time.Clock()
        time.sleep(0.5)
        FPS = self.fps
        FPS +=1
        while self.__running.isSet():
            self.__flag.wait()
            clock.tick(FPS)

            self.render(self.update())
            self.redraw()


    #defs that are needed to control the thread: pause render,resume render,stop render process 
    def pause(self):
        self.__flag.clear() # Set to False to block the thread
    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking
    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False

    #def which find clothest point to the wall, encreases the graphics
    @lru_cache()
    def find_clothest_point(self,map,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        '''
        map - world map
        l - length of ray
        xp,yp - previous ray position
        xc,yc - current ray position
        cos,sin - cos and sin divided by density of current position
        lc - current ray step
        lmin - minimum step of the ray
        '''
        while map[int(yc)][int(xc)]!=0:
            l -= lc
            xc -= cos
            yc -= sin

        if lc <= lmin:
            return xc+cos,yc+sin,l+lc
        if lc>lmin:
            return self.find_clothest_point(map,l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)

    #def which find clothest point to the wall, encreases the graphics and fixes same bugs
    @lru_cache()
    def find_clothest_gran(self,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        '''
        map - world map
        l - length of ray
        xp,yp - previous ray position
        xc,yc - current ray position
        cos,sin - cos and sin divided by density of current position
        lc - current ray step
        lmin - minimum step of the ray
        '''
        while (not int(xc)==xp) or (not int(yc)==yp):
            l -= lc
            xc -= cos
            yc -= sin

        if lc <= lmin:
            return xc+10*cos,yc+10*sin,l+10*lc
        if (not(int(xc) == xp) and int(yc)==yp) or (int(xc)==xp and not( int(yc)==yp)):
            return xc,yc,l+lc
        if lc>lmin:
            return self.find_clothest_gran(l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)

    #def which converts enemy position to render data
    def enemy_ray_caster(self,wall_data,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0):
        '''
        wall_data - current walls position
        enemies - enemies types and there position
        cos0,sin0 - right border of view zone
        '''
        enemy_render_data = []
        density,pe,stepx ,stepy=self.density,self.pe,self.stepx,self.stepy

        for i in range(0,len(enemies),4):
            x,y = enemies[i+0], enemies[i+1]
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
                            enemy_render_data.append([l+minR,w,enemies[i+2],enemies[i+3]])

        return enemy_render_data

    #one of the main def, sends rays and gets every single column of pixels position
    def ray_cast(self,map,cos,sin,cos1,sin1,minR,maxR,x0,y0):
        '''
        map - world map
        cos,sin - strting position of the ray
        cos1,sin1 - final position of the ray
        minR - minimum field of view
        maxR - maximum render distance
        x0,y0 - player position
        '''

        dl,pe,stepx,stepy,width,height,density,w,dW = self.dl,self.pe,self.stepx,self.stepy,self.width, self.height,self.density,self.W,self.dW

        history =[]
        render_data = []

        mapCH = [[0 for _ in range(width)] for _ in range(height)]
        mapCV = [[0 for _ in range(width)] for _ in range(height)]

        dcos = (cos1 - cos)*density*dl
        dsin = (sin1 - sin)*density*dl
        sin = sin*dl
        cos = cos*dl
        
        VM = False

        k = 1
        d = 0
        ugol = 1
        sc = 4
        x,y =0,0

        rX,rY = int(x+x0/stepx),int(y+y0/stepy)
        d_max= int(1/density)+1

        while d < d_max:

            if ugol == 0:
                sc = 1

            x , y, l= 0,0,minR
            
            xp,yp = rX,rY

            render_data.append([maxR,d*dW,1,0,1])
            history.append([0,0,True])

            while l <maxR:
                rX,rY = int(x+x0/stepx),int(y+y0/stepy)

                if ugol == 0:
                    if l>render_data[-2][0]+1:
                        if l - 1>minR:
                            
                            ugol,sc = 1,4

                            sin -= (ugol+1)*dsin
                            cos -=(ugol+1)*dcos

                            d -=(ugol+1)
                            t -= (ugol+1)*density

                            for i in range(len(render_data)-ugol-1,len(render_data)):

                                if history[i][2]:
                                    mapCV[history[i][1]][history[i][0]] -= 1
                                else:
                                    mapCH[history[i][1]][history[i][0]] -= 1

                            del render_data[-(ugol+1):]
                            del history[-(ugol+1):]


                            rX,rY,VM = history[-(1)][0],history[-(1)][1],history[-(1)][2]

                            ugol +=1
                            break
                    
                if map[rY][rX]>0:

                    xc,yc = x+x0/stepx,y+y0/stepy
                    xc,yc,l = self.find_clothest_point(map,l,xp,yp,xc,yc,cos/10/sc,sin/10/sc,dl/10/sc,dl/1000/sc)
                    rY,rX = int(yc),int(xc)
                    dx,dy = abs(rX - xc),abs(rY - yc) 

                    if yp != rY and xp != rX:
                        k = max(dy,dx)
                        xp,yp,l = self.find_clothest_gran(l,xp,yp,xc,yc,cos/10/sc,sin/10/sc,dl/10/sc,dl/1000/sc)
                        yp,xp = int(yp),int(xp)

                    if map[rY][rX]==0 or map[yp][xp]>0:
                        break

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
                    else:
                        k = 0

                    if not VM:
                        mapCH[rY][rX] += 1
                        render_data[-1]=[l, d*dW,mapCH[rY][rX],k,map[rY][rX]]
                    else:
                        mapCV[rY][rX] += 1
                        render_data[-1]=[l, d*dW,mapCV[rY][rX],k,map[rY][rX]]

                    history[-1]=[rX,rY,VM]
                    
                    if ugol == 0:
                        if len(render_data)>3:
                            if l<render_data[-2][0]-1:                              
                                if l - 1>minR:
                                    ugol = min(int(dl/density),len(render_data)-2)+1
                                
                                    for i in range(len(render_data)-ugol,len(render_data)):
                                        if history[i][2]:
                                            mapCV[history[i][1]][history[i][0]] -= 1
                                        else:
                                            mapCH[history[i][1]][history[i][0]] -= 1
                                
                                    sc = 4
                                    sin -= ugol*dsin
                                    cos -=ugol*dcos
                                    d -= ugol
                                    t -= ugol*density
                                
                                    del render_data[-ugol:]
                                    del history[-ugol:]

                                    rX,rY,VM = history[-(1)][0],history[-(1)][1],history[-(1)][2]
                                    
                                    break

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
        
            d+= 1

        return render_data

    #draws walls, enemy on surface
    def draw_wall(self,render_data,enemies,elevation):
        '''
        render_data - wall textures and thir position
        enemies - position of enemies
        elevation - y position of the whole render
        '''

        sprites= self.sprites

        W,H,pe,dW,density = self.W,self.H,self.pe,self.dW,self.density
        j = 0
        i_max = int(1 / density)+1

        for i in range(i_max):
            if j<len(enemies):
                if render_data[i][0]<enemies[j][0]:

                    render_image = pygame.transform.scale(sprites[enemies[j][2]][int(enemies[j][3])],(int(pe/enemies[j][0]),int(pe/enemies[j][0]*1.4)))

                    render_mask = pygame.mask.from_surface(render_image)
                    render_mask = render_mask.to_surface()
                    dark = pygame.Surface(render_image.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, min(255,enemies[j][0]*255/10)))
                    render_image.blit(dark,(0,0))
                    render_image.blit(render_image, (0, 0), None, pygame.BLEND_RGBA_MULT)
                    inv = pygame.Surface(render_mask.get_rect().size, pygame.SRCALPHA)
                    inv.fill((255,255,255,255))
                    inv.blit(render_mask, (0,0), None, pygame.BLEND_RGB_SUB)
                    render_mask.set_colorkey((255,255,255))
                    render_image.blit(render_mask, (0, 0))
                    render_image.set_colorkey((0,0,0))
                    inv.set_colorkey((255,255,255))

                    self.render_surface.blit(inv,(int(enemies[j][1]*dW-pe/enemies[j][0]/2*1.5),int(H//2*elevation-pe/enemies[j][0]*0.4)))
                    self.render_surface.blit(render_image,(int(enemies[j][1]*dW-pe/enemies[j][0]/2*1.5),int(H//2*elevation-pe/enemies[j][0]*0.4)))
                    j += 1

            self.render_surface.blit(render_data[i][5],(render_data[i][1],int(H//2*elevation-pe/render_data[i][0])))


    #def which draws background
    def draw_background(self,elevation,maxR):
        '''
        elevation - parametr which shows y angle
        '''
        W,H = self.W,self.H

        self.sky = pygame.Surface((W,H//2+H//2*(elevation-1)-self.pe/maxR+1))
        self.ground = pygame.Surface((W,H//2-H//2*(elevation-1)-self.pe/maxR+1))

        self.gradientRect(self.sky,(153, 153, 102),(0,0,0),pygame.Rect(0,0,W,H//2+H//2*(elevation-1)-self.pe/maxR+1))
        self.gradientRect(self.ground,(0,0,0),(135,62,35),pygame.Rect(0,0,W,H//2-H//2*(elevation-1)-self.pe/maxR+1))

        self.render_surface.fill((0,0,0)) 

        self.render_surface.blit(self.sky,(0,0))
        self.render_surface.blit(self.ground,(0,H//2+H//2*(elevation-1)+self.pe/maxR-1))

    #function that calls some other to create image
    def render(self,args):
        '''
        args - banch of arguments
        '''

        map,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0,elevation = args

        render_wall_data = self.ray_cast(map,cos0,sin0,cos1,sin1,minR,maxR,x0,y0)


        enemy_render_data = self.enemy_ray_caster(render_wall_data,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0)
        render_wall_data = self.texturize(render_wall_data)

        render_wall_data.sort(key=lambda item: item[0], reverse = True)
        enemy_render_data.sort(key=lambda item: item[0], reverse = True)

        while self.blit:
            pass

        self.blit = True
        self.draw_background(elevation,maxR)
        self.draw_wall(render_wall_data, enemy_render_data,elevation)
        self.blit = False
    
    #creates background images 
    def gradientRect( self,window, left_colour, right_colour, target_rect ):
        colour_rect = pygame.Surface( ( 2, 2 ) )                          
        pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            
        pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            
        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) ) 
        window.blit( colour_rect, target_rect )      
    
    #converts wall data to textures for rendering
    def texturize(self,render_data):
        '''
        render_data - wall position and some stuff data
        '''

        width_,height_ = 200,200

        n,n_ ,texture_data= [],[],[]

        ston = self.ston
        pe,dW, w,H = self.pe,(self.dW+1),self.W,self.H*1.5

        x = 0

        for i in range(len(render_data)):
            if render_data[i][2] == 1:
                n.append(i)

        n.append(len(render_data))
    
        for j in range(len(n)-1):
            n_.append(n[j+1]-n[j])

        dark  = pygame.Surface((dW,H)).convert_alpha()

        for j in range(len(n_)):
            end = x+n_[j]
            
            k1 = min(render_data[x:end], key=lambda c: c[3])[3]
            k2 = max(render_data[x:end], key=lambda c: c[3])[3]

            end -= 1

            width,height = width_*(k2-k1) , height_ 
            texture_buffer = pygame.Surface((width , height ))
            texture_buffer.blit(ston[render_data[end][4]-1][0],(0,0),(k1*width_,0,width_,height_))
            dark.fill((0, 0, 0, render_data[x][0]*255/7))

            for i in range(n_[j]):

                h = int(2*pe/render_data[x][0])

                if h>H:
                    texture_data = pygame.Surface((dW, H))
                    texture_buffer_ = texture_buffer.subsurface((0, ((h-H)//2/h)*height, width, H/h*height))
                    texture_data.blit(pygame.transform.scale(texture_buffer_,(round(dW*n_[j]),H)),(0,0),(round(dW*i),0,dW,H))

                    texture_data.blit(dark,(0,0))
                    render_data[x][0] = 2*pe/H
                    render_data[x]= render_data[x]+[texture_data]
                else:
                    texture_data = pygame.Surface((dW, h))
                    texture_data.blit(pygame.transform.scale(texture_buffer,(round(dW*n_[j]),h)),(0,0),(round(dW*i),0,dW,h))
                    texture_data.blit(dark,(0,0))
                    render_data[x]= render_data[x]+[texture_data]

                x = x+1
        
        return render_data