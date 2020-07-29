import pygame

class Bar(pygame.sprite.Sprite):
    def  __init__(self, x, value, screen_height, liftoff, bar_width):
        super().__init__()
        y = screen_height - liftoff - value
        apricot = (252, 200, 155)

        self.image = pygame.Surface((bar_width, value))
        self.rect = pygame.Rect(liftoff, y, bar_width, value)

        self.image.fill(apricot)

