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

#Scale constants
Scale_Constants = [1,1,1,1,1]
Print = False


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
        self.counter = 0

        for Thruster in self.Thrusters: # 6x6 Matrix
            ThrusterPosition = np.array(tuple(map(float, Thruster["Position"].split(','))))
            ThrusterDirection = np.array(tuple(map(float, Thruster["Direction"].split(','))))
            ThrusterPosition = np.subtract(ThrusterPosition, self.CG)
            Torque = np.cross(ThrusterPosition, ThrusterDirection)
            ThrusterArray = np.concatenate((ThrusterDirection, Torque)).reshape(6,1)
            self.ThrusterMatrix = np.concatenate((self.ThrusterMatrix, ThrusterArray), axis = 1)

        for i in range(5):
            message = [0] * 6
            message[i] = -1
            self.gamepadScaleConstant(message)
        #self.gamepadScaleConstant(message = [0,0,0,1,0,0])

        pub.subscribe(self.command_movement, "command.movement")

    def truncate(self, finalList):
        if max(abs(finalList)) > 1:
            for counter, Thruster in enumerate(self.Thrusters):
                finalList[counter, 0] /= max(abs(finalList))
        return finalList

    def directionScale(self, finalList):
        for counter, Thruster in enumerate(self.Thrusters):
            if finalList[counter, 0] < 0:
                finalList[counter, 0] *= Thruster["NegativeScale"]
            else:
                finalList[counter, 0] *= Thruster["PositiveScale"]
            #finalList[counter,0] /= Thruster["Scale"] # uncomment for cmbinational movement
            if Thruster["Invert"] == True:
                finalList[counter, 0] *= -1
        if Print:
            print("direction scale out: ", finalList.reshape(1,6))
        return finalList

    def invert(self, finalList):
        for counter, Thruster in enumerate(self.Thrusters):
            if Thruster["Invert"] == True:
                finalList[counter, 0] *= -1
        if Print:
            print("invert out: ", finalList.reshape(1,6))
        return finalList

    def overallScale(self, finalList):
        for counter, Thruster in enumerate(self.Thruster):
            finalList[counter, 0] /= Thruster["Scale"]

    def pseudoInv(self, expectedResult):
        ThrusterMatrixInv = np.linalg.pinv(self.ThrusterMatrix[0:6,1:7])
        finalList = ThrusterMatrixInv.dot(expectedResult)
        if Print:
            print('pinv out: ', finalList.reshape(1,6))
        return finalList

    def gamepadScale(self, message):
        gamepadScaled = list(message)
        for counter, dof in enumerate(gamepadScaled):
            if counter != 5:
                gamepadScaled[counter] *= Scale_Constants[counter]
        if Print:
            print('gamepadScaled out :', gamepadScaled)
        return gamepadScaled

    def gamepadScaleConstant(self, message):
        print(message)
        if Print:
            print("Test case: ", message)
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message
        expectedResult = np.array((Strafe, Drive, Updown, TiltFB, TiltLR, Yaw)).reshape(6,1)
        finalList = self.pseudoInv(expectedResult)
        finalList = self.directionScale(finalList)
        for counter, dof in enumerate(message):
            if dof != 0:
                Scale_Constants[counter] = float(1/max(abs(finalList)))
        print(Scale_Constants)

    def command_movement(self, message):
        if Print:
            print("Test Case: ", message)

        message = self.gamepadScale(message)
        Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message
        expectedResult = np.array((Strafe, Drive, Updown, TiltFB, TiltLR, Yaw)).reshape(6,1)
        finalList = self.pseudoInv(expectedResult)
        finalList = self.directionScale(finalList)
        finalList = self.invert(finalList)
        #finalList = self.truncate(finalList)

        pub.sendMessage("Thruster.Power", message = finalList)

    def run(self):
        pass

class __Test_Case_Combo__(Module):
    def __init__(self):
        pub.subscribe(self.Thruster_Power_Listener_Max, "Thruster.Power")
        self.List = [(-1,0,1),(-1,0,1),(-1,0,1),(-1,0,1),(-1,0,1)]
        self.FL_List, self.FR_List, self.BL_List, self.BR_List, self.UF_List, self.UB_List = [],[],[],[],[],[]

    def Thruster_Power_Listener_Max(self, message):
        FL, FR, BL, BR, UF, UB = message
        self.FL_List.append(FL), self.FR_List.append(FR), self.BL_List.append(BL), self.BR_List.append(BR), self.UF_List.append(UF), self.UB_List.append(UB)
        print(f"max FL: {float(max(np.abs(self.FL_List)))}, combo: {self.message}, item: {len(self.FL_List)}")
        print(f"max FR: {float(max(np.abs(self.FR_List)))}")
        print(f"max BL: {float(max(np.abs(self.BL_List)))}")
        print(f"max BR: {float(max(np.abs(self.BR_List)))}")
        print(f"max UF: {float(max(np.abs(self.UF_List)))}")
        print(f"max UB: {float(max(np.abs(self.UB_List)))}")

    def run(self):
        combined = ((x,y,tz,y,tx) for x in self.List[0] for y in self.List[1] for tz in self.List[2] for y in self.List[3] for tx in self.List[4])
        for combo in combined:
            '''if (combo[0] + combo[1] == 1  or combo[0] + combo[1] == -1 or (combo[0] == 0 and combo[1] == 0)) and (combo[2] + combo[4] == -1 \
            or combo[2] + combo[4] == 1 or (combo[2] == 0 and combo[4] == 0)):'''
            self.message = (combo[0], combo[1], combo[2], combo[3], combo[4], 0)
            pub.sendMessage("command.movement", message = self.message)
        self.stop()

class __Test_Case_Single__(Module):
    def __init__(self):
        pub.subscribe(self.Thruster_Power_Listener_Single, "Thruster.Power")

    def Thruster_Power_Listener_Single(self, message):
        #print(f"Scale Constants: {Scale_Constants}")
        print("message: ", message.reshape(1,6))

    def run(self):
        pub.sendMessage("command.movement", message = (0,0,0,1,0,0))
        self.stop()


if __name__ == "__main__":
    Print = False
    from itertools import combinations
    from Gamepad import Gamepad

    Gamepad = Gamepad()
    #Gamepad.start(1)

    Thruster_Power = Thruster_Power()
    #__Test_Case_Combo__ = __Test_Case_Combo__()
    __Test_Case_Single__ = __Test_Case_Single__()
    __Test_Case_Single__.start(1)
    #__Test_Case_Combo__.start(1)
