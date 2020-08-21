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
from Module_Base import Module

class ControlProfile(Module):
    def __init__(self, max_percentage = 100, formula_modifier = 30, activate = 'A'):
        pub.subscribe(self.movementListener, 'gamepad.movement')
        pub.subscribe(self.profileListener, 'gamepad.profile')
        self.max_percentage = int(max_percentage)/100
        self.formula_modifier = float(formula_modifier)
        self.activate = activate
        self.profile_change = 'A'

    def run(self):
        pass

    @staticmethod
    def PowerFunction(A, B):
        if A >=0:
            return 1/B*(((B+1)**A)-1)
        else:
            return -1/B*(((B+1)**-A)-1)

    def movementListener(self, message):
        if self.profile_change == self.activate:
            Strafe, Drive, Yaw, Updown, TiltFB, TiltLR = message
            Strafe = self.PowerFunction(Strafe, self.formula_modifier)
            Drive = self.PowerFunction(Drive, self.formula_modifier)
            Yaw = self.PowerFunction(Yaw, self.formula_modifier)
            Updown = self.PowerFunction(Updown, self.formula_modifier)
            TiltFB = self.PowerFunction(TiltFB, self.formula_modifier)
            TiltLR = self.PowerFunction(TiltLR, self.formula_modifier)

            pub.sendMessage("command.movement", message = (Strafe, Drive, Yaw, Updown, TiltFB, TiltLR))

    def profileListener(self, message):
        self.profile_change = message
class __Test_Case_Send__(Module):
    def __init__(self):
        pub.subscribe(self.command_movement_listener, "command.movement")

    def command_movement_listener(self, message):
        print(f"message: ", message)

    def run(self):
        pass
        #pub.sendMessage("gamepad.movement", message = (0.2,0,0,0,0,0))
        #pub.sendMessage("gamepad.profile", message = 'A')

if __name__ == "__main__":
    from Gamepad import Gamepad
    Gamepad = Gamepad()
    Gamepad.start(100)

    __test_case_send__ = __Test_Case_Send__()
    __test_case_send__.start(1)

    ControlProfile = ControlProfile(100, 0.0001, 'A')
