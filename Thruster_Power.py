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
import yaml


class Thruster_Power(Module):
    def __init__ (self):
        try:
            content = yaml.load(open('Thruster.yaml', 'r'), Loader = yaml.FullLoader)
            for key,value in content.items():
                exec(f"self.{key} = value")
        except FileNotFoundError:
            pass

        self.CG = np.array(tuple(map(float, self.CG.split(','))))
        self.ThrusterMatrix = np.zeros((6,1))
        self.Thrusters = (self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB)

        for Thruster in self.Thrusters: # 6x6 Matrix
            ThrusterPosition = np.array(tuple(map(float, Thruster["Position"].split(','))))
            ThrusterDirection = np.array(tuple(map(float, Thruster["Direction"].split(','))))
            ThrusterPosition = np.subtract(ThrusterPosition, self.CG)
            Torque = np.cross(ThrusterPosition, ThrusterDirection)
            ThrusterArray = np.concatenate((ThrusterDirection, Torque)).reshape(6,1)
            self.ThrusterMatrix = np.concatenate((self.ThrusterMatrix, ThrusterArray), axis = 1)

        pub.subscribe(self.command_movement, "command.movement")

    def command_movement(self, message):
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message
        expectedResult = np.array((Strafe, Drive, Updown, TiltFB, TiltLR, Yaw)).reshape(6,1)

        ThrusterMatrixInv = np.linalg.pinv(self.ThrusterMatrix[0:6,1:7])
        finalList = ThrusterMatrixInv.dot(expectedResult)
        #print(self.ThrusterMatrix)

        for counter, Thruster in enumerate(self.Thrusters):
            if Thruster["Invert"] == True:
                finalList[counter, 0] *= -1

        pub.sendMessage("Thruster.Power", message = finalList)



    def run(self):
        pass
class __Test_Case_Send__(Module):
    def run(self):
        pub.sendMessage("command.movement", message = (0,0,0,0,1,0))

if __name__ == "__main__":
    from Gamepad import Gamepad
    def Thruster_Power_Listener(message):

        print(message.reshape(1,6))

    Gamepad = Gamepad()
    Gamepad.start(100)

    Thruster_Power = Thruster_Power()
    Thruster_Power.start(100)

    test_case_send = __Test_Case_Send__()
    test_case_send.start(1)

    pub.subscribe(Thruster_Power_Listener, "Thruster.Power")
