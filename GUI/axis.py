import pygame


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
            if i == 0:
                display_text('-1', self.screen, x, y+15, 'center', 'b', 14)
            elif i == 10:
                display_text('0', self.screen, x, y+15, 'center', 'b', 14)
            elif i == 20:
                display_text('1', self.screen, x, y+15, 'center', 'b', 14)

        # draw y axis
        yStart = (self.xliftoff+self.xlim/2, self.screen_height-self.yliftoff-self.ylim)
        yEnd = (self.xliftoff+self.xlim/2, self.screen_height-self.yliftoff)
        pygame.draw.line(self.screen, magenta, yStart, yEnd, axis_width)
        return self.screen


def display_text(text, screen, x, y, alignment, colour, size):
    black = (0, 0, 0)
    if colour == 'b':
        colour = black
    font = pygame.font.SysFont("Courier New", size)
    textSurf = font.render(text, True, colour)
    textRect = textSurf.get_rect()
    if alignment == 'left':
        textRect.left = x
        textRect.centery = y
    elif alignment == 'right':
        textRect.right = x
        textRect.centery = y
    else:
        textRect.center = (x, y)
    screen.blit(textSurf, textRect)
