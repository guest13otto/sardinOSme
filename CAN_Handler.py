'''
CAN_Handler Module

Subscribe Topics:

cansend
    address: Integer
    data: Tuple

Publish Topics:

log.sent:
    message

log.error:
    message

'''

import can
from ModuleBase import Module
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.message_listener, "cansend")

    def message_listener(self, adddress, data):
        msg = can.Message(arbitration_id = address, data = data, is_extended_id = False)


        try:
            self.bus.send(msg)
            pub.sendMessage("log.sent" , message = msg)

        except Can.CanError:
            pub.sendMessage("log.error" , message = msg)

    def run(self):
        message = self.bus.recv(1)

class __Test_Case_Send__(Module):
    data = [0x20, 7000>>8 & 0xFF, 7000 & 0xFF]
    pub.sendMessage('cansend', 0x0ff, data)

if __name__ == "__main__":

    def logger(message):
        print(message)

    can_handler = CAN_Handler()
    can_handler.start(10)
    pub.subscribe(logger, "log.sent")
    pub.subscribe(logger, "log.error")

    test_case_send = __Test_Case_Send__()
    test_case_send.start(10)
