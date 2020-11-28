import pygame
from Module_Base_Async import Module
from pubsub import pub


class Pygame_Joystick(Module):
        def __init__(self):
                super().__init__()
                pygame.init()
                pygame.joystick.init()
                pygame.joystick.Joystick(0).init()
                self.joystick = pygame.joystick.Joystick(0)
                print(self.joystick.get_name())
                self.move = [0, 0, 0, 0, 0, 0]

        @Module.loop(100)
        def run_(self):
                for event in pygame.event.get():
                         for i in range(self.joystick.get_numaxes()):
                                 self.move[0]= self.joystick.get_axis(0)
                         pub.sendMessage("gamepad.movement", message = {"gamepad_message": self.move})
