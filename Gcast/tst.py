import pygame
import sys
import os
import math
import time

pygame.init()

screen = pygame.display.set_mode((600, 480), pygame.SRCALPHA)

path = os.path.join(sys.path[0],"pony\\wall\\enter")
files = next(os.walk(path))
onlyfiles = next(os.walk(path)) 
print(onlyfiles)

floor = pygame.image.load(files[0]+"\\"+onlyfiles[2][0])


floorp = pygame.transform.rotate(floor,45)
floor = pygame.transform.scale(floor,(75,75))


#screen.blit(floor,(0,0))
#screen.blit(floorp,(0,0))

pygame.display.update()


h = 1

dx = 1

x =0
k = 0

xmin = 5

W = floorp.get_width()
d =0
z= 0

floorp = floor

n = 20
h = 0.8
dz = 7/n

d =0
xmin= 20

x0 = 0



print(d)

pygame.display.update()
clock = pygame.time.Clock()


floorp = pygame.Surface((75*15,75*15))

for x in range(0,15):
    for y in range(0,15):
        floorp.blit(floor,(x*75,y*75))

screen.blit(floorp,(0,0))
pygame.display.update()


x0,y0 =750,750


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pg.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

while 1:
    ground = pygame.Surface((75*3,100))
    clock.tick(30)
    cut = pygame.Surface((75*3,75*7))
    cut.blit(floorp,(0,0),(x0/100*75+75*7,y0/100*75+75*7,75*3,75*7))


    
    
    #screen.blit(cut,(0,0))
    while z < 7:
        
        l = z**2+h**2

        l = math.sqrt(l)

        dx = l*xmin
    
        line = pygame.Surface((75*3,int(dx)))
        line.blit(cut,(0,0),(0,75*z,75*3,75*7))

        line = pygame.transform.scale(line,(75*3/l,int(5)))
        ground.blit(line,(75*1.5-75*1.5/l,int(5)*d))


        x += dx
        d+=1
        z+=dz

    ground = pygame.transform.scale(ground,(640,240))
    ground = pygame.transform.flip(ground,False,True)

    screen.blit(ground,(0,240))

    #print(x)

    n = 80
    h = 1
    dz = 7/n

    d =0
    xmin= 6.68

    
    z =0
    x=0



    


    pygame.display.update()
    screen.fill((0,0,0))

    for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:



                if event.key == pygame.K_w:
                    y0+=5
                if event.key == pygame.K_s:
                    y0+=-5

                if event.key == pygame.K_a:
                    x0+=5
                if event.key == pygame.K_d:
                    x0+=-5
                if event.key == pygame.K_q:
                    a+=1
                if event.key == pygame.K_e:
                    a+=-1