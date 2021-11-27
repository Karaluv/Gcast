import cv2
import os
import pygame
import sys

cap = cv2.VideoCapture(os.path.join(sys.path[0] + "\\pony\\video\\", "Intro_video.mp4"))
success, img = cap.read()
shape = img.shape[1::-1]
wn = pygame.display.set_mode(shape)
clock = pygame.time.Clock()

pygame.init()
    
pygame.mixer.music.load(os.path.join(sys.path[0] + "\\pony\\music\\", "Intro_sound.mp3"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(1)

while success:
    clock.tick(24)
    success, img = cap.read()
    if (img is None):
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            success = False
            break
    wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
    pygame.display.update()

pygame.quit()