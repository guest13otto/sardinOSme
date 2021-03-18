from pubsub import pub
from Module_Base import Module, Async_Task
import pygame
import platform

# constants
DEADZONE_THRESHOLD_L = 0.1
DEADZONE_THRESHOLD_R = 0.1
DEADZONE_THRESHOLD_Z = 0.1
ProfileChars = ("A", "B", "C", "D")


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

def button_pressed(button_record):
    if button_record[0]!=button_record[1] and button_record[1]==1:
        button_record[0] = button_record[1]
        return True
    button_record[0] = button_record[1]
    return False

def button_hold(button_record):
    button_record[0] = button_record[1]
    if button_record[1] == 1:
        return True
    else:
        return False


class Joystick(Module):
    def __init__(self):
        #Prerequisite
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


        #Active Tool Modes
        self.active_tool = ""
        self.active_tools = ("gamepad.gripper", "gamepad.EM1", "gamepad.EM2", "gamepad.erector")
        self.bumper_hold = (True, False, False, True)  #Determines if the corresponding active tool requires holding down activation
        self.last_tool = ""

        #Inputs
        self.a_input = [0, 0]
        self.b_input = [0, 0]
        self.x_input = [0, 0]
        self.y_input = [0, 0]
        self.lb_input = [0, 0]
        self.rb_input = [0, 0]
        self.back_input = [0, 0]
        self.start_input = [0, 0]
        self.guide_input = [0, 0]
        self.l_stick_input = [0, 0]
        self.r_stick_input = [0, 0]
        self.west_input = [0, 0]
        self.east_input = [0, 0]
        self.north_input = [0, 0]
        self.south_input = [0, 0]


        #State variables
        self.control_invert = False
        self.new_movement_message = [0, 0, 0, 0, 0, 0]
        self.movement_message = [0, 0, 0, 0, 0, 0]  #strafe, drive, yaw, updown, tilt, 0
        self.direct_input = [0, 0, 0, 0, 0, 0]
        self.bumper_hold_on = False
        self.bumper_hold_default_sent = False
        self.show_transectline = False
        self.thumb_profile_cycle = 0

        '''
        self.active = True #[True, False, False]  #Analog, South, West
        self.EM1_L = False
        self.EM1_R = False
        self.EM2_L = False
        self.EM2_R = False
        self.gripper_default_sent = False
        '''
        

        
        super().__init__()
    

    def change_active_tool(self, tool_index : int):
        pub.sendMessage("joystick.tool_change", message={"index": tool_index, "name": self.active_tools[tool_index]})
        """
        Automatically handle change of active tool when index to self.active_tools is inputted\n
        self.active_tools = [False, False, False, False] <= Gripper, EM_Left, EM_Right, Erector
        """
        if self.active_tool:
            pub.sendMessage(self.active_tool, message = {"tool_state": 0})
        _new_tool = self.active_tools[tool_index]
        if self.active_tool == _new_tool:
            self.active_tool = ""
        else:
            self.active_tool = _new_tool
        self.bumper_hold_on = self.bumper_hold[tool_index]
        self.bumper_hold_default_sent = False


    @Async_Task.loop(1)
    async def get_joystick(self):
        pygame.event.pump()
        for i in range(self.joystick.get_numaxes()):
            self.direct_input[i] = self.joystick.get_axis(i)


    @Async_Task.loop(1, condition = "platform.system() == 'Windows'")
    async def get_buttons_win(self):
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

    @Async_Task.loop(1, condition = "platform.system() == 'Linux'")
    async def get_buttons_linux(self):
        self.a_input = [self.a_input[0],self.joystick.get_button(0)]
        self.b_input = [self.b_input[0],self.joystick.get_button(1)]
        self.x_input = [self.x_input[0],self.joystick.get_button(2)]
        self.y_input = [self.y_input[0],self.joystick.get_button(3)]
        self.lb_input = [self.lb_input[0],self.joystick.get_button(4)]
        self.rb_input = [self.rb_input[0],self.joystick.get_button(5)]
        self.back_input = [self.back_input[0],self.joystick.get_button(6)]
        self.start_input = [self.start_input[0],self.joystick.get_button(7)]
        self.guide_input = [self.guide_input[0],self.joystick.get_button(8)]
        self.l_stick_input = [self.l_stick_input[0],self.joystick.get_button(9)]
        self.r_stick_input = [self.r_stick_input[0],self.joystick.get_button(10)]
        self.west_input = [self.west_input[0], hat_mapping(self.joystick.get_hat(0))[0]]
        self.east_input = [self.east_input[0], hat_mapping(self.joystick.get_hat(0))[1]]
        self.north_input = [self.north_input[0], hat_mapping(self.joystick.get_hat(0))[2]]
        self.south_input = [self.south_input[0], hat_mapping(self.joystick.get_hat(0))[3]]


    @Async_Task.loop(1, condition = "platform.system() == 'Windows'")
    async def mapping_win(self):
        LLR, LUD, BLR, RUD, RLR, _ = self.direct_input
        LLR = 1*deadzoneleft(LLR)
        LUD = -1*deadzoneleft(LUD)
        RLR = 1*deadzoneright(RLR)
        RUD = -1*deadzoneright(RUD)
        BLR = -1*deadzone_back(BLR)
        if self.control_invert:
            self.new_movement_message = [-LLR, -LUD, -RLR, BLR, -RUD, 0]       #(strafe, drive, yaw, updown, tilt, 0)
        else:
            self.new_movement_message = [ LLR,  LUD, -RLR, BLR,  RUD, 0]


    @Async_Task.loop(1, condition = "platform.system() == 'Linux'")
    async def mapping_linux(self):
        LLR, LUD, BL, RLR, RUD, BR = self.direct_input
        LLR = 1*deadzoneleft(LLR)
        LUD = -1*deadzoneleft(LUD)
        BL = -((BL+1)/2)
        RLR = 1*deadzoneright(RLR)
        RUD = -1*deadzoneright(RUD)
        BR = (BR+1)/2
        BLR = deadzone_back(BL+BR)
        if self.control_invert:
            self.new_movement_message = [-LLR, -LUD, -RLR, BLR, -RUD, 0]       #(strafe, drive, yaw, updown, tilt, 0)
        else:
            self.new_movement_message = [ LLR,  LUD, -RLR, BLR,  RUD, 0]

    @Async_Task.loop(1)
    async def pub_loop(self):
        if self.new_movement_message != self.movement_message:
            self.movement_message = self.new_movement_message[:]
        pub.sendMessage("gamepad.movement", message = {"gamepad_message":self.movement_message})

        if button_pressed(self.l_stick_input):
            self.thumb_profile_cycle = (self.thumb_profile_cycle-1)%len(ProfileChars)
            pub.sendMessage("gamepad.profile", message = {"Profile_Dict": ProfileChars[self.thumb_profile_cycle]})
        if button_pressed(self.r_stick_input):
            self.thumb_profile_cycle = (self.thumb_profile_cycle+1)%len(ProfileChars)
            pub.sendMessage("gamepad.profile", message = {"Profile_Dict": ProfileChars[self.thumb_profile_cycle]})

        if button_pressed(self.x_input):
            self.control_invert = not self.control_invert
            pub.sendMessage("gamepad.invert", message = {"invert": self.control_invert}) #For GUI

        if button_pressed(self.north_input):
            self.change_active_tool(0)

        if button_pressed(self.west_input):
            self.change_active_tool(1)

        if button_pressed(self.east_input):
            self.change_active_tool(2)

        if button_pressed(self.south_input):
            self.change_active_tool(3)

        if self.active_tool: #Check empty string ""
            if self.bumper_hold_on:
                if button_hold(self.lb_input):
                    pub.sendMessage(self.active_tool, message = {"tool_state": 1})
                    self.bumper_hold_default_sent = False
                elif button_hold(self.rb_input):
                    pub.sendMessage(self.active_tool, message = {"tool_state": -1})
                    self.bumper_hold_default_sent = False
                else:
                    if not self.bumper_hold_default_sent:
                        pub.sendMessage(self.active_tool, message = {"tool_state": 0})
                        self.bumper_hold_default_sent = True
            else:
                if button_pressed(self.lb_input):
                    pub.sendMessage(self.active_tool, message = {"tool_state": 1})
                if button_pressed(self.rb_input):
                    pub.sendMessage(self.active_tool, message = {"tool_state": -1})




