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
Normalize_Constant_Z = 256 #1024 white controller ; 256 black controller
Directional_BTN = {"BTN_NORTH", "BTN_WEST", "BTN_SOUTH", "BTN_EAST"}
#BTN_TL, BTN_TR {0, 1}

ProfileDict = {'BTN_THUMB0': 'A',
               'BTN_THUMB1': 'B',
               'BTN_THUMB2': 'C',
               'BTN_THUMB3': 'D'}

# variables
from inputs import get_gamepad
from pubsub import pub
from Module_Base import Module


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

    def run(self):
        #global previous_message
        #global movement_message
        events= get_gamepad()
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

                self.updown = half_movement_value_join(self.updown1, self.updown2)


                if self.control_invert == False:#tfront, tback
                    self.movement_message = (self.strafe, self.drive, self.yaw, self.updown, self.tilt, 0)
                else:
                    self.movement_message = (-self.strafe, -self.drive, self.yaw,  self.updown, -self.tilt, 0)
                #pub_to_manager('movement', message = self.movement_message)
                pub.sendMessage("gamepad.movement", message = self.movement_message)

        hatcode = event.code[0:8]
        controlcode = event.code
        if controlcode[:9] == "BTN_THUMB" and event.state!=0:
            if controlcode[-1] == "R":
                self.thumb_profile_cycle = (self.thumb_profile_cycle+1)%4
            else:
                self.thumb_profile_cycle = (self.thumb_profile_cycle-1)%4
            pub.sendMessage("gamepad.profile", message = ProfileDict[str(event.code[:-1])+str(self.thumb_profile_cycle)])

        if controlcode == 'BTN_TL' and event.state != 0:
            pass #EM

        if controlcode == 'BTN_TR' and event.state != 0:
            pass #EM

        if (controlcode == "BTN_SOUTH") and (event.state == 1):
            pass
            pub.sendMessage("movement_activation", sender = "transectline")
            pub.sendMessage("show_transectline", message = not self.show_transectline)

        if (controlcode == "BTN_WEST") and (event.state == 1):
            self.control_invert = not self.control_invert
            pub.sendMessage("gamepad.invert", message = self.control_invert) #For GUI


if __name__ == "__main__":
    import time
    def debug_listener_movement(message):
        print("movement", message)

    def debug_listener_profile(message):
        print("\t\t\t\t\t", "profile", message,"\n")
        time.sleep(1)

    debug = Gamepad()
    debug.start(120)
    pub.subscribe(debug_listener_movement, 'gamepad.movement')
    pub.subscribe(debug_listener_profile, 'gamepad.profile')
