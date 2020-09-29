from pubsub import pub
from Module_Base_Async import Module
from Module_Base_Async import AsyncModuleManager
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

    def __init__(self, topic, handlers):
        print(f"instantiated {topic}")
        self.topic = topic
        self.handlers = handlers
        self.logger = logging.getLogger(self.topic)

        self.logger.addHandler(self.handlers)

        '''for k,v in  logging.Logger.manager.loggerDict.items():
            print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) )
            if not isinstance(v, logging.PlaceHolder):
                for h in v.handlers:
                    print('     +++',str(h.__class__)[8:-2] )'''
        #print(f"type: {type(self.topic)}, topic: {self.topic}")

        pub.subscribe(self.listener, "gamepad")
        #exec("pub.subscribe(self.listener, f'self.topic')")
    def listener(self, message):
        print("received pub message")
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
            self.configHandlers = config['handlers']
            logging.config.dictConfig(config)

        self.Print = Print
        self.log = log
        self.topics = tuple(map(str, topics.split(',')))
        self.handlers = {}

        if self.Print and not self.log:
            self.handlers["console"] = self.configHandlers["console"]
        elif self.log and not self.Print:
            self.handlers["Logger_file"] = self.configHandlers["Logger_file"]
            self.handlers["Logger_console"] = self.configHandlers["Logger_console"]
        elif self.log and self.Print:
            self.handlers["Logger_file"] = self.configHandlers["Logger_file"]
            self.handlers["console"] = self.configHandlers["console"]

        # for topic in self.topics:
        #     while ' ' in topic: topic = topic[1:]
        #     exec(f"{topic} = TopicLogger('{topic}', {self.Print}, {self.log}, handlers = {self.handlers})")
        gamepad = TopicLogger('gamepad', self.handlers)

    def run(self):
        pass


class __Test_Case_Send__(Module):
    def __init__(self):
        super().__init__()

    @Module.asyncloop(1)
    async def run(self):
        print("sent test case")
        pub.sendMessage("gamepad", message = {"logLevel": "warning","Ricky": "dehydrtion"})



if __name__ == "__main__":
    Logger = Logger(Print = True, log = False, topics = "gamepad, command")
    Logger.start(1)

    __Test_Case_Send__ = __Test_Case_Send__()
    __Test_Case_Send__.start(1)
    AsyncModuleManager = AsyncModuleManager()
    AsyncModuleManager.register_modules(Logger, __Test_Case_Send__)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()