if __name__ == "__main__":
    from Module_Base import ModuleManager
    def debug_listener_profile(message):
        print("\t\t\t\t\t", "profile", message,"\n")

    def debug_listener_movement(message):
        print(message["gamepad_message"])

    def debug_listener_EM1(message):
        print("EM1: ", message)
    def debug_listener_EM2(message):
        print("EM2: ", message)
    def debug_listener_gripper(message):
        print("gripper: ", message)
    def debug_listener_erector(message):
        print("erector: ", message)


    pub.subscribe(debug_listener_profile, 'gamepad.profile')
    joystick = Joystick()
    joystick.start(50)
    pub.subscribe(debug_listener_gripper, "gamepad.gripper")
    #pub.subscribe(debug_listener_movement, 'gamepad.movement')
    pub.subscribe(debug_listener_EM1, 'gamepad.EM1')
    pub.subscribe(debug_listener_EM2, 'gamepad.EM2')
    pub.subscribe(debug_listener_erector, 'gamepad.erector')
    #pub.subscribe(debug_listener_profile, 'gamepad.profile')
    mm = ModuleManager("")
    mm.start(1)
    mm.register_all()
    mm.start_all()

    try:
        mm.run_forever()
    except KeyboardInterrupt:
        print("keyboard interrupt")
    except BaseException:
        pass
    finally:
        print("Closing Loop")
