import pygame
from axis import display_text
import time


class Profile(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height):
        super().__init__()
        self.profile = -1
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text = ''
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.labels = ['profile ' + str(i) for i in range(4)]
        self.labelx = self.screen_width - 7
        self.labely = 10

    def popup(self, profile):
        if profile != self.profile:
            self.profile = profile
            self.screen.fill(self.colours[profile])
            display_text(self.labels[profile], self.screen, self.screen_width/2, self.screen_height/2, 'center', 'b', 20)
            time.sleep(20)
            self.text = self.labels[profile]

        display_text(self.text, self.screen, self.labelx, self.labely, 'right', self.colours[profile], 14)
