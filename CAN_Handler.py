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
from Module_Base import Module
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.message_listener, "cansend")

    def message_listener(self, data):
        msg = can.Message(arbitration_id = data[0], data = data[1:], is_extended_id = False)


        try:
            self.bus.send(msg)
            pub.sendMessage("log.sent" , message = msg)

        except can.CanError:
            pub.sendMessage("log.error" , message = msg)

    def run(self):
        message = self.bus.recv(1)

class __Test_Case_Send__(Module):
    def run(self):
        data = (0xff, 0x20, 3000>>8 & 0xFF, 3000 & 0xFF)
        pub.sendMessage('cansend', data = data)

if __name__ == "__main__":

    def logger_sent(message):
        print("message sent: ", message)

    def logger_error(message):
        print("message not sent: ", message)

    can_handler = CAN_Handler()
    can_handler.start(10)
    pub.subscribe(logger_sent, "log.sent")
    pub.subscribe(logger_error, "log.error")

    test_case_send = __Test_Case_Send__()
    test_case_send.start(10)
