import time
from Module_Base import Module, Async_Task
from pubsub import pub


class Move_Forward(Module):
    def __init__(self, start_countdown, duration, power):
        super().__init__()
        self.start_countdown = float(start_countdown)
        self.duration = float(duration)
        self.start_time = False
        self.movement_message = (0, -float(power), 0.04, 0, -0.6, 0)
        pub.subscribe(self.start_listener, "gamepad.move_forward")

    def start_listener(self, message):
        if message["start"] == 1:
            self.start_time = time.time()
        else:
            self.start_time = False

    @Async_Task.loop(1)
    async def run(self):
        elapsed_time = time.time()-self.start_time
        if not self.start_time:
            pub.sendMessage("moveforward.stop", message = {"stop": True})
        elif elapsed_time < self.start_countdown:
            pass
        elif elapsed_time < self.duration+self.start_countdown:
            pub.sendMessage("gamepad.movement", message = {"gamepad_message": self.movement_message})
        else:
            pub.sendMessage("gamepad.movement", message = {"gamepad_message": (0, 0, 0, 0, 0, 0)})
            pub.sendMessage("moveforward.stop", message = {"stop": True})
            self.start_time = False
