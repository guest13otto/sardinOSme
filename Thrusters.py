'''
Subscribe Topics:

Thruster.Power
    message: FL, FR, BL, BR, BL, UF, UB <-1, 1>

Publish Topics:

can.send
    address <hexadecimal>
    data <bytearray>

'''


from Module_Base import Module, Async_Task
from pubsub import pub
import yaml
import numpy as np

class Thrusters(Module):
    def __init__ (self):
        super().__init__()
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
        self.target_power = [[0,0,0,0,0,0]]
        self.Thrusters = [self.ThrusterFL, self.ThrusterFR, self.ThrusterBL, self.ThrusterBR, self.ThrusterUF, self.ThrusterUB]


    @staticmethod
    def valmap(value, istart, istop, ostart, ostop):
      return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

    def listener(self, message):
        self.power = message["Thruster_message"]
        for list in self.power:
            for counter, power in enumerate(list):
                if power > 0:
                    self.target_power[0][counter] = self.valmap(power, 0, 1, self.Thrusters[counter]["Deadzone"], 1)
                elif power < 0:
                    self.target_power[0][counter] = self.valmap(power, 0, -1, -self.Thrusters[counter]["Deadzone"], -1)
                else:
                    self.target_power[0][counter] = 0
            #print(self.target_power)
    @Async_Task.loop(1)
    async def run(self):
        rate = self.rate * (1 / self.interval)
        #print("rate: ", rate)
        for list in self.target_power:
            for counter, power in enumerate(list):
                self.difference[counter] = power - self.current_power[counter]
                if abs(self.difference[counter]) > rate:
                    self.current_power[counter] += self.difference[counter]/abs(self.difference[counter])*rate
                else:
                    self.current_power[counter] = power
                if abs(self.current_power[counter]) > 1:
                    self.output_power[counter] = self.current_power/abs(self.current_power[counter])
                else:
                    self.output_power[counter] = self.current_power[counter]

                if self.output_power[counter] >= 0:
                    self.output_power[counter] = int(self.output_power[counter]*32767)
                else:
                    self.output_power[counter] = int(self.output_power[counter]*32768)
                #print(self.Thrusters)
                pub.sendMessage("can.send", message = {"address": self.Thrusters[counter]["Address"], "data": [32, self.output_power[counter] >> 8 & 0xff, self.output_power[counter] & 0xff]})
        #print(f"difference: {self.difference}")
        #print(f"current_power: {self.current_power}")
        #print(f"output_power: {self.output_power}")
                pub.sendMessage("info", message = {"output_power": self.output_power})
        #print(self.Thrusters[0]["Address"])
        #print(f"rate: {rate}")


class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()
        pub.subscribe(self.can_send_listener, "can.send")

    def can_send_listener(self, message):
        print('address:' ,message["address"], 'data(binary):', message["data"], 'data(int):', message["data"][1] << 8| message["data"][2])

    def run(self):
        pub.sendMessage("Thruster.Power", message = {"Thruster_message": [[0.0001,0,0,0,0,0]]})
        self.stop_all()

if __name__ == "__main__":
    from Gamepad import Gamepad
    #Gamepad = Gamepad()
    #Gamepad.start(1)

    Thrusters = Thrusters()
    Thrusters.start(1)

    __test_case_send__ = __Test_Case_Send__()
    __test_case_send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(__test_case_send__, Thrusters)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
