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



class rendering(threading.Thread):



    def __init__(self,u,density,dl,render_surface,height,width,update,redraw):

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
            self.ston[-1][-1] = pygame.transform.scale(self.ston[-1][-1],(200,200))


        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\flag")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
            self.ston[-1][-1] = pygame.transform.scale(self.ston[-1][-1],(200,200))



        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\flagblood")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
            self.ston[-1][-1] = pygame.transform.scale(self.ston[-1][-1],(200,200))

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\enter")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
            self.ston[-1][-1] = pygame.transform.scale(self.ston[-1][-1],(200,200))

        self.ston.append([])
        path = os.path.join(sys.path[0],"pony\\wall\\exit")
        files = next(os.walk(path))
        onlyfiles = next(os.walk(path)) 
        print(onlyfiles)
        for i in range(len(onlyfiles[2])):
            print(files[0]+"\\"+onlyfiles[2][i])
            self.ston[-1].append(pygame.image.load(files[0]+"\\"+onlyfiles[2][i]).convert_alpha())
            self.ston[-1][-1] = pygame.transform.scale(self.ston[-1][-1],(200,200))

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




        
        self.sprites = tuple(tuple(i) for i in self.sprites)
        self.ston = tuple(tuple(i) for i in self.ston)

        self.pe = 100
        self.stepx =100
        self.stepy = 100

        self.pi_2 = math.pi*2

        maxR = 7
        
        self.sky = pygame.Surface((W,H//2-self.pe/maxR+1))
        self.ground = pygame.Surface((W,H//2-self.pe/maxR+1))

        self.gradientRect(self.sky,(153, 153, 102),(0,0,0),pygame.Rect(0,0,W,H//2-self.pe/maxR+1))
        self.gradientRect(self.ground,(0,0,0),(135,62,35),pygame.Rect(0,0,W,H//2-self.pe/maxR+1))

        self.width = width
        self.height = height

        self.fps = 60

        self.xs = 618

        self.blit = False


        self.update = update

        self.redraw = redraw

        threading.Thread.__init__(self)


        


    def run(self):

        import time


        time.sleep(0.5)

        while 1:

            self.render(self.update())
            self.redraw()


    @lru_cache()
    def find_clothest_point(self,map,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        

        while map[int(yc)][int(xc)]!=0:
            l -= lc
            xc -= cos
            yc -= sin

        if lc <= lmin:
            return xc+cos,yc+sin,l+lc
        if lc>lmin:
            return self.find_clothest_point(map,l+lc,xp,yp,xc+cos,yc+sin,cos/10,sin/10,lc/10,lmin)

    @lru_cache()
    def find_clothest_gran(self,l,xp,yp,xc,yc,cos,sin,lc,lmin):
        

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

    
    def enemy_ray_caster(self,wall_data,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0):

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


    def ray_cast(self,map,cos,sin,cos1,sin1,minR,maxR,x0,y0):


        dl,pe,stepx,stepy,width,height,density,w = self.dl,self.pe,self.stepx,self.stepy,self.width, self.height,self.density,self.W

        history =[]
        

        mapCH = [[0 for _ in range(width)] for _ in range(height)]
        mapCV = [[0 for _ in range(width)] for _ in range(height)]

        render_data = []

        VM = False

        dcos = (cos1 - cos)*density*dl
        dsin = (sin1 - sin)*density*dl
        sin = sin*dl
        cos = cos*dl

        t = 0
        k = 1
        d = 0

        ugol = 1

        sc = 4
        x,y =0,0

        rX,rY = int(x+x0/stepx),int(y+y0/stepy)
        

        while t < 1:

            if ugol == 0:
                sc = 1

            x , y, l= 0,0,minR
            
            
            xp,yp = rX,rY

            render_data.append([maxR,t*w-d,1,0,1])
            history.append([0,0,True])

            
            
            while l <maxR:
                rX,rY = int(x+x0/stepx),int(y+y0/stepy)

                #этот if можешь закоментить если сложно
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
                        render_data[-1]=[l, t*w-d,mapCH[rY][rX],k,map[rY][rX]]
                    else:
                        mapCV[rY][rX] += 1
                        render_data[-1]=[l, t*w-d,mapCV[rY][rX],k,map[rY][rX]]

                    history[-1]=[rX,rY,VM]

                    
                    if ugol == 0:
                        if len(render_data)>3:
                            if l<render_data[-2][0]-1:

  
                                
                                if l - 1>minR:

                                    ugol = min(int(dl/density),len(render_data)-2)
                                
                                    for i in range(len(render_data)-ugol-1,len(render_data)):

                                        if history[i][2]:
                                            mapCV[history[i][1]][history[i][0]] -= 1
                                        else:
                                            mapCH[history[i][1]][history[i][0]] -= 1
                                
                                    sc = 4
  
                                    sin -= (ugol+1)*dsin
                                    cos -=(ugol+1)*dcos

                                    d -= (ugol+1)
                                    t -= (ugol+1)*density
                                
                                    del render_data[-(ugol+1):]
                                    del history[-(ugol+1):]


                                    rX,rY,VM = history[-(1)][0],history[-(1)][1],history[-(1)][2]

                                    ugol +=1

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

            t += density
            
            d+= 1


        return render_data





    def draw_wall(self,render_data,enemies):
        
        sprites= self.sprites

        W,H,pe,dw,density = self.W,self.H,self.pe,self.dw,self.density

        i,w,j,i_max = 0,0,0,int(1 / density)
        
        while i <= i_max:
            if j<len(enemies):
                if render_data[i][0]<enemies[j][0]:
                    render_image = pygame.transform.scale(sprites[enemies[j][2]][int(enemies[j][3])],(int(pe/enemies[j][0]),int(pe/enemies[j][0]*1.4)))

                    render_mask = pygame.mask.from_surface(render_image)
                    render_mask = render_mask.to_surface()
                    dark = pygame.Surface(render_image.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, min(255,enemies[j][0]*255/7)))
                    render_image.blit(dark,(0,0))

                    render_image.blit(render_image, (0, 0), None, pygame.BLEND_RGBA_MULT)
                    render_mask.set_colorkey((255,255,255))
                    render_image.blit(render_mask, (0, 0))
                    render_image.set_colorkey((0,0,0))

                    self.render_surface.blit(render_image,(int(enemies[j][1]*(dw-1)-pe/enemies[j][0]/2),int(H//2-pe/enemies[j][0]*0.4)))
                    j += 1

            self.render_surface.blit(render_data[i][5],(render_data[i][1],int(H//2-pe/render_data[i][0])))

            #pygame.draw.rect(self.render_surface,(128,128,128),(render_data[i][1],int(H//2-pe/render_data[i][0]),int(dw),int(pe/render_data[i][0])))
            w +=dw
            i +=1

        return w-i-dw

    def draw_background(self):
        maxR = 7
        W,H = self.W,self.H

        
        self.render_surface.blit(self.sky,(0,0))
        self.render_surface.blit(self.ground,(0,H//2+self.pe/maxR-1))

    def render(self,args):

        map,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0 = args

        render_wall_data = self.ray_cast(map,cos0,sin0,cos1,sin1,minR,maxR,x0,y0)

        # на это похуй
        

        enemy_render_data = self.enemy_ray_caster(render_wall_data,enemies,cos0,sin0,cos1,sin1,minR,maxR,x0,y0)

        # в этой функции меняется 6й элемент массива - surface
        render_wall_data = self.texturize(render_wall_data)
        
        # блок сортировки переделать под tuple с сортировкой строк по первому элементу в порядке убывания
        render_wall_data.sort(key=lambda item: item[0], reverse = True)
        enemy_render_data.sort(key=lambda item: item[0], reverse = True)


        while self.blit:
            pass
        self.blit = True
        self.draw_background()
        res = self.draw_wall(render_wall_data, enemy_render_data)
        self.blit = False

        self.xs = res
     
    def gradientRect( self,window, left_colour, right_colour, target_rect ):
        colour_rect = pygame.Surface( ( 2, 2 ) )                          
        pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            
        pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            
        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) ) 
        window.blit( colour_rect, target_rect )      
    
    def texturize(self,render_data):

        width_,height_ = 200,200

        n,n_ ,texture_data= [],[],[]

        ston = self.ston
        pe,dw, w,H = self.pe,self.dw,self.W,self.H

        x = 0


        for i in range(len(render_data)):
            if render_data[i][2] == 1:
                n.append(i)

        n.append(len(render_data))
    
        for j in range(len(n)-1):
            n_.append(n[j+1]-n[j])

        dark  = pygame.Surface((dw,H)).convert_alpha()

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
                    texture_data = pygame.Surface((dw, H))
                    texture_buffer_ = texture_buffer.subsurface((0, ((h-H)//2/h)*height, width, H/h*height))
                    texture_data.blit(pygame.transform.scale(texture_buffer_,(round(dw*n_[j]),H)),(0,0),(round(dw*i),0,dw,H))

                    texture_data.blit(dark,(0,0))
                    render_data[x][0] = 2*pe/H
                    render_data[x]= render_data[x]+[texture_data]
                else:
                    texture_data = pygame.Surface((dw, h))
                    texture_data.blit(pygame.transform.scale(texture_buffer,(round(dw*n_[j]),h)),(0,0),(round(dw*i),0,dw,h))
                

                    texture_data.blit(dark,(0,0))
                    render_data[x]= render_data[x]+[texture_data]

                x = x+1
        
        return render_data




