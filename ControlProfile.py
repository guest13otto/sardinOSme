'''
Control Profile Module

Subscribe Topics

gamepad.movement
    message: Vector6

gamepad.profile
    message: String

Publish Topics

command.movement
    message: Vector6

'''


from pubsub import pub
from Module_Base import Async_Task, Module

class ControlProfile(Module):
    def __init__(self, max_percentage = 100, formula_modifier = 30, activate = 'A'):
        super().__init__()
        pub.subscribe(self.movementListener, 'gamepad.movement')
        pub.subscribe(self.profileListener, 'gamepad.profile')
        self.max_percentage = int(max_percentage)/100
        self.formula_modifier = float(formula_modifier)
        self.activate = activate
        self.profile_change = 'A'

    @staticmethod
    def PowerFunction(A, B):
        if A >=0:
            return 1/B*(((B+1)**A)-1)
        else:
            return -1/B*(((B+1)**-A)-1)

    def movementListener(self, message):
        if self.profile_change == self.activate:
            Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message["gamepad_message"]
            Strafe = self.PowerFunction(Strafe, self.formula_modifier)
            Drive = self.PowerFunction(Drive, self.formula_modifier)
            Yaw = self.PowerFunction(Yaw, self.formula_modifier)
            Updown = self.PowerFunction(Updown, self.formula_modifier)
            TiltFB = self.PowerFunction(TiltFB, self.formula_modifier)
            TiltLR = self.PowerFunction(TiltLR, self.formula_modifier)

            Strafe *= self.max_percentage
            Drive *= self.max_percentage
            Yaw *= self.max_percentage
            Updown *= self.max_percentage
            TiltFB *= self.max_percentage
            TiltLR *= self.max_percentage

            pub.sendMessage("command.movement", message = {"command_message": (Strafe, Drive, Yaw, Updown, TiltFB, TiltLR)})

    def profileListener(self, message):
        self.profile_change = message["Profile_Dict"]
        #print(self.profile_change)
class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.command_movement_listener, "command.movement")

    def command_movement_listener(self, message):
        print(message["command_message"])

    @Async_Task.loop(1)
    async def run(self):
        pub.sendMessage("gamepad.movement", message = {"gamepad_message": (0.2,0,0,0,0,0)})
        pub.sendMessage("gamepad.profile", message = {"Profile_Dict": 'A'})

if __name__ == "__main__":
    from Joystick import Joystick
    from Module_Base import ModuleManager

    

    Gamepad = Joystick()
    #Gamepad.start(100)

    __test_case_send__ = __Test_Case_Send__()
    __test_case_send__.start(1)

    ControlProfileA = ControlProfile(100, 0.0001, 'A')
    ControlProfileB = ControlProfile(70, 0.0001, 'B')
    ControlProfileC = ControlProfile(50, 0.0001, 'C')
    ControlProfileD = ControlProfile(30, 0.0001, 'D')

    mm = ModuleManager("", (400, 400))
    mm.start(1)
    mm.register_all()
    mm.start_all()

    mm.register_modules(__test_case_send__, ControlProfileA, ControlProfileB, ControlProfileC, ControlProfileD)

    try:
        mm.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        mm.stop_all()
