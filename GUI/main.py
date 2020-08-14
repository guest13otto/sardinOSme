import pygame
from Module_Base_Async import Module, AsyncModuleManager
from plot import Plot
#from Gamepad import Gamepad
from pubsub import pub
import random


class GUI(Module):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ControlGUI(UWU")
        screen = pygame.display.set_mode((400, 300))
        self.clock = pygame.time.Clock()
        self.plot = Plot(screen, 400, 300)
        self.arr = [0 for i in range(9)]
        self.profile = -1
        pub.subscribe(self.handler, 'test.send')
        super().__init__()

    #@Module.loop(1)
    def run(self):
        self.clock.tick(30)
        self.plot.update(self.arr, self.profile)
        pygame.display.flip()
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()

    def handler(self, arr, profile):
        self.arr = arr
        self.profile = profile


class TestCaseSend(Module):
    def __init__(self):
        self.testcase = 0
        self.profile = -1
        super().__init__()

    #@Module.loop(1)
    def run(self):
        self.testcase = [random.uniform(-1.0, 1.0) for i in range(9)]
        print(self.testcase)

    @Module.loop(0.25)
    def run2(self):
        self.profile = random.randint(0, 4)
        print(self.profile)

    @Module.loop(1)
    def run_send(self):
        pub.sendMessage('test.send', arr=self.testcase, profile=self.profile)


if __name__ == "__main__":
    test_case_send = TestCaseSend()
    gui = GUI()
    test_case_send.start(1)
    gui.start(1)
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
