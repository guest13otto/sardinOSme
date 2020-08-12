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
Scale_Constants = (2.33, 2.33,  3.3, 2, 1.65, 0)# strafe, drive, yaw, updown, tiltFB, tiltLR
Backward_Thrust = 1.65


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

        Strafe *= Scale_Constants[0]
        Drive *= Scale_Constants[1]
        Yaw *= Scale_Constants[2]
        Updown *= Scale_Constants[3]
        TiltFB *= Scale_Constants[4]

        expectedResult = np.array((Strafe, Drive, Updown, TiltFB, TiltLR, Yaw)).reshape(6,1)

        ThrusterMatrixInv = np.linalg.pinv(self.ThrusterMatrix[0:6,1:7])
        finalList = ThrusterMatrixInv.dot(expectedResult)

        #pub.sendMessage("Thruster.RAW", message = finalList)

        for counter, Thruster in enumerate(self.Thrusters):
            if finalList[counter, 0] < 0:
                finalList[counter, 0] *= Backward_Thrust
            #finalList[counter,0] = finalList[counter,0] / Thruster["Scale"]
            if Thruster["Invert"] == True:
                finalList[counter, 0] *= -1

        print(finalList)

        #pub.sendMessage("Thruster.Power", message = finalList)



    def run(self):
        pass
class __Test_Case_Combo__(Module):
    def run(self):
        combined = [(x,y,tz,y,tx) for x in List[0] for y in List[1] for tz in List[2] for y in List[3] for tx in List[4]]
        for combo in combined:
            if (combo[0] + combo[1] == 1  or combo[0] + combo[1] == -1 or (combo[0] == 0 and combo[1] == 0)) and (combo[2] + combo[4] == -1 \
            or combo[2] + combo[4] == 1 or (combo[2] == 0 and combo[4] == 0)):
                message = (combo[0], combo[1], combo[2], combo[3], combo[4], 0)
                print(message)
                pub.sendMessage("command.movement", message = message)

        '''for counter, combo in enumerate(combinations(List, 6)):
            combo = (combo[0], combo[1], combo[2], 0, 0, 0)
            pub.sendMessage("command.movement", message = combo)'''

class __Test_Case_Scaled__(Module):
    def run(self):
        pub.sendMessage("command.movement", message = (1,1,0,0,0,0))
        '''pub.sendMessage("command.movement", message = (0,1,0,0,0,0))
        pub.sendMessage("command.movement", message = (0,0,1,0,0,0))
        pub.sendMessage("command.movement", message = (0,0,0,1,0,0))
        pub.sendMessage("command.movement", message = (0,0,0,0,1,0))
        pub.sendMessage("command.movement", message = (0,0,0,0,0,1))'''


if __name__ == "__main__":
    from itertools import combinations
    from Gamepad import Gamepad

    List = [(-1,0,1),(-1,0,1),(-1,0,1),(-1,0,1),(-1,0,1)]
    FL_List, FR_List, BL_List, BR_List, UF_List, UB_List = [],[],[],[],[],[]

    def Thruster_Power_Listener_Scaled(message):
        print("message: ", message.reshape(1,6))


    def Thruster_Power_Listener(message):
        FL, FR, BL, BR, UF, UB = message
        FL_List.append(FL)
        FR_List.append(FR)
        BL_List.append(BL)
        BR_List.append(BR)
        UF_List.append(UF)
        UB_List.append(UB)
        print(f"max FL: {max(FL_List)}, item: {len(FL_List)}")
        print(f"max FR: {max(FR_List)}")
        print(f"max BL: {max(BL_List)}")
        print(f"max BR: {max(BR_List)}")
        print(f"max UF: {max(UF_List)}")
        print(f"max UB: {max(UB_List)}")


    Gamepad = Gamepad()
    #Gamepad.start(100)

    Thruster_Power = Thruster_Power()
    test_case_combo = __Test_Case_Combo__()
    test_case_scaled = __Test_Case_Scaled__()
    test_case_scaled.start(1)
    #test_case_combo.start(1)

    #pub.subscribe(Thruster_Power_Listener, "Thruster.RAW")
    pub.subscribe(Thruster_Power_Listener_Scaled, "Thruster.Power")
