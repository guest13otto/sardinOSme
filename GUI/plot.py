import pygame
from axis import Axis, display_text
from bar import Bar
from profile import Profile
from widget import Widget
from label import Label


class Plot:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.xliftoff = 50
        self.yliftoff = 30
        self.bar_width = 11
        self.axes = Axis(screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        self.directions = [Bar(i, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
                           for i in range(11)]
        #self.profile = Profile(screen, screen_width, screen_height)
        self.profile = Widget()
        self.textTR = Label(10, screen_width-7, 'right', (0, 0, 0), 14)

    def update(self, values, profile):
        labels = ['strafe', 'drive', 'yaw', 'tilt', 'ud', 'FL', 'FR', 'BL', 'BR', 'TL', 'TR']
        self.screen.fill((200, 200, 255))

        for i in range(11):
            self.directions[i].draw(values[i], labels[i])

        self.axes.draw()

        print('profile ' + str(profile))
        #self.profile.popup(profile)
        popup = self.profile.update(profile)

        self.textTR.set_text('profile '+str(profile), self.screen)
