from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
from pubsub import pub

class EM(Module):
    def __init__(self, address):
        super().__init__()
        exec(f"pub.subscribe(self.Listener, '')")
        pub.subscribe(self.Listener, "gamepad.EM")

    @Module.asyncloop(1)
    async def run(self):
        pass

    def Listener(self, message):
        pass

class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.Listener, "can.send")

    @Module.asyncloop(1)
    def run(self):
        pass

    def Listener(self, message):
        print(message)

if __name__ == "__main__":

    Module = ModuleName()
    Module.start(1)
    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Module, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
