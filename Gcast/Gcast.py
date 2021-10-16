import pygame
import math
from random import randint
import os
import sys
from pygame.locals import Color
from pygame import display


FPS = 60
u = 0.5


class wall:

    def __init__(self,color,texture,p1,p2):
        self.color = color
        self.texture = texture
        self.p1 = p1
        self.p2 = p2

class map:

    def __init__(self, walls):
        self.walls = walls


        self.map_claster = [[1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,1],[1,0,0,0,1,0,0,0,1],[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1]]
        #self.map_claster = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.hm,self.wm = 5,9

        self.freemap = [[0]*self.wm]*self.hm

        

    def ray_cast(self,density,dl,a0,a1,minR,maxR,x0,y0):
        
        global pe
        wm,hm = self.wm,self.hm
        mapC =[[0]*wm]*hm
        mapP = [[0]*wm]*hm
        render_data = []
        a=a0
        render_pol = []
        while a < a1:
            
            mapP = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
            
            x , y = 0,0
            render_data.append((1000,-1))
            l = minR
            
            sin =math.sin(a)*dl
            cos=math.cos(a)*dl

            render_pol_buffer = []
            
            while l <maxR:


                renderZ = self.map_claster[int(y+y0/stepy)][int(x+x0/stepx)]

                if mapP[int(y+y0/stepy)][int(x+x0/stepx)] == 0:
                    render_pol_buffer.append(l)
                    mapP[int(y+y0/stepy)][int(x+x0/stepx)] += 1

                if renderZ>0:
                    


                    mapC[int(y+y0/stepy)][int(x+x0/stepx)]=mapC[int(y+y0/stepy)][int(x+x0/stepx)]+1
                    
                    render_data[-1]=(l,mapC[int(y+y0/stepy)][int(x+x0/stepx)])

                    #if mapC[int(y+y0/stepy)][int(x+x0/stepx)]==1:
                    k = (  (round(y+y0/stepy)-y0/stepy-y)**2 +(round(x+x0/stepx)-x0/stepx-x)**2 )**0.5
                    
                    render_data[-1]=(l,mapC[int(y+y0/stepy)][int(x+x0/stepx)],k)


                    render_pol.append(render_pol_buffer)



                    break
                y = y + sin
                x = x + cos
                l = l+dl
            a = a + density
        #print(len(render_data),len(render_pol))
        return render_data,render_pol


def texturize(render_data):
    n = []
    stone = []
    n_=[]


    for i in range(len(render_data)):

        if render_data[i][1] == 1:
            n.append(i)

    n.append(len(render_data))
    
    for j in range(len(n)-1):
        n_.append(n[j+1]-n[j])
    x = 0
    for j in range(len(n_)):

        k1 = render_data[x][2]
        k2 = abs(1-render_data[x+n_[j]-1][2])

        #k2 = 1
        #k1 = 0

        if k2<k1:
            k2,k1 = k1,k2

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

 

class slave:
    x = 0


class billy:
    
    def __init__(self, x,y,a,name):
        self.x = x
        self.y = y
        self.a = a
        self.name = name

    def Rotate(self,a):
        self.a = self.a +a
        global move
        move = True

    def Move(self,l,n):
        a = self.a
        x_ = self.x+l*math.sin(a)+n*math.cos(a)
        y_ = self.y+l*math.cos(a)+n*math.sin(a)
        global map1
        if map1.map_claster[int(y_/100+0.25)][int(x_/100+0.25)] == 0:
            if map1.map_claster[int(y_/100-0.25)][int(x_/100-0.25)] == 0:
                if map1.map_claster[int(y_/100-0.25)][int(x_/100+0.25)] == 0:
                    if map1.map_claster[int(y_/100+0.25)][int(x_/100-0.25)] == 0:
                        self.y = y_
                        self.x = x_


def rotate_point(angle,p,po):
    x_ = po[0] + math.cos(angle) * (p[0] - po[0]) - math.sin(angle) * (p[1] - po[1])
    y_ = po[1] + math.sin(angle) * (p[0] - po[0]) + math.cos(angle) * (p[1] - po[1])
    return (x_,y_)

def draw_2d():
    claster= map1.map_claster
    x0 = pe
    y0 = pe

    for y in range(len(claster)):
        for x in range(len(claster[y])):
            if claster[y][x]!= 0:
                
                pygame.draw.rect(screen,(128,128,128),(x*x0,y*y0,x0,y0),2)

