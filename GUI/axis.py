import pygame

class Axis(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, liftoff, bar_width):
        super.__init__()
        self.Y_LIMIT = bar_width * (6*2+1)
        self.X_LIMIT = screen_width - liftoff * 2
        self.liftoff =  liftoff
        self.screen_height = screen_height

    def draw(self):
        magenta = (255, 95, 162)
        axis_width = 2

        #draw x axis
        xDivSurface = (axis_width, 10)
        xDiv = self.X_LIMIT / 11
        xSurface = (self.X_LIMIT, axis_width)
        y = self.screen_height - self.liftoff
        xStart = (self.liftoff, y)
        xEnd = (self.liftoff+self.X_LIMIT, y)
        pygame.draw.line(xSurface, magenta, xStart, xEnd, axis_width)
        for i in range(10):
            x = self.liftoff+xDiv*(i+1)
            pygame.draw.line(xDivSurface, magenta, (x, y-5), (x, y+5), axis_width)

        #draw y axis
        ySurface = (axis_width, self.Y_LIMIT)
        yStart = (self.screen_height-self.liftoff-self.Y_LIMIT, self.liftoff)
        yEnd = (self.screen_height-self.liftoff, self.liftoff)
        pygame.draw.line(ySurface, magenta, yStart, yEnd, axis_width)



