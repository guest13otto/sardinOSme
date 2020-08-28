import pygame
'''
positions:
top left (0, 0)
top right (0, 1)
bottom left (1, 0)
bottom right (1, 1)
'''


class Label:
    def __init__(self, surface, screen_width, screen_height, position, colour, size):
        if position[1] == 0:
            self.alignment = 'left'
            self.x = 10
        else:
            self.alignment = 'right'
            self.x = screen_width - 10
        if position[0] == 0:
            self.y = 15
        else:
            self.y = screen_height - 15
        self.colour = colour
        self.size = size
        self.font = pygame.font.SysFont("Courier New", size)
        self.surface = surface

    def update(self, text):
        display_text(text, self.surface, self.x, self.y, self.alignment, self.colour, self.size)


def display_text(text, surface, x, y, alignment, colour, size):
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
    surface.blit(textSurf, textRect)
