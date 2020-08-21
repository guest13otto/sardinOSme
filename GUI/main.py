import pygame
from Module_Base_Async import Module, AsyncModuleManager
from plot import Plot
#from Gamepad import Gamepad
from pubsub import pub
import random
import popup


class GUI(Module):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption("ControlGUI(UWU")
        screen = pygame.display.set_mode((400, 300))
        self.clock = pygame.time.Clock()
        self.plot = Plot(screen, 400, 300)
        self.movement = [0 for i in range(11)]
        self.thruster = [0 for i in range(6)]
        self.profile = -1
        #pub.subscribe(self.test_handler, 'test.send')
        pub.subscribe(self.movement_handler, 'gamepad.movement')
        #pub.subscribe(self.profile_handler, 'gamepad.profile')

        self.widgets = []
        self.widgets.append((popup.ProfilePopup(), (0, 0)))

    def run(self):
        self.clock.tick(30)
        self.plot.update(self.movement, self.profile)

        '''
        for widget in self.widgets:
            pygame.display.get_surface().blit(widget[0].update(), widget[1])
        '''

        pygame.display.flip()
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()

    def test_handler(self, movement, profile):
        self.movement = movement
        self.profile = profile

    def movement_handler(self, message):
        self.movement = message

    def thruster_handler(self, message):
        self.thruster = message

    def profile_handler(self, message):
        self.profile = message


class TestCaseSend(Module):
    def __init__(self):
        super().__init__()
        self.movement = 0
        self.profile = -1

    def run(self):
        self.movement = [random.uniform(-1.0, 1.0) for i in range(11)]
        pub.sendMessage('gamepad.movement', message=self.movement)
        print(self.movement)

    @Module.loop(0.25)
    def run2(self):
        self.profile = random.randint(0, 4)
        pub.sendMessage('gamepad.profile', message=self.profile)
        print(self.profile)


if __name__ == "__main__":
    test_case_send = TestCaseSend()
    gui = GUI()
    test_case_send.start(1)
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
