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

    def __init__(self, topic, Print, log, handlers):
        self.topic = topic
        self.Print = Print
        self.log = log
        self.handlers = handlers
        #print(self.handlers)
        self.logger = logging.getLogger(self.topic)

        print(self.handlers)
        # for handler in self.handlers:
        #     if handler != "class":
        #         self.logger.addHandler(handler)
        #     else:

        '''for k,v in  logging.Logger.manager.loggerDict.items():
            print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) )
            if not isinstance(v, logging.PlaceHolder):
                for h in v.handlers:
                    print('     +++',str(h.__class__)[8:-2] )'''
        #print(f"type: {type(self.topic)}, topic: {self.topic}")

        #https://stackoverflow.com/questions/6333916/python-logging-ensure-a-handler-is-added-only-once

        pub.subscribe(self.listener, self.topic)
    def listener(self, message):

        level = message.get("logLevel")
        try:
            print(f"self.logger.{level}({message})")
        except KeyError:
            print(f"self.logger.debug({message})")

class Logger(Module):

    def __init__(self, Print, log, topics):
        super().__init__()
        with open('LoggerConfig.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
            self.handlers = config['handlers']
            logging.config.dictConfig(config)

        self.Print = Print
        self.log = log
        self.topics = tuple(map(str, topics.split(',')))

        if self.Print and not self.log:
            self.handlers = self.handlers["console"]
        elif self.log and not self.Print:
            self.handlers = self.handlers["Logger_file"].update(self.handlers["Logger_Print"])
        elif self.log and self.Print:
            self.handlers = self.handlers["Logger_file"]  self.handlers["console"]

        for topic in self.topics:
            if ' ' in topic: topic = topic[1:]
            exec(f"{topic} = TopicLogger('{topic}', {self.Print}, {self.log}, handlers = {self.handlers})")

    def run(self):
        pass


if __name__ == "__main__":
    Logger = Logger(Print = True, log = True, topics = "gamepad, command")
    pub.sendMessage("gamepad.sf", message = {"logLevel": "warning","Ricky": "dehydrtion"})
