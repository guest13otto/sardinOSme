from Module_Base import Module
from pubsub import pub
import yaml

class Thrusters(Module):
    def __init__(self):
        try:
            content = yaml.load(open('Thruster.yaml', 'r'), Loader = yaml.FullLoader)
            for key,value in content.items():
                exec(f"self.{key} = value")
        except FileNotFoundError:
            pass

        pub.subscribe(self.listener, "Thruster.Power")
        self.current_power = [0,0,0,0,0,0]
        self.output_power = [0,0,0,0,0,0]
        self.difference = [0,0,0,0,0,0]
        self.target_power = [0,0,0,0,0,0]
        self.Thrusters = [self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB]
        #print(f"rate: {self.rate}")

    def listener(self, message):
        self.target_power = message

    def run(self):
        self.rate *= self.interval
        #self.rate *= self.interval
        for counter, target_power in enumerate(self.target_power):
            self.difference[counter] = target_power - self.current_power[counter]
            if abs(self.difference[counter]) > self.rate:
                self.current_power[counter] += self.difference[counter]/abs(self.difference[counter])*self.rate
            else:
                self.current_power[counter] = target_power
            if abs(self.current_power[counter]) > 1:
                self.output_power[counter] = self.current_power/abs(self.current_power[counter])
            else:
                self.output_power[counter] = self.current_power[counter]

            if self.output_power[counter] >= 0:
                self.output_power[counter] = int(self.output_power[counter]*32767)
            else:
                self.output_power[counter] = int(self.output_power[counter]*32768)

        #print(f"difference: {self.difference}")
        #print(f"current_power: {self.current_power}")
        #print(f"output_power: {self.output_power}")
        #print(self.Thrusters[0]["Address"])
            pub.sendMessage("can.send", address = self.Thrusters[counter]["Address"], data = [32, self.output_power[counter] >> 8 & 0xff, self.output_power[counter] & 0xff])

class __Test_Case_Send__(Module):
    def __init__(self):
        pub.subscribe(self.can_send_listener, "can.send")

    def can_send_listener(self, address, data):
        print(f"address: {address}, data: {data}")

    def run(self):
        pub.sendMessage("Thruster.Power", message = (1,0,0,0,0,0))

if __name__ == "__main__":
    from Gamepad import Gamepad
    #Gamepad = Gamepad()
    #Gamepad.start(1)

    Thrusters = Thrusters()
    Thrusters.start(1)

    __test_case_send = __Test_Case_Send__()
    __test_case_send.start(1)
