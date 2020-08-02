import pygame


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
        apricot = (252, 200, 155)
        self.colour = apricot

    def draw(self, value):
        bar_length = abs(value) * (self.xlim / 1.1)
        if value > 0:
            x = self.screen_width/2
        else:
            x = self.screen_width/2 - bar_length
        rect = pygame.Rect(x, self.y, bar_length, self.bar_width)
        pygame.draw.rect(self.screen, self.colour, rect)

