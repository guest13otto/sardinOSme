import pygame
from pubsub import pub
import time


class ProfilePopup:
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((400, 300))
        self.profile = -1
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.labels = ['profile ' + str(i) for i in range(4)]
        self.font = pygame.font.SysFont("Courier New", 14)
        pub.subscribe(self.profile_handler, "gamepad.profile")
        self.expired = time.time()

    def profile_handler(self, message):
        self.set_profile(message)

    def set_profile(self, profile):
        if profile != self.profile:
            self.expired = time.time() + 2
        self.profile = profile

    def update(self):
        if self.expired > time.time():
            self.surface.fill(self.colours[self.profile])
            self.surface.set_alpha(255)
            '''
            textSurf = self.font.render(self.labels[self.profile], True, self.colours[self.profile])
            textRect = textSurf.get_rect()
            textRect.center = (200, 150)
            self.surface.blit(textSurf, (0, 0))
            '''
        else:
            self.surface.fill((0, 0, 0))
            self.surface.set_alpha(0)
        return self.surface #, textSurf, textRect