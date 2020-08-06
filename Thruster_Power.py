'''
Subcribe Topics:

command.movement
    vector6: Strafe, Drive, Yaw, UpDown, TiltFB, TiltLR

Publish Topics

Thruster.Power
    vector6: Strafe, Drive, UpDown, TiltFB, TiltLR, Yaw
'''

from Module_Base import Module
from pubsub import pub
import numpy as np


class Thruster_Power(Module):
    def __init__ (self, CG, ThrusterFL, ThrusterFR, ThrusterBL, ThrusterBR, ThrusterUF, ThrusterUB):


        CG = np.array(tuple(map(float, CG.split(','))))
        self.ThrusterMatrix = np.zeros((6,1))
        self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB = ThrusterFL, ThrusterFR, ThrusterBL, ThrusterBR, ThrusterUF, ThrusterUB
        self.Thrusters = (ThrusterFL, ThrusterFR, ThrusterBL, ThrusterBR, ThrusterUF, ThrusterUB)

        for Thruster in self.Thrusters: # 6x6 Matrix
            ThrusterPosition = np.array(tuple(map(float, Thruster["Position"].split(','))))
            ThrusterDirection = np.array(tuple(map(float, Thruster["Direction"].split(','))))
            ThrusterPosition = np.subtract(ThrusterPosition, CG)
            Torque = np.cross(ThrusterPosition, ThrusterDirection)
            ThrusterArray = np.concatenate((ThrusterDirection, Torque)).reshape(6,1)
            self.ThrusterMatrix = np.concatenate((self.ThrusterMatrix, ThrusterArray), axis = 1)
        print(self.ThrusterMatrix[0:6, 1:7])

        pub.subscribe(self.command_movement, "command.movement")

    def command_movement(self, message):
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message
        expectedResult = np.array((Strafe, Drive, Updown, TiltFB, TiltLR, Yaw)).reshape(6,1)

        ThrusterMatrixInv = np.linalg.pinv(self.ThrusterMatrix[0:6,1:7])
        finalList = ThrusterMatrixInv.dot(expectedResult)
        print(finalList)

        for counter, Thruster in enumerate(self.Thrusters):
            if Thruster["Invert"] == True:
                finalList[counter, 0] *= -1



    def run(self):
        pass
