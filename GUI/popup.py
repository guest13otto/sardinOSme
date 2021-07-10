import pygame
from pubsub import pub
from label import Label
import time


class ProfilePopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.profile = 0
        #teal = (108, 194, 189)
        #blue = (90, 128, 158)
        #purple = (124, 121, 162)
        #coral = (245, 125, 124)
        #self.colours = [teal, blue, purple, coral]
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        self.colours = [green, yellow, red, blue]
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
        self.surface.fill((1, 1, 1))
        if self.expired > time.time():
            profSurf = pygame.Surface((self.x, self.y))
            profSurf.fill(self.colours[self.profile])

            textSurf = self.font.render(self.labels[self.profile], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (self.x/2, self.y/2)
            profSurf.blit(textSurf, textRect)
            self.surface.blit(profSurf, (self.screen_width-self.x, 0))
        else:
            label = Label(self.screen_width, self.screen_height, (0, 1), 14, bgColour=self.colours[self.profile])
            self.surface.blit(label.update(self.labels[self.profile]), (0, 0))
        return self.surface


class InvertPopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.invert = 0
        red = (255, 0, 0)
        #green = (0, 255, 0)
        blue = (0, 0, 255)
        #self.colours = [green, red]
        self.colours = [blue, red]
        self.iArr = ['OFF', 'ON']
        self.labels = ['Invert: ' + self.iArr[i] for i in range(2)]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.invert_handler, "gamepad.invert")
        self.expired = time.time()

    def invert_handler(self, message):
        self.set_invert(message["invert"])

    def set_invert(self, invert):
        if bool(self.invert) != invert:
            self.expired = time.time() + 1
        if invert:
            self.invert = 1
        else:
            self.invert = 0

    def update(self):
        self.surface.fill((1, 1, 1))
        if self.expired > time.time():
            invertSurf = pygame.Surface((self.x, self.y))
            invertSurf.fill(self.colours[self.invert])

            textSurf = self.font.render(self.labels[self.invert], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (self.x / 2, self.y / 2)
            invertSurf.blit(textSurf, textRect)
            self.surface.blit(invertSurf, (0, 0))
        else:
            label = Label(self.screen_width, self.screen_height, (0, 0), 14, bgColour=self.colours[self.invert])
            self.surface.blit(label.update(self.labels[self.invert]), (0, 0))
        return self.surface


class ToolsPopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.tool = -1
        self.emStates = [[False, False], [False, False]]
        self.labels = ['Gripper', 'EM1', 'EM2', 'Erector']
        self.emLabels = ['OFF', 'ON']
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.toolColours = [teal, blue, purple, coral]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.tool_handler, "gamepad.selected_tool")
        pub.subscribe(self.em_handler, "gamepad.em_states")
        self.expired = time.time()

    def tool_handler(self, message):
        self.tool = message["tool_index"]
        self.expired = time.time() + 1

    def em_handler(self, message):
        lr = ['L', 'R']
        for i in range(2):
            for j in range(2):
                self.emStates[i][j] = message["gamepad.EM{}{}".format(i+1, lr[j])]

    def update(self):
        self.surface.fill((1, 1, 1))
        if self.tool >= 0:
            if self.expired > time.time():
                self.surface.fill((1, 1, 1))
                toolSurf = pygame.Surface((self.x, self.y))
                toolSurf.fill(self.toolColours[self.tool])

                textSurf = self.font.render(self.labels[self.tool], True, (0, 0, 0))
                textRect = textSurf.get_rect()
                textRect.center = (self.x / 2, self.y / 2)
                toolSurf.blit(textSurf, textRect)
                self.surface.blit(toolSurf, (self.screen_width-self.x, self.screen_height-self.y))
            else:
                self.surface.fill((1, 1, 1))
                label = Label(self.screen_width, self.screen_height, (1, 1), 14, bgColour=self.toolColours[self.tool])
                self.surface.blit(label.update(self.labels[self.tool]), (0, 0))
        emLabel = Label(self.screen_width, self.screen_height, (1, 0), 14, bgColour=self.toolColours[2])
        emTexts = ['', '']
        for i in range(2):
            emTexts[i] = 'EM{} L:{} R:{}'.format(i+1, self.emLabels[int(self.emStates[i][0])], self.emLabels[int(self.emStates[i][1])])
        emText = '  '.join(emTexts)
        self.surface.blit(emLabel.update(emText), (1, 0))
        return self.surface
