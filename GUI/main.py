import sys, os, inspect
import pygame
from plot import Plot
from pubsub import pub
import random
from popup import ProfilePopup, EMPopup

#import from parent directory
#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0, parentdir)
from Module_Base_Async import Module, AsyncModuleManager


class GUI(Module):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption("ControlGUI(UWU")
        self.screen_width = 400
        self.screen_height = 300
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.plot = Plot(self.screen, 400, 300)
        self.movement = [0 for i in range(6)]
        self.power = [0 for i in range(6)]
        self.profile = -1

        self.widgets = []
        self.widgets.append((ProfilePopup(self.screen_width, self.screen_height), (0, 0)))
        self.widgets.append((EMPopup(self.screen_width, self.screen_height, 1), (0, 0)))
        self.widgets.append((EMPopup(self.screen_width, self.screen_height, 2), (0, 0)))

        self.charts = []
        self.charts.append((Plot(['strafe', 'drive', 'yaw', 'ud', 'tilt', 'zero'], self.screen_width, self.screen_height), (0, 0), 0))
        self.charts.append((Plot(['FL', 'FR', 'BL', 'BR', 'TL', 'TR'], self.screen_width, self.screen_height), (self.screen_width/2, 0), 1))

    def run(self):
        #self.clock.tick(50)

        for chart in self.charts:
            pygame.display.get_surface().blit(chart[0].update(chart[2]), chart[1])

        for widget in self.widgets:
            pygame.display.get_surface().blit(widget[0].update(), widget[1])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def test_handler(self, movement, profile):
        self.movement = movement
        self.profile = profile

    def movement_handler(self, message):
        self.movement = message

    def power_handler(self, message):
        self.power = message

    def profile_handler(self, message):
        self.profile = message


class TestCaseSend(Module):
    def __init__(self):
        super().__init__()
        self.movement = 0
        self.profile = -1
        self.power = 0

    def run(self):
        self.movement = [random.uniform(-1.0, 1.0) for i in range(5)]
        self.movement.append(0.000)
        pub.sendMessage('gamepad.movement', message={"gamepad_message": self.movement})

    @Module.loop(0.003)
    def run2(self):
        pArr = ['A', 'B', 'C', 'D']
        self.profile = pArr[random.randint(0, 3)]
        pub.sendMessage('gamepad.profile', message={"Profile_Dict": self.profile})

    @Module.loop(1)
    def run3(self):
        self.power = [random.uniform(-1.0, 1.0) for i in range(6)]
        pub.sendMessage('Thruster.Power', message={"Thruster_message": [self.power]})

    @Module.loop(0.002)
    def run4(self):
        pub.sendMessage('gamepad.EM{}'.format(random.randint(1, 2)), message={"EM_L": random.randint(0, 1), "EM_R": random.randint(0, 1)})


if __name__ == "__main__":
    test_case_send = TestCaseSend()
    gui = GUI()
    test_case_send.start(50)
    gui.start(30)
    AsyncModuleManager.register_modules(gui, test_case_send)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
