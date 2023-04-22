from Module_Base import Module, Async_Task
from pubsub import pub
import asyncio

class Gripper(Module):
    def __init__(self, device, address, speed, flip):
        super().__init__()
        self.device = device
        self.flip = int(flip)
        self.speed = int(speed)
        self.address = address
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.device}")')

    @Async_Task.loop(1)
    async def run(self):
        pass

    def Listener(self, message):
        tool_state = message["tool_state"]

        if self.flip:
            tool_state = -tool_state

        if tool_state == 1:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, self.speed >> 8 & 0xff, self.speed & 0xff]})
        elif tool_state == -1:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, -self.speed >> 8 & 0xff, -self.speed & 0xff]})
        else:
            pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [32, 0x00, 0x00]})

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.gripper", message = {"extend": False, "retract": True})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":

    Gripper = Gripper('gripper', '0x21', 17000)
    Gripper.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Gripper, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
