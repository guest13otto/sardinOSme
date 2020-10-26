import pygame
from label import display_text


class Axis(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height, xliftoff, yliftoff, bar_width):
        super().__init__()
        self.screen = screen
        self.xlim = screen_width - (xliftoff + 10)
        self.ylim = bar_width * (6*2+1)
        self.xliftoff = xliftoff
        self.yliftoff = yliftoff
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self):
        pygame.init()
        magenta = (255, 95, 162)
        axis_width = 2

        # draw x axis
        xDiv = self.xlim / 22
        y = self.screen_height - self.yliftoff
        xStart = (self.xliftoff, y)
        xEnd = (self.xliftoff+self.xlim, y)
        pygame.draw.line(self.screen, magenta, xStart, xEnd, axis_width)
        for i in range(21):
            x = self.xliftoff+xDiv*(i+1)
            pygame.draw.line(self.screen, magenta, (x, y-5), (x, y+5), axis_width)
            if i % 5 == 0:
                if i % 10 == 0:
                    display_text(str(int(i/10 - 1)), self.screen, x, y+15, 'center', 14)
                else:
                    pygame.draw.line(self.screen, (168, 128, 186), (x+1, y-self.ylim), (x+1, y-5))

        # draw y axis
        yStart = (self.xliftoff+self.xlim/2, self.screen_height-self.yliftoff-self.ylim)
        yEnd = (self.xliftoff+self.xlim/2, self.screen_height-self.yliftoff)
        pygame.draw.line(self.screen, magenta, yStart, yEnd, axis_width)
        return self.screen
