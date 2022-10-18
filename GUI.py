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
        #teal = (108, 194, 189)
        #blue = (90, 128, 158)
        #purple = (124, 121, 162)
        #coral = (245, 125, 124)
        #self.colours = [teal, blue, purple, coral]
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        ##colors
        self.screen_width = 2000
        self.screen_height = 1000
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pub.subscribe(self.movement_handler, "gamepad.movement")
        pub.subscribe(self.quitter, "quit")
        
    def quitter(self, message):
        if message == 1:
            pygame.quit()
        else: 
            pass
        
    @Async_Task.loop(1)
    async def run(self):
        self.clock.tick(30)
        self.screen.fill((91, 143, 227))
        pygame.draw.circle(self.screen, (255, 255, 255), (500+(50*self.movement[0]), 500+(50*self.movement[1])), 50, 0)
        pygame.display.flip()
    def movement_handler(self, message):
        self.movement = message["gamepad_message"]




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
