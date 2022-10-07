from pubsub import pub
from Module_Base import Module, Async_Task
import pygame
import platform

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
        #pub.subscribe(self.move_forward_listener, "moveforward.stop")
        self.c = 0
        super().__init__()

    @Async_Task.loop(1)
    async def get_joystick(self):
        ## KEEEP
        pygame.event.pump()
        self.c += 0.01
        if self.c >=1:
            self.c = -1
        pub.sendMessage("gamepad.movement", message = {"gamepad_message": [self.c,0,0,0,0,0]})



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
    def debug_listener_tool_states(message):
        print("em_state", message)
    def debug_listener_selected_tool(message):
        print("selected_tool", message)


    pub.subscribe(debug_listener_profile, 'gamepad.profile')
    joystick = Joystick()
    joystick.start(50)
    pub.subscribe(debug_listener_gripper, "gamepad.gripper")
    #pub.subscribe(debug_listener_movement, 'gamepad.movement')
    pub.subscribe(debug_listener_EM1, 'gamepad.EM1')
    pub.subscribe(debug_listener_EM2, 'gamepad.EM2')
    pub.subscribe(debug_listener_erector, 'gamepad.erector')
    pub.subscribe(debug_listener_tool_states, "gamepad.em_states")
    pub.subscribe(debug_listener_selected_tool, "gamepad.selected_tool")
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
