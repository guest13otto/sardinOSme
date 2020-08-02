import pygame


class Axis(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height, liftoff, bar_width):
        super().__init__()
        self.screen = screen
        self.ylim = bar_width * (6*2+1)
        self.xlim = screen_width - liftoff * 2
        self.liftoff = liftoff
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self):
        magenta = (255, 95, 162)
        axis_width = 2

        # draw x axis
        xDiv = self.xlim / 22
        y = self.screen_height - self.liftoff
        xStart = (self.liftoff, y)
        xEnd = (self.liftoff+self.xlim, y)
        pygame.draw.line(self.screen, magenta, xStart, xEnd, axis_width)
        for i in range(21):
            x = self.liftoff+xDiv*(i+1)
            pygame.draw.line(self.screen, magenta, (x, y-5), (x, y+5), axis_width)

        # draw y axis
        yStart = (self.screen_width/2, self.screen_height-self.liftoff-self.ylim)
        yEnd = (self.screen_width/2, self.screen_height-self.liftoff)
        pygame.draw.line(self.screen, magenta, yStart, yEnd, axis_width)

