from pubsub import pub
from Module_Base_Async import Module
import yaml
import logging
import logging.config
import copy

AllTopics = {"Gamepad": 'gamepad',
             "ControlProfile": 'command',
             "Thruster_Power": 'Thruster',
             "Thruster": 'can',
             "CAN_Handler": 'log'
             }

class TopicLogger:
    # console = logging.StreamHandler()
    # Logger_file = logging.FileHandler('console.log')
    # Logger_console = logging.StreamHandler()

    def __init__(self, topic, print, log):
        self.topic = topic
        self.print = print
        self.log = log
        self.logger = logging.getLogger(self.topic)

        if self.print:
            #https://stackoverflow.com/questions/6333916/python-logging-ensure-a-handler-is-added-only-once
            self.logger.addHandler(console)
        elif self.log and not self.print:
            self.logger.addHandler(Logger_file, Logger_console)
        elif self.log and self.print:
            self.logger.addHandler(Logger_file, console)
        else:
            pass

        pub.subscribe(self.listener, self.topic)
    def listener(self, message):
        level = message.get("logLevel")
        try:
            exec(f"logger.{level}({message})")
        except KeyError:
            exec(f"logger.debug({message})")

class Logger(Module):

    def __init__(self, print, log, topics):
        super().__init__()
        with open('LoggerConfig.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        
        self.print = print
        self.log = log
        self.topics = tuple(map(str, topics.split(',')))
        print(self.topics)

        for topic in self.topics:

            exec(f"{topic} = TopicLogger({topic}, {self.print}, {self.log})")

    def run(self):
        pass


if __name__ == "__main__":
    Logger = Logger(print = True, log = False, topics = "gamepad, command")
    pub.sendMessage("gamepad", message = {"logLevel": "warning","Ricky": "dehydrtion"})
