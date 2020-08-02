import pygame
from axis import Axis, display_text
from bar import Bar


class Plot:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.liftoff = 100
        self.bar_width = 40
        self.axes = Axis(screen, screen_width, screen_height, self.liftoff, self.bar_width)
        strafe = Bar(0, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        drive = Bar(1, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        yaw = Bar(2, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        tilt = Bar(3, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        updown1 = Bar(4, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        updown2 = Bar(5, screen, screen_width, screen_height, self.liftoff, self.bar_width)
        self.directions = [strafe, drive, yaw, tilt, updown1, updown2]

    def update(self, strafe, drive, yaw, tilt, updown1, updown2):
        values = [strafe, drive, yaw, tilt, updown1, updown2]
        labels = ['strafe', 'drive', 'yaw', 'tilt', 'updown1', 'updown2']
        self.screen.fill((200, 200, 255))

        for i in range(6):
            self.directions[i].draw(values[i], labels[i])

        self.axes.draw()
