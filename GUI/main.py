import pygame
from Module_Base import Module
from plot import Plot
#from Gamepad import Gamepad
from pubsub import pub
import random


class GUI(Module):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ControlGUI(UWU")
        screen = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.plot = Plot(screen, 1080, 720)

    def run(self):
        '''
        strafe = (cv2.getTrackbarPos('strafe', 'Track Bars') - 50) / 50
        drive = (cv2.getTrackbarPos('drive', 'Track Bars') - 50) / 50
        yaw = (cv2.getTrackbarPos('yaw', 'Track Bars') - 50) / 50
        tilt = (cv2.getTrackbarPos('tilt', 'Track Bars') - 50) / 50
        updown1 = (cv2.getTrackbarPos('updown1', 'Track Bars') - 50) / 50
        updown2 = (cv2.getTrackbarPos('updown2', 'Track Bars') - 50) / 50
        '''
        self.clock.tick(30)
        arr = [random.uniform(-1.0, 1.0) for i in range(6)]
        #self.plot.update((random.uniform(-1.0, 1.0), 0.1, 0.2, -1, 0.1, 0.2))
        self.plot.update(arr)
        pygame.display.flip()
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()


class TestCaseSend(Module):
    def run(self):
        testcase = [random.uniform(-1.0, 1.0) for i in range(6)]
        print(testcase)
        pub.sendMessage('test.send', message=testcase)


if __name__ == "__main__":
    gui = GUI()
    gui.start(10)

    #test_case_send = TestCaseSend()
    #test_case_send.start(0.1)

    #pub.subscribe(main(), 'test.send')


