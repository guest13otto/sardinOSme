import time
from Module_Base import Module, Async_Task
from pubsub import pub


class Move_Forward(Module):
    def __init__(self, seconds, power):
        super().__init__()
        self.seconds = float(seconds)
        self.start_time = False
        self.movement_message = (0, float(power), 0, 0, 0, 0)
        pub.subscribe(self.start_listener, "gamepad.move_forward")

    def start_listener(self, message):
        if message["start"] == 1:
            self.start_time = time.time()
        else:
            self.start_time = False

    @Async_Task.loop(1)
    async def run(self):
        if not self.start_time:
            pub.sendMessage("moveforward.stop", message = {"stop": True})
        elif time.time()-self.start_time < self.seconds:
            pub.sendMessage("gamepad.movement", message = {"gamepad_message": self.movement_message})
        else:
            pub.sendMessage("moveforward.stop", message = {"stop": True})
            self.start_time = False
