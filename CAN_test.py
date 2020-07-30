import can

bus = can.interface.Bus(bustype = "socketcan", channel = "can0", bitrate = 250000)


def can_receive(can):
    message = can.Message
    print(message.data)
    print(message.arbitration_id)

while True:
    notifier = can.Notifier(bus, [can_receive(can)]
    msg = can.Message(arbitration_id = 0xff, data = 0x10, is_extended_id = False)
    bus.send(msg)

