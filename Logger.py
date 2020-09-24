from pubsub import pub
from Module_Base_Async import Module
import yaml
import logging
import logging.config

AllTopics = {"Gamepad": 'gamepad',
             "ControlProfile": 'command',
             "Thruster_Power": 'Thruster',
             "Thruster": 'can',
             "CAN_Handler": 'log'
             }

class Logger(Module):

    def Factory(self, topic):
        def innerListener(message):
            level = message.get("logLevel")
            try:
                print(f"self.{topic}.{level}({message})")
            except KeyError:
                exec(f"self.{topic}.debug({message})")
        return innerListener

    def __init__(self, Print, Log, Topics):
        super().__init__()
        with open('LoggerConfig.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        #self.logger = logging.getLogger('Logger')
        #self.printer = logging.getLogger('Printer')
        self.Print = Print
        self.Log = Log
        self.Topics = tuple(map(str, Topics.split(',')))
        #print(self.Topics)

        for topic in self.Topics:
            exec(f"self.{topic} = logging.getLogger('{topic}')")

            if self.Print:
                #https://stackoverflow.com/questions/6333916/python-logging-ensure-a-handler-is-added-only-once
                exec(f"self.{topic}.addHandler(logging.console)")
            elif self.Log and not self.Print:
                exec(f"self.{topic}.addHandler(Logger_file, Logger_console)")
            elif self.Log and self.file:
                exec(f"self.{topic}.addHandler(Logger_file, console)")
            else:
                pass

            exec(f"{topic}_listener = self.Factory({topic})")
            exec(f'pub.subscribe({topic}_listener, "{topic}")')

    def run(self):
        pass


if __name__ == "__main__":
    Logger = Logger(Print = True, Log = False, Topics = "gamepad,command")
    pub.sendMessage("gamepad.sdfs", message = {"logLevel": "warning","Ricky": "dehydrtion"})
