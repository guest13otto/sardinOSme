import pygame
'''
positions:
top left (0, 0)
top right (0, 1)
bottom left (1, 0)
bottom right (1, 1)
'''


class Label:
    def __init__(self, screen_width, screen_height, position, size, **kwargs):
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
        self.colour = kwargs.get('colour', None)
        self.size = size
        self.bgColour = kwargs.get('bgColour', None)
        self.font = pygame.font.SysFont("Courier New", size)
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.fill((1, 1, 1))
        self.surface.set_colorkey((1, 1, 1))

    def update(self, text):
        display_text(text, self.surface, self.x, self.y, self.alignment, self.size, colour=self.colour, bgColour=self.bgColour)
        return self.surface


def display_text(text, surface, x, y, alignment, size, **kwargs):
    bgColour = kwargs.get('bgColour', None)
    colour = kwargs.get('colour', None)
    black = (0, 0, 0)
    if not colour:
        colour = black
    font = pygame.font.SysFont("Courier New", size)
    '''
    8-bit fonts
    font = pygame.font.SysFont("Fixedsys", size)
    font = pygame.font.SysFont("System", size)
    '''
    if bgColour:
        textSurf = font.render(text, False, colour, bgColour)
    else:
        textSurf = font.render(text, False, colour)
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
