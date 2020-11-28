import pygame
from label import display_text


class Bar(pygame.sprite.Sprite):
    def __init__(self, order, screen, screen_width, screen_height, xliftoff, yliftoff, bar_width):
        super().__init__()
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bar_width = bar_width
        self.xlim = (self.screen_width - (xliftoff + 10)) / 2
        self.y = screen_height - (yliftoff + 2 * (6-order) * bar_width)
        self.valuey = self.y + bar_width / 2
        self.labelx = 10
        self.xliftoff = xliftoff
        twice0 = (255, 212, 168)
        twice1 = (252, 200, 155)
        twice2 = (253, 179, 165)
        twice3 = (254, 151, 164)
        twice4 = (254, 123, 163)
        twice5 = (255, 95, 162)
        twice = [twice0, twice1, twice2, twice3, twice4, twice5, twice5, twice4, twice3, twice2, twice1, twice0]
        self.colour = twice[order]

    def draw(self, screen, value, label):
        self.screen = screen
        bar_length = abs(value) * (self.xlim / 1.1)
        if value >= 0:
            x = self.xliftoff + self.xlim
            value = '+' + '%.3f' % value
        else:
            x = self.xliftoff + self.xlim - (bar_length - 1)
            value = '%.3f' % value
        display_text(label, self.screen, self.labelx, self.valuey-7, 'left', 14)
        rect = pygame.Rect(x, self.y, bar_length, self.bar_width)
        pygame.draw.rect(self.screen, self.colour, rect)
        display_text(str(value), self.screen, self.labelx, self.valuey+7, 'left', 14)
        return self.screen
