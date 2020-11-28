from pubsub import pub
from Module_Base_Async import Module
import pygame

# constants
DEADZONE_THRESHOLD_L = 0.1
DEADZONE_THRESHOLD_R = 0.1
DEADZONE_THRESHOLD_Z = 0.1
ProfileDict = {0: 'A',
               1: 'B',
               2: 'C',
               3: 'D'}
LogicDict = {0 : False,
             1 : True}


def deadzoneleft(X):
    if X <(DEADZONE_THRESHOLD_L) and X > (-DEADZONE_THRESHOLD_L):
        return 0
    else:
        return X
def deadzoneright(X):
    if X <(DEADZONE_THRESHOLD_R) and X > (-DEADZONE_THRESHOLD_R):
        return 0
    else:
        return X

def deadzone_back(value):
    if value <(DEADZONE_THRESHOLD_Z) and value > (-DEADZONE_THRESHOLD_Z):
        return 0
    else:
        return value

def hat_mapping(hat_tuple):
    west = 0
    east = 0
    north = 0
    south = 0
    if hat_tuple[0]==1:
        east = 1
    if hat_tuple[0]==-1:
        west = 1
    if hat_tuple[1]==1:
        north = 1
    if hat_tuple[1]==-1:
        south = 1
    return west, east, north, south
        
def set_value(var, value):
    if value != None:
        var = value
        
def button_pressed(button_record):
    if button_record[0]!=button_record[1] and button_record[1]==1:
        button_record[0] = button_record[1]
        return True
    button_record[0] = button_record[1]
    return False

