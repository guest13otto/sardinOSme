import pygame
from axis import display_text

class Bar(pygame.sprite.Sprite):
    def __init__(self, order, screen, screen_width, screen_height, liftoff, bar_width):
        super().__init__()
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.liftoff = liftoff
        self.bar_width = bar_width
        self.xlim = (self.screen_width - self.liftoff * 2) / 2
        self.y = screen_height - (liftoff + 2 * (6-order) * bar_width)
        self.valuey = self.y + bar_width / 2
        self.labelx = 10
        apricot = (252, 200, 155)
        self.colour = apricot

    def draw(self, value, label):
        bar_length = abs(value) * (self.xlim / 1.1)
        if value >= 0:
            x = self.screen_width/2
            valuex = x + bar_length + 5
            alignment = 'left'
        else:
            x = self.screen_width/2 - bar_length
            valuex = x - 5
            alignment = 'right'
        display_text(label, self.screen, self.labelx, self.valuey, 'left')
        rect = pygame.Rect(x, self.y, bar_length, self.bar_width)
        pygame.draw.rect(self.screen, self.colour, rect)
        display_text(str(value), self.screen, valuex, self.valuey, alignment)
