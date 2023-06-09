from Module_Base import Module, Async_Task
from pubsub import pub
import asyncio

class Light(Module):
    def __init__(self, device, address):
        super().__init__()
        self.device = device
        self.address = address
        self.light_on = False
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.device}")')

    @Async_Task.loop(1)
    async def run(self):
        pass

    def Listener(self, message):
        if message["light"] == 1:
            if self.light_on:
                pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [61]})
                self.light_on = False
            else:
                pub.sendMessage('can.send', message = {"address": eval(self.address), "data": [60, 0xFF, 0xFF, 0xFF]})
                self.light_on = True
        

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.light", message = {"on": False})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":

    Light = Light('light', '0x51')
    Light.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Light, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
