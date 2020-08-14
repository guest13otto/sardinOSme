import pygame


class Label:
    def __init__(self, x, y, alignment, colour, size):
        self.x = x
        self.y = y
        self.alignment = alignment
        self.colour = colour
        self.size = size
        self.font = pygame.font.SysFont("Courier New", size)

    def set_text(self, text, screen):
        textSurf = self.font.render(text, True, self.colour)
        textRect = textSurf.get_rect()
        if self.alignment == 'left':
            textRect.left = self.x
            textRect.centery = self.y
        elif self.alignment == 'right':
            textRect.right = self.x
            textRect.centery = self.y
        else:
            textRect.center = (self.x, self.y)
        screen.blit(textSurf, textRect)
