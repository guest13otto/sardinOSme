

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
import at_serial_can
from Module_Base import Module, Async_Task
from pubsub import pub

class CAN_Handler(Module):
    def __init__(self):
        super().__init__()
        self.bus = at_serial_can.ATSerialBus(channel="COM4", bitrate=250000)
        pub.subscribe(self.message_listener, "can.send")
        #notifier = can.Notifier(self.bus, [CAN_Listener])

    def message_listener(self, message):
        msg = can.Message(arbitration_id = message["address"], data = message["data"], is_extended_id = False)
        self.bus.send(msg)
        # pub.sendMessage("log.sent" , message = msg)

    # @Async_Task.loop(1)
    # async def run(self):
    #     msg = self.bus.recv(0)
    #     # topic = "can.receive." + str(arbitration_id)
    #     if msg is not None:
    #         #pub.sendMessage("can.receive.", msg)
    #         print("CAN RX" , msg)


class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
    def run(self):
        pub.sendMessage('can.send', message = {"address": 0xff,"data": bytearray([0x10])})
        #self.stop_all()

if __name__ == "__main__":
    #to test run script on pi, and a CANBUS node that receives 0x10 command

    def logger_sent(message):
        print("log.sent: ", message)

    def logger_error(message):
        print("log.error: ", message)

    def logger_receive(message):
        print("can.receive: ", message["data"], "can.extra: ", message["extra"])

    pub.subscribe(logger_sent, "log.sent")
    pub.subscribe(logger_error, "log.error")
    pub.subscribe(logger_receive, "can.receive")

    can_handler = CAN_Handler()
    can_handler.start(1)
    test_case_send = __Test_Case_Send__()
    test_case_send.start(0.2)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(test_case_send, can_handler)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
