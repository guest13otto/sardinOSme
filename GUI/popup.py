import pygame
from pubsub import pub
from label import Label
import time


class ProfilePopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((400, 300))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.profile = -1
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.pArr = ['A', 'B', 'C', 'D']
        self.labels = ['profile ' + self.pArr[i] for i in range(4)]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.profile_handler, "gamepad.profile")
        self.expired = time.time()

    def profile_handler(self, message):
        self.set_profile(message["Profile_Dict"])

    def set_profile(self, profile):
        for i in range(len(self.pArr)):
            if profile == self.pArr[i]:
                profile = i
        if profile != self.profile:
            self.expired = time.time() + 1
        self.profile = profile

    def update(self):
        if self.expired > time.time():
            self.surface.fill((1, 1, 1))
            profSurf = pygame.Surface((self.x, self.y))
            profSurf.fill(self.colours[self.profile])

            textSurf = self.font.render(self.labels[self.profile], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (self.x/2, self.y/2)
            profSurf.blit(textSurf, textRect)
            self.surface.blit(profSurf, (self.screen_width-self.x, 0))
        else:
            self.surface.fill((1, 1, 1))
            label = Label(self.screen_width, self.screen_height, (0, 1), 14, bgColour=self.colours[self.profile])
            self.surface.blit(label.update(self.labels[self.profile]), (0, 0))
        return self.surface


class EM1Popup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((400, 300))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.emL = -1
        self.emR = -1
        self.labels = ['OFF', 'ON']
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.em1_handler, "gamepad.EM1")
        self.expired = time.time()

    def em1_handler(self, message):
        self.set_em1(message["EM_L"], message["EM_R"])

    def set_em1(self, emL, emR):
        if emL != self.emL or emR != self.emR:
            self.emL = emL
            self.emR = emR
            self.expired = time.time() + 1

    def update(self):
        purple = (124, 121, 162)
        if self.expired > time.time():
            self.surface.fill((1, 1, 1))
            em1Surf = pygame.Surface((self.x, self.y))
            em1Surf.fill(purple)

            textSurfL = self.font.render('EM_L: ' + self.labels[self.emL], True, (0, 0, 0))
            textRectL = textSurfL.get_rect()
            textRectL.center = (self.x / 2, self.y / 2 - 10)

            textSurfR = self.font.render('EM_L: ' + self.labels[self.emL], True, (0, 0, 0))
            textRectR = textSurfR.get_rect()
            textRectR.center = (self.x / 2, self.y / 2 + 10)

            em1Surf.blit(textSurfL, textRectL)
            em1Surf.blit(textSurfR, textRectR)
            self.surface.blit(em1Surf, (self.screen_width-self.x, self.screen_height-self.y))
        else:
            self.surface.fill((1, 1, 1))
            label = Label(self.screen_width, self.screen_height, (1, 1), 14, bgColour=purple)
            text = 'EM_L: ' + self.labels[self.emL] + ' EM_R: ' + self.labels[self.emR]
            self.surface.blit(label.update(text), (0, 0))
        return self.surface
