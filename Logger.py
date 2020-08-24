from pubsub import pub
from Module_Base_Async import Module
import yaml

AllTopics = {"Gamepad": 'gamepad',
             "ControlProfile": 'command',
             "Thruster_Power": 'Thruster',
             "Thruster": 'can',
             "CAN_Handler": 'log'
             }
Topics = []

class Logger(Module):
    def __init__(self):
        super().__init__()
        '''try:
            content = yaml.load(open('config.yaml', 'r'), Loader = yaml.FullLoader)
            for key,value in content.items():
                for key, value in value.items():
                    if key == 'varclass':
                        Topics.append(value)
        except FileNotFoundError:
            pass'''
        for varclass in AllTopics:
            #print(varclass, AllTopics[varclass])
            exec(f"pub.subscribe(self.message_listener, '{AllTopics[varclass]}')")

    def message_listener(self, message):
        print(message)

    def run(self):
        pass


if __name__ == "__main__":
    Logger = Logger()

    pub.sendMessage("can.sdfs", message = {"Ricky": "dehydrtion"})
