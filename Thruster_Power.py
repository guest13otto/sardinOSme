from Module_Base import Module
from pubsub import pub
import numpy as np

class Thruster_Power(Module):
    def __init__ (self, CG, ThrusterFL, ThrusterFR, ThrusterBL, ThrusterBR, ThrusterUF, ThrusterUB):
        self.CG = CG
        self.ThrusterFL = ThrusterFL
        self.ThrusterFR = ThrusterFR
        self.ThrusterBL = ThrusterBL
        self.ThrusterBR = ThrusterBR
        self.ThrusterUF = ThrusterUF
        self.ThrusterUB = ThrusterUB

        FLposition = tuple(map(float, self.ThrusterFL["Position"].split(',')))
        print(FLposition)

        pub.subscribe(self.command_movement, "command.movement")

    def command_movement(self, message):
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message

    def run(self):
        pass