def draw_pol(a0,a1,density,render_pol):
    x,y = bill.x,bill.y
    i = 0
    
 
    w = 0
    dw = W*density / (2*u) 

    cl1 = (255,188,255)
    cl2 =(100,100,255)

    while w<W-1:

        for j in range(len(render_pol[i])):

            cl1_ = render_pol[i][j]/7*cl1[0],render_pol[i][j]/7*cl1[1],render_pol[i][j]/7*cl1[2]
            cl2_ = render_pol[i][j]/7*cl2[0],render_pol[i][j]/7*cl2[1],render_pol[i][j]/7*cl2[2]

            cl1__ = cl1[0] - cl1_[0],cl1[1] - cl1_[1],cl1[2] - cl1_[2]
            cl2__ = cl2[0] - cl2_[0],cl2[1] - cl2_[1],cl2[2] - cl2_[2]

            pygame.draw.line(screen,cl1__,(w-i,H//2+ pe/render_pol[i][j]),(w+dw-i,H//2+ pe/render_pol[i][j]),2)
            pygame.draw.line(screen,cl2__,(w-i,H//2- pe/render_pol[i][j]),(w+dw-i,H//2 -  pe/render_pol[i][j]),2)
        w = w+dw
        i=i+1

def draw_wall(a0,a1,density,render_data):

    x,y = bill.x,bill.y
    i = 0
    
 
    w = 0
    dw = W*density / (2*u) 

    stone = texturize(render_data)


    while w < W-1:
        screen.blit(stone[i],(w-i,int(H//2-pe/render_data[i][0])))
        #pygame.draw.rect(screen,(128,255,128),(w,H//2-pe/render_data[i][0],dw,2*pe/render_data[i][0]),0)
        w = w+dw
        
        i = i+1

        
def draw_ray2d(a0,a1,density,render_data):
    x,y = bill.x,bill.y
    i = 0

    cl = (255,128,128)

    a = a0

    while a < a1:

        
        
        pygame.draw.line(screen,cl_,(x,y),(x+math.cos(a)*render_data[i][0]*pe,y+math.sin(a)*render_data[i][0]*pe),2)
        i = i+1
        a = a+ density


def render():
    
    for i in map1.index:
        draw_wall(map1.walls[i],map1.l1[i],map1.l2[i])

def start():
    global pe
    print("start")
    bill = billy(150,150,-math.pi/2,"VAn")
    wall1 = wall((128,128,128),False,(-100,200),(100,200))
    wall2 = wall((128,128,0),False,(-100,100),(100,100)) 
    walls = [wall1,wall2]
    return  map(walls), bill

def input(user_input):


    keys=pygame.key.get_pressed()

    #if keys[K_s]:
    #   map1.Move(10,0)
    #if keys[K_w]:
    #   map1.Move(-10,0)
    #if keys[K_d]:
    #   map1.Move(0,10)
    #if keys[K_a]:
    #   map1.Move(0,-10)

    #if keys[K_q]:
    #   map1.Rotation_map(0.01,(0,0))
    #if keys[K_e]:
    #   map1.Rotation_map(-0.01,(0,0))


    for event in user_input:
        global kw,ks,kd,ka

        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_q:
            #   finished = True
            if event.key == pygame.K_w:
                kw =True
            if event.key == pygame.K_s:
                ks =True
            if event.key == pygame.K_a:
                ka =True
            if event.key == pygame.K_d:
                kd =True

            if event.key == pygame.K_q:
                bill.Rotate(-0.1)
            if event.key == pygame.K_e:
                bill.Rotate(0.1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                kw =False
            if event.key == pygame.K_s:
                ks =False
            if event.key == pygame.K_a:
                ka =False
            if event.key == pygame.K_d:
                kd =False

        

        bill.Rotate((-W/2 +  pygame.mouse.get_pos()[0])/200)
        pygame.mouse.set_pos((W//2,H//2))
 

        if event.type == pygame.QUIT:
            #quit and save part
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            #mouse event part
            #shoot(event.pos)
            print("shoot")



def update():

    #screen.blit(nacl(pygame.transform.rotate(floor,bill.a),0.8),(0,H//2))
    

    gradientRect(screen,(0,0,0),(128,50,128),pygame.Rect(0,H//2,W,H//2))
    gradientRect(screen,(128,50,50),(0,0,0),pygame.Rect(0,0,W,H//2))
    
    a = bill.a

    
    
    render_data,render_pol = map1.ray_cast(0.01,0.01,a-u,a+u,0.01,600,bill.x,bill.y)

    
    
    draw_wall(a-u,a+u,0.01,render_data)
    draw_pol(a-u,a+u,0.01,render_pol)
    #draw_ray2d(a - u,a + u,0.01,render_data)
    #draw_ray2d(a-u,a+u,0.01,render_data)

pygame.init()

pygame.mouse.set_visible(False)

infoObject = pygame.display.Info()

W,H = infoObject.current_w, infoObject.current_h

W,H = W // 2,H // 2
ys = 10
h0 = 10000
l0 = 100
w0 = 1
dens = 0.01
dw = W*0.01 / (2*u) 


ston = pygame.image.load(os.path.join(sys.path[0],"stone.png"))
floor =  pygame.image.load(os.path.join(sys.path[0],"floor.jpg"))
floor = pygame.transform.scale(floor,(int(W*8.76/10.1),H//2))

i =0

move = False


#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.FULLSCREEN)

screen = pygame.display.set_mode((infoObject.current_w // 2, infoObject.current_h // 2))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
bl = (0,0,0)
map1,bill = start()
L0 = 25
pe =200
stepx =100
stepy = 100

kw,ks,ka,kd = False,False,False,False

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it



#main loop
while not finished:
    clock.tick(FPS)
    
    input(pygame.event.get())
    update()
    pygame.display.flip()
    screen.fill(bl)

    if kw:
        bill.Move(0,3)
    if ks:
        bill.Move(0,-3)
    if ka:
        bill.Move(-3,0)
    if kd:
        bill.Move(3,0)

    
