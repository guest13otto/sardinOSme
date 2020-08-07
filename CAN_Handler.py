

'''
CAN_Handler Module

Subscribe Topics:

can.send
    address <hexadecimal>
    data <bytearrray>

Publish Topics:

log.sent:
    message frame

log.error:
    message frame

can.receive.<arbitration_id>:
    data <bytearray>
    extra <dictionary>
	"timestamp" <float>

'''

import can
from Module_Base import Module
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        self.bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)
        pub.subscribe(self.message_listener, "can.send")
        #notifier = can.Notifier(self.bus, [CAN_Listener])

    def message_listener(self, address, data):
        msg = can.Message(arbitration_id = address, data = data, is_extended_id = False)
        try:
            self.bus.send(msg)
            pub.sendMessage("log.sent" , message = msg)

        except can.CanError:
            pub.sendMessage("log.error" , message = msg)


    def run(self):
        message = self.bus.recv(1)
        #print("received:", message)
        if message != None:
            topic_name = "can.receive." + str(hex(message.arbitration_id))[2:]
            #print("topic_name: ", topic_name)
            pub.sendMessage(topic_name, message = message.data, extra = {"timestamp": message.timestamp})
            

class __Test_Case_Send__(Module):
    def run(self):
        pub.sendMessage('can.send', address = 0xff,data = bytearray([0x10]))

if __name__ == "__main__":

    def logger_sent(message):
        print("log.sent: ", message)

    def logger_error(message):
        print("log.error: ", message)

    def logger_receive(message, extra):
        print("can.receive: ", message, "can.extra: ", extra)

    can_handler = CAN_Handler()
    can_handler.start(1)

    test_case_send = __Test_Case_Send__()
    test_case_send.start(1)

    pub.subscribe(logger_sent, "log.sent")
    pub.subscribe(logger_error, "log.error")
    pub.subscribe(logger_receive, "can.receive")
