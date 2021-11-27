import moviepy.editor
import moviepy.video.fx.all
import pygame
class VideoSprite(pygame.sprite.Sprite):
    def __init__(self, rect, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((rect.width, rect.height), pygame.HWSURFACE)
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.video = moviepy.editor.VideoFileClip(filename).resize((self.rect.width, self.rect.height))
        self.video_stop = False
    def update(self, time = pygame.time.get_ticks()):
        if not self.video_stop:
            try: raw_image = self.video.get_frame(time / 1000) # / 1000
            for time in s:
                self.image = pygame.image.frombuffer(raw_image, (self.rect.width, self.rect.height), 'RGB')
                except: self.video_stop = True