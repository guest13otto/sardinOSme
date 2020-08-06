from Module_Base import Module
from pubsub import pub
import numpy as np

class Thruster_Power(Module):
    def __init__ (self, CG, ThrusterFL, ThrusterFR, ThrusterBL, ThrusterBR, ThrusterUF, ThrusterUB):
        self.CG = np.array(tuple(map(float, CG.split(','))))
        self.ThrusterFL = ThrusterFL
        self.ThrusterFR = ThrusterFR
        self.ThrusterBL = ThrusterBL
        self.ThrusterBR = ThrusterBR
        self.ThrusterUF = ThrusterUF
        self.ThrusterUB = ThrusterUB
        self.ThrusterMatrix = np.zeros((6,1))

        Thrusters = (self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB)

        for Thruster in Thrusters:
            ThrusterPosition = np.array(tuple(map(float, Thruster["Position"].split(','))))
            ThrusterDirection = np.array(tuple(map(float, Thruster["Direction"].split(','))))
            ThrusterPosition = np.subtract(ThrusterPosition, self.CG)
            Torque = np.cross(ThrusterPosition, ThrusterDirection)
            ThrusterArray = np.concatenate((ThrusterDirection, Torque)).reshape(6,1)
            self.ThrusterMatrix = np.concatenate((self.ThrusterMatrix, ThrusterArray), axis = 1)
        print(self.ThrusterMatrix)



        pub.subscribe(self.command_movement, "command.movement")

    def command_movement(self, message):
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message

    def run(self):
        pass
