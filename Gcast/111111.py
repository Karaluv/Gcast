import pygame
from pygamevideo import Video
window = pygame.display.set_mode()
video = Video(os.path.join(sys.path[0] + "\\pony\\video\\", "Intro_video.mp4")) # start video
video.play() # main loop
while True: # draw video to display surface # this function must be called every tick
    video.draw_to(window, (0, 0)) # set window title to current duration of video as hour: minute: second
    t = video.current_time.format("%h:%m:%s")
    pygame.display.set_caption(t)
import pygame
import sys
pygame.init()
clo_obj = pygame.time.Clock()
movie = pygame.movie.Movie("movie_sample.mpg")
sur_obj = pygame.display.set_mode(movie.get_size())
mov_scre = pygame.Surface(movie.get_size()).convert()
movie.set_display(mov_scre)
movie.play()
while True:
    for eve in pygame.event.get():
        if eve == pygame.QUIT:
            movie.stop()
            pygame.quit()
            sys.exit()
            sur_obj.blit(mov_scre, (0, 0))
            pygame.display.update()
            clo_obj.tick(60)