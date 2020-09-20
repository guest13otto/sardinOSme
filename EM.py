from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
from pubsub import pub
import asyncio

OnCommand = 0x10


EMLRcommand = {
                "EM_L": {1 : [0x30, 0x10], 0: [0x30, 0x00]},
                "EM_R": {1 : [0x31, 0x10], 0: [0x31, 0x00]},
                }

class EM(Module):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address
        exec(f'pub.subscribe(self.Listener, "gamepad.{self.name}")')

    def run(self):
        pass

    def Listener(self, message):
        pub.sendMessage("can.send", message = {"address": eval(self.address), "data": EMLRcommand[str(list(message.keys())[0])][list(message.values())[0]]})
        #pub.sendMessage("can.send", message = {"address": eval(self.address), "data": [0x31, 0x10]})

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    def run(self):
        pub.sendMessage("gamepad.EM1", message = {"EM_R": 0})

    def Listener(self, message):
        print(message)

if __name__ == "__main__":
    from Gamepad import Gamepad

    EM1 = EM("EM1", '0x31')
    EM2 = EM("EM2", '0x32')
    EM1.start(1)
    EM2.start(1)
    Gamepad = Gamepad()
    #Gamepad.start(10)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Gamepad, EM1, EM2, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        #print("Closing Loop")
        AsyncModuleManager.stop_all()