class Joystick(Module):
    def __init__(self):
        pygame.init()
        if pygame.display.get_init()==1:
            pygame.display.init()
            pygame.display.set_mode((200, 1))
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except:
            raise TypeError("No joystick connected")
        self.joystick.init()
        """
        self.a_input = get_button_once(self.joystick.get_button, 0)
        self.b_input = get_button_once(self.joystick.get_button, 1)
        self.x_input = get_button_once(self.joystick.get_button, 2)
        self.y_input = get_button_once(self.joystick.get_button, 3)
        self.lb_input = get_button_once(self.joystick.get_button, 4)
        self.rb_input = get_button_once(self.joystick.get_button, 5)
        self.back_input = get_button_once(self.joystick.get_button, 6)
        self.start_input = get_button_once(self.joystick.get_button, 7)
        self.l_stick_input = get_button_once(self.joystick.get_button, 8)
        self.r_stick_input = get_button_once(self.joystick.get_button, 9)
        self.west_input = get_hat_once(self.joystick.get_hat, 0, 0)
        self.east_input = get_hat_once(self.joystick.get_hat, 0, 1)
        self.north_input = get_hat_once(self.joystick.get_hat, 0, 2)
        self.south_input = get_hat_once(self.joystick.get_hat, 0, 3)"""
        self.a_input = [0, 0]
        self.b_input = [0, 0]
        self.x_input = [0, 0]
        self.y_input = [0, 0]
        self.lb_input = [0, 0]
        self.rb_input = [0, 0]
        self.back_input = [0, 0]
        self.start_input = [0, 0]
        self.l_stick_input = [0, 0]
        self.r_stick_input = [0, 0]
        self.west_input = [0, 0]
        self.east_input = [0, 0]
        self.north_input = [0, 0]
        self.south_input = [0, 0]
        self.control_invert = False
        self.movement_message = [0, 0, 0, 0, 0, 0]  #strafe, drive, yaw, updown, tilt, 0
        self.direct_input = [0, 0, 0, 0, 0, 0]
        self.active = True #[True, False, False]  #Analog, South, West
        self.EM1_L = False
        self.EM1_R = False
        self.EM2_L = False
        self.EM2_R = False
        self.show_transectline = False
        self.thumb_profile_cycle = 0
        super().__init__()

    @Module.loop(1)
    def run_get_joystick(self):
        pygame.event.pump()
        num_axis = self.joystick.get_numaxes()
        for i in range(num_axis):
            self.direct_input[i] = self.joystick.get_axis(i)

    
    @Module.loop(1)
    def run_get_buttons(self):
        self.a_input = [self.a_input[0],self.joystick.get_button(0)]
        self.b_input = [self.b_input[0],self.joystick.get_button(1)]
        self.x_input = [self.x_input[0],self.joystick.get_button(2)]
        self.y_input = [self.y_input[0],self.joystick.get_button(3)]
        self.lb_input = [self.lb_input[0],self.joystick.get_button(4)]
        self.rb_input = [self.rb_input[0],self.joystick.get_button(5)]
        self.back_input = [self.back_input[0],self.joystick.get_button(6)]
        self.start_input = [self.start_input[0],self.joystick.get_button(7)]
        self.l_stick_input = [self.l_stick_input[0],self.joystick.get_button(8)]
        self.r_stick_input = [self.r_stick_input[0],self.joystick.get_button(9)]
        self.west_input = [self.west_input[0], hat_mapping(self.joystick.get_hat(0))[0]]
        self.east_input = [self.east_input[0], hat_mapping(self.joystick.get_hat(0))[1]]
        self.north_input = [self.north_input[0], hat_mapping(self.joystick.get_hat(0))[2]]
        self.south_input = [self.south_input[0], hat_mapping(self.joystick.get_hat(0))[3]]

    @Module.loop(1)
    def run_mapping(self):
        LLR, LUD, BL, RLR, RUD, BR = self.direct_input
        LLR = -1*deadzoneleft(LLR)
        LUD = -1*deadzoneleft(LUD)
        BL = -((BL+1)/2)
        BR = (BR+1)/2
        #print(BL)
        BLR = BL+BR
        #print(BLR)
        RLR = deadzoneright(RLR)
        RUD = -1*deadzoneright(RUD)
        new_movement_message = [RLR, LUD, LLR, RUD, BLR, 0]
        if new_movement_message != self.movement_message:
            self.movement_message = new_movement_message[:]
        pub.sendMessage("gamepad.movement", message = {"gamepad_message":self.movement_message})

        #print(button_pressed(self.l_stick_input))
        if button_pressed(self.l_stick_input):
            self.thumb_profile_cycle = (self.thumb_profile_cycle-1)%4
            pub.sendMessage("gamepad.profile", message = {"Profile_Dict": ProfileDict[self.thumb_profile_cycle]})
        if button_pressed(self.r_stick_input):
            self.thumb_profile_cycle = (self.thumb_profile_cycle+1)%4
            pub.sendMessage("gamepad.profile", message = {"Profile_Dict": ProfileDict[self.thumb_profile_cycle]})

        if button_pressed(self.lb_input):
            self.EM1_L = not self.EM1_L
            pub.sendMessage("gamepad.EM1", message = {"EM_L": self.EM1_L, "EM_R": self.EM1_R})
        if button_pressed(self.rb_input):
            self.EM1_R = not self.EM1_R
            pub.sendMessage("gamepad.EM1", message = {"EM_L": self.EM1_L, "EM_R": self.EM1_R})

        if button_pressed(self.west_input):
            self.EM2_L = not self.EM2_L
            pub.sendMessage("gamepad.EM2", message = {"EM_L": self.EM2_L, "EM_R": self.EM2_R})
        if button_pressed(self.east_input):
            self.EM2_R = not self.EM2_R
            pub.sendMessage("gamepad.EM2", message = {"EM_L": self.EM2_L, "EM_R": self.EM2_R})

        if button_pressed(self.x_input):
            self.control_invert = not self.control_invert
            pub.sendMessage("gamepad.invert", message = {"invert": self.control_invert}) #For GUI

        



    def destroy(self):
        print("Destroyed")

if __name__ == "__main__":
    from Module_Base_Async import AsyncModuleManager
    def debug_listener_profile(message):
        print("\t\t\t\t\t", "profile", message,"\n")

    def debug_listener_movement(message):
        print(message["gamepad_message"])

    def debug_listener_EM1(message):
        print("EM1: ", message)
    def debug_listener_EM2(message):
        print("EM2: ", message)

    #pub.subscribe(debug_listener_profile, 'gamepad.profile')
    joystick = Joystick()
    joystick.start(50)
    pub.subscribe(debug_listener_movement, 'gamepad.movement')
    pub.subscribe(debug_listener_EM1, 'gamepad.EM1')
    pub.subscribe(debug_listener_EM2, 'gamepad.EM2')
    pub.subscribe(debug_listener_profile, 'gamepad.profile')
    AsyncModuleManager.register_module(joystick)
    
    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
