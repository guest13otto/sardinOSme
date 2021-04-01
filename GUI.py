import sys
import pygame
from pubsub import pub
import random
from Module_Base import Module, Async_Task, ModuleManager
sys.path.insert(1, './GUI')
from plot import Plot
from popup import *


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
        self.widgets.append((InvertPopup(self.screen_width, self.screen_height), (0, 0)))
        self.widgets.append((ToolsPopup(self.screen_width, self.screen_height), (0, 0)))

        self.charts = []
        self.charts.append((Plot(['strafe', 'drive', 'yaw', 'ud', 'tilt', 'zero'], self.screen_width, self.screen_height), (0, 0), 0))
        self.charts.append((Plot(['FL', 'FR', 'BL', 'BR', 'TL', 'TR'], self.screen_width, self.screen_height), (self.screen_width/2, 0), 1))

    @Async_Task.loop(1)
    async def run(self):
        self.clock.tick(30)

        for chart in self.charts:
            pygame.display.get_surface().blit(chart[0].update(chart[2]), chart[1])

        for widget in self.widgets:
            pygame.display.get_surface().blit(widget[0].update(), widget[1])

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


class TestCaseSend(Module):
    def __init__(self):
        super().__init__()
        self.movement = 0
        self.profile = -1
        self.power = 0
        self.invert = False

    @Async_Task.loop(1)
    async def run(self):
        self.movement = [random.uniform(-1.0, 1.0) for i in range(5)]
        self.movement.append(0.000)
        pub.sendMessage("gamepad.movement", message={"gamepad_message": self.movement})

    @Async_Task.loop(0.003)
    async def run2(self):
        pArr = ['A', 'B', 'C', 'D']
        self.profile = pArr[random.randint(0, 3)]
        pub.sendMessage("gamepad.profile", message={"Profile_Dict": self.profile})

    @Async_Task.loop(1)
    async def run3(self):
        self.power = [random.uniform(-1.0, 1.0) for i in range(6)]
        pub.sendMessage("Thruster.Power", message={"Thruster_message": [self.power]})

    @Async_Task.loop(0.02)
    async def run4(self):
        pub.sendMessage("gamepad.selected_tool", message={"tool_index": random.randint(0, 3)})

    @Async_Task.loop(0.002)
    async def run5(self):
        flip = random.randint(0, 1)
        if flip:
            self.invert = not self.invert
        pub.sendMessage("gamepad.invert", message={"invert": self.invert})

    @Async_Task.loop(0.02)
    async def run6(self):
        pub.sendMessage("gamepad.em_states", message={"gamepad.EM1L": bool(random.randint(0, 1)), "gamepad.EM1R": bool(random.randint(0, 1)), "gamepad.EM2L": bool(random.randint(0, 1)), "gamepad.EM2R": bool(random.randint(0, 1))})


if __name__ == "__main__":
    test_case_send = TestCaseSend()
    gui = GUI()
    test_case_send.start(50)
    gui.start(30)
    mm = ModuleManager("")
    mm.start(1)
    mm.register_all()
    mm.start_all()

    try:
        mm.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
