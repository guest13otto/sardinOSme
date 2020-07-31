
'''
CAN_Handler Module

Subscribe Topics:

cansend
    data: Tuple
    data[1]: address <hexadecimal>
    data[2]: command <hexadecimal>

Publish Topics:

can.sent:
    message

can.error:
    message

can.receive.<arbitration_id>:
    message

'''

import can
from Module_Base import Module
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.message_listener, "cansend")
        #notifier = can.Notifier(self.bus, [CAN_Listener])

    def message_listener(self, data):
        msg = can.Message(arbitration_id = data[0], data = data[1:], is_extended_id = False)
        try:
            self.bus.send(msg)
            pub.sendMessage("can.sent" , message = msg)

        except can.CanError:
            pub.sendMessage("can.error" , message = msg)


    def run(self):
        message = self.bus.recv(0.5)
        #print("received:", message)
        if message != None:
            pub.sendMessage("can.receive", message = message)

class __Test_Case_Send__(Module):
    def run(self):
        data = (0xff, 0x10)
        pub.sendMessage('cansend', data = data)

if __name__ == "__main__":

    def logger_sent(message):
        print("log.sent: ", message)

    def logger_error(message):
        print("log.error: ", message)

    def logger_receive(message):
        print("log.receive: ", message.arbitration_id)

    can_handler = CAN_Handler()
    can_handler.start(10)

    test_case_send = __Test_Case_Send__()
    test_case_send.start(0.4)

    pub.subscribe(logger_sent, "log.sent")
    pub.subscribe(logger_error, "log.error")
    pub.subscribe(logger_receive, "can.receive")
