import pygame
import numpy as np
from axis import Axis
from bar import Bar
from profile import Profile
from pubsub import pub


class Plot:
    def __init__(self, labels, screen_width, screen_height):
        self.screen_width = screen_width / 2
        self.screen_height = screen_height
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        self.xliftoff = 50
        self.yliftoff = 50
        self.bar_width = 17
        self.labels = labels
        self.axes = Axis(self.screen, self.screen_width, self.screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        self.movement = [0, 0, 0, 0, 0, 0]
        self.profile = 0
        self.power = [0, 0, 0, 0, 0, 0]
        self.charts = 0
        pub.subscribe(self.movement_handler, "gamepad.movement")
        pub.subscribe(self.profile_handler, "gamepad.profile")
        pub.subscribe(self.power_handler, "Thruster.Power")

    def update(self, order):
        self.update_charts()
        values = self.charts[order]
        directions = [Bar(i, self.screen, self.screen_width, self.screen_height, self.xliftoff, self.yliftoff, self.bar_width)
                           for i in range(6)]
        self.screen.fill((200, 200, 255))
        self.screen = self.axes.draw()

        for i in range(6):
            self.screen = directions[i].draw(self.screen, values[i], self.labels[i])

        return self.screen

    def movement_handler(self, message):
        self.movement = message["gamepad_message"]

    def profile_handler(self, message):
        self.profile = message

    def power_handler(self, message):
        self.power = message["Thruster_message"][0]

    def update_charts(self):
        self.charts = [self.movement, self.power]
