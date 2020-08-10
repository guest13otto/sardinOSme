import pygame
from axis import Axis, display_text
from bar import Bar


class Plot:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.xliftoff = 50
        self.yliftoff = 30
        self.bar_width = 14
        self.axes = Axis(screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        strafe = Bar(0, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        drive = Bar(1, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        yaw = Bar(2, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        tilt = Bar(3, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        updown1 = Bar(4, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        updown2 = Bar(5, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        tpos = Bar(6, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        tdir = Bar(7, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        ttor = Bar(8, screen, screen_width, screen_height, self.xliftoff, self.yliftoff, self.bar_width)
        self.directions = [strafe, drive, yaw, tilt, updown1, updown2, tpos, tdir, ttor]

    def update(self, values):
        #values = [strafe, drive, yaw, tilt, updown1, updown2]
        labels = ['strafe', 'drive', 'yaw', 'tilt', 'ud1', 'ud2', 'tpos', 'tdir', 'torque']
        self.screen.fill((200, 200, 255))

        for i in range(9):
            self.directions[i].draw(values[i], labels[i])

        self.axes.draw()
