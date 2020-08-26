import pygame
import numpy as np
from axis2 import Axis2, display_text
from bar2 import Bar2
from profile import Profile
from label import Label
from pubsub import pub


class Plot2:
    def __init__(self, labels, screen_width, screen_height):
        self.screen_width = screen_width / 2
        self.screen_height = screen_height
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.xliftoff = 50
        self.yliftoff = 30
        self.bar_width = 20
        self.labels = labels
        self.axes = Axis2(self.screen, self.screen_width, self.screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        #self.profile = Profile(screen, screen_width, screen_height)
        self.textTR = Label(screen_width-7, 10, 'right', (0, 0, 0), 14)
        self.movement = 0
        self.profile = 0
        self.power = 0
        self.charts = 0
        pub.subscribe(self.movement_handler, "gamepad.movement")
        pub.subscribe(self.profile_handler, "gamepad.profile")
        pub.subscribe(self.power_handler, "thruster.power")

    def update(self, order):
        self.update_charts()
        values = self.charts[order]
        directions = [Bar2(i, self.screen, self.screen_width, self.screen_height, self.xliftoff, self.yliftoff, self.bar_width)
                           for i in range(6)]
        self.screen.fill((200, 200, 255))
        self.screen = self.axes.draw()

        for i in range(6):
            self.screen = directions[i].draw(self.screen, values[i], self.labels[i])

        return self.screen

    def movement_handler(self, message):
        self.movement = message

    def profile_handler(self, message):
        self.profile = message

    def power_handler(self, message):
        self.power = message

    def update_charts(self):
        self.charts = [self.movement, self.power]