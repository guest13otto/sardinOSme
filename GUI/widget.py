import pygame


class Widget:
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((400, 300))
        self.profile = -1
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.labels = ['profile ' + str(i) for i in range(4)]
        self.font = pygame.font.SysFont("Courier New", 14)

    def update(self, profile):
        if profile != self.profile:
            self.profile = profile
            self.surface.fill(self.colours[profile])
            textSurf = self.font.render(self.labels[profile], True, self.colours[profile])
            textRect = textSurf.get_rect()
            textRect.center = (200, 150)
            self.surface.blit(textSurf, textRect)
            return self.surface
