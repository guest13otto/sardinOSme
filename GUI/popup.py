import pygame
from pubsub import pub
from label import Label
import time


class ProfilePopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((400, 300))
        self.profile = -1
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.pArr = ['A', 'B', 'C', 'D']
        self.labels = ['profile ' + self.pArr[i] for i in range(4)]
        self.font = pygame.font.SysFont("Courier New", 32)
        pub.subscribe(self.profile_handler, "gamepad.profile")
        self.expired = time.time()

    def profile_handler(self, message):
        self.set_profile(message["gamepad_profile"])

    def set_profile(self, profile):
        for i in range(len(self.pArr)):
            if profile == self.pArr[i]:
                profile = i
        if profile != self.profile:
            self.expired = time.time() + 2
        self.profile = profile

    def update(self):
        if self.expired > time.time():
            self.surface.fill(self.colours[self.profile])
            #self.surface.set_alpha(255)
            self.surface.set_colorkey()

            textSurf = self.font.render(self.labels[self.profile], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (200, 150)
            self.surface.blit(textSurf, textRect)
        else:
            self.surface.fill((1, 1, 1))
            #self.surface.set_alpha(0)
            self.surface.set_colorkey((1, 1, 1))
            label = Label(self.surface, self.screen_width, self.screen_height, (0, 1), 'b', 14)
            label.update(self.labels[self.profile])
            #self.surface.blit(label.update(self.labels[self.profile]), (0, 0))
        return self.surface
