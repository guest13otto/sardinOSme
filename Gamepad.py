'''
Gamepad Module

Subscribe Topics: None

Publish Topics:

gamepad.movement
    message: Vector6

gamepad.profile
    message: String

gamepad.invert
    message: Boolean

'''


# constants
DeadZone_ThresholdL = 0.11
DeadZone_ThresholdR = 0.1
Normalize_Constant = 32768
Normalize_Constant_Z = 1024 #1024 white controller ; 256 black controller
Directional_BTN = {"BTN_NORTH", "BTN_WEST", "BTN_SOUTH", "BTN_EAST"}
#BTN_TL, BTN_TR {0, 1}

ProfileDict = {'BTN_THUMB0': 'A',
               'BTN_THUMB1': 'B',
               'BTN_THUMB2': 'C',
               'BTN_THUMB3': 'D'}

# variables
from inputs import get_gamepad
from pubsub import pub
from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
import asyncio


def normalize(X, constant = Normalize_Constant):
    if X < 0:
        return (X/constant)
    else:
        return (X/(constant-1))

def deadzoneleft(X):
    if X <(DeadZone_ThresholdL) and X > (-DeadZone_ThresholdL):
        return 0
    else:
        return X
def deadzoneright(X):
    if X <(DeadZone_ThresholdR) and X > (-DeadZone_ThresholdR):
        return 0
    else:
        return X

def half_movement_value_join(negative_value, positive_value):
    return negative_value+positive_value

def half_movement_value_split(full_value):
    if full_value>=0:
        return 0, full_value
    else:
        return full_value, 0


class Gamepad(Module):
    def __init__(self):
        super().__init__()
        #pub.subscribe(self.south_listener, 'transectline')
        self.drive = 0
        self.strafe = 0
        self.yaw = 0
        self.tilt = 0
        self.updown1 = 0
        self.updown2 = 0
        self.updown = 0
        self.tilt_front = 0
        self.tilt_back = 0
        self.control_invert = False
        self.movement_message = (0,0,0,0,0,0)
        self.active = True #[True, False, False]  #Analog, South, West
        self.show_transectline = False
        self.thumb_profile_cycle = 0
        self.EM1_L = 0
        self.EM1_R = 0
        self.EM2_L = 0
        self.EM2_R = 0
        self.light = 0

    @Module.asyncloop(1)
    async def run2(self):
        pub.sendMessage("gamepad.movement", message = {"gamepad_message": self.movement_message})

    @Module.asyncloop(10)
    async def run3(self):
        loop = asyncio.get_running_loop()
        events = await loop.run_in_executor(None, get_gamepad)
        analogcode = None
        for event in events:
            if self.active:
                analogcode = event.code[0:6]
                if (analogcode == "ABS_X"):
                    self.strafe = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_Y"):
                    self.drive = deadzoneleft(normalize(event.state))
                elif (analogcode == "ABS_RX"):
                    self.yaw = deadzoneright(normalize(event.state))
                elif (analogcode == "ABS_RY"):
                    self.tilt = (deadzoneright(normalize(event.state)))
                    #print(self.tilt)
                if (analogcode == "ABS_Z"):
                    self.updown1 =  (-1)*normalize(event.state, Normalize_Constant_Z)
                if (analogcode == "ABS_RZ"):
                    self.updown2 = normalize(event.state, Normalize_Constant_Z)
                #if (analogcode[:4] == "ABS_" and analogcode[-1] == "Z"):
                self.updown = half_movement_value_join(self.updown1, self.updown2)
                #print(self.strafe, self.drive, self.tilt, self.yaw, self.updown)

                if self.control_invert == False:#tfront, tback
                    self.movement_message = (-self.strafe, self.drive, self.yaw, self.updown, -self.tilt, 0)
                else:
                    self.movement_message = (self.strafe, -self.drive, self.yaw,  self.updown, self.tilt, 0)

                #pub.sendMessage("gamepad.movement", message = {"gamepad_message": self.movement_message})

                hatcode = event.code[0:8]
                controlcode = event.code
                if controlcode[:9] == "BTN_THUMB" and event.state!=0:
                    if controlcode[-1] == "R":
                        self.thumb_profile_cycle = (self.thumb_profile_cycle+1)%4
                    else:
                        self.thumb_profile_cycle = (self.thumb_profile_cycle-1)%4
                    pub.sendMessage("gamepad.profile", message = {"Profile_Dict": ProfileDict[str(event.code[:-1])+str(self.thumb_profile_cycle)]})

                if controlcode == 'BTN_TL' and event.state != 0:
                    self.EM1_L += event.state
                    pub.sendMessage("gamepad.EM1", message = {"EM_L": self.EM1_L%2, "EM_R": self.EM1_R%2})

                if controlcode == 'BTN_TR' and event.state != 0:
                    self.EM1_R += event.state
                    pub.sendMessage("gamepad.EM1", message = {"EM_L": self.EM1_L%2, "EM_R": self.EM1_R%2})

                if controlcode == 'ABS_HAT0X':
                    if event.state == -1:
                        self.EM2_L += 1
                        pub.sendMessage("gamepad.EM2", message = {"EM_L": self.EM2_L%2, "EM_R": self.EM2_R%2})
                    if event.state == 1:
                        self.EM2_R += 1
                        pub.sendMessage("gamepad.EM2", message = {"EM_L": self.EM2_L%2, "EM_R": self.EM2_R%2})

                if (controlcode == "BTN_SOUTH") and (event.state == 1):
                    pass
                    '''pub.sendMessage("gamepad.movement_activation", message = {"activate": "transectline"})
                    pub.sendMessage("gamepad.show_transectline", message = {"show": not self.show_transectline})'''
                if (controlcode == 'BTN_NORTH') and (event.state == 1):
                    self.light = not self.light
                    pub.sendMessage("gamepad.light", message = {"light": self.light})

                if (controlcode == "BTN_WEST") and (event.state == 1):
                    self.control_invert = not self.control_invert
                    pub.sendMessage("gamepad.invert", message = {"invert": self.control_invert}) #For GUI



if __name__ == "__main__":
    import time
    def debug_listener_movement(message):
        print(message["gamepad_message"])

    def debug_listener_profile(message):
        print("\t\t\t\t\t", message["Profile_Dict"])
        #time.sleep(1)
    def debug_listener_EM1(message):
        print("EM1: ", message)
    def debug_listener_EM2(message):
        print("EM2: ", message)

    debug = Gamepad()
    debug.start(120)
    pub.subscribe(debug_listener_movement, 'gamepad.movement')
    pub.subscribe(debug_listener_profile, 'gamepad.profile')
    pub.subscribe(debug_listener_EM1, 'gamepad.EM1')
    pub.subscribe(debug_listener_EM2, 'gamepad.EM2')
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(debug)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
