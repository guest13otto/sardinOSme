import pygame
from axis import display_text

class Bar(pygame.sprite.Sprite):
    def __init__(self, order, screen, screen_width, screen_height, xliftoff, yliftoff, bar_width):
        super().__init__()
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bar_width = bar_width
        self.xlim = (self.screen_width - xliftoff * 2) / 2
        self.y = screen_height - (yliftoff + 2 * (9-order) * bar_width)
        self.valuey = self.y + bar_width / 2
        self.labelx = 10
        apricot = (252, 200, 155)
        twice1 = (252, 207, 166)
        twice2 = (253, 179, 165)
        twice3 = (254, 151, 164)
        twice4 = (254, 123, 163)
        twice5 = (255, 95, 162)
        twice = [twice1, twice2, twice3, twice4, twice5, twice4, twice3, twice2, twice1]
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        green = (0, 255, 0)
        cyan = (0, 255, 255)
        blue = (0, 0, 255)
        magenta = (255, 0, 255)
        colours = [red, yellow, green, cyan, blue, magenta]
        self.colour = twice[order]

    def draw(self, value, label):
        bar_length = abs(value) * (self.xlim / 1.1)
        if value >= 0:
            x = self.screen_width/2
            valuex = x + bar_length + 5
            alignment = 'left'
        else:
            x = self.screen_width/2 - (bar_length - 1)
            valuex = x - 5
            alignment = 'right'
        display_text(label + ' ' + str('%.3f' % value), self.screen, self.labelx, self.valuey, 'left')
        rect = pygame.Rect(x, self.y, bar_length, self.bar_width)
        pygame.draw.rect(self.screen, self.colour, rect)
        #display_text(str('%.3f'%value), self.screen, valuex, self.valuey, alignment)
