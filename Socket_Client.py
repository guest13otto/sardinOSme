import socketio
import asyncio
import yaml
from pubsub import pub
from Module_Base_Async import Module

class cpub(Module):
    sio = socketio.AsyncClient()

    def __init__(self, ip, port, config_file):
        super().__init__()
        self.handlers = {}
        self.pub_senders = []
        self.topic_event = {}
        self.topic_message = {}
        self.ip = ip
        self.port = int(port)
        content = yaml.load(open(config_file, 'r'), Loader = yaml.FullLoader)
        try:
            for handler_name, topic in content.items():
                setattr(self.__class__, f'{handler_name}_handler', self._handler)
                pub.subscribe(getattr(self, f"{handler_name}_handler"), topic)
                self.handlers[f"{handler_name}_handler"] = getattr(self, f"{handler_name}_handler")
                self.topic_event[topic] = asyncio.Event()
                self.set_task(self.pub_sender, f"{self.__class__.__name__}.pub_sender_{handler_name}", self.topic_event[topic])
                self.pub_senders.append(f"{self.__class__.__name__}.pub_sender_{handler_name}")
        except AttributeError:
            print("config file empty")

        
    def _handler(self, message, topic = pub.AUTO_TOPIC):
        topic = topic.getName()
        self.topic_message[topic] = message
        if not self.topic_event[topic].is_set():
            self.topic_event[topic].set()

    async def pub_sender(self, event):
        while True:
            await event.wait()
            for topic, event_obj in self.topic_event.items():
                if event==event_obj:
                    await self.send(topic = topic, message = self.topic_message[topic])
                    event_obj.clear()

    def run_once(self):
        for pub_sender in self.pub_senders:
            pub.sendMessage("AsyncModuleManager", target = pub_sender, command = "start")


    @sio.event
    async def connect():
        print('connected to server')

    @sio.event
    async def disconnect():
        print("disconnected from server")

    @Module.asyncloop(1)
    async def run_try_connect_client(self):
        try:
            await self.sio.connect(f'http://{self.ip}:{self.port}')
        except socketio.exceptions.ConnectionError as e:
            print("connecting...", e)
        except:
            pass

    @sio.event
    async def recv(data):
        pub.sendMessage(data["topic"], message = data["message"])

    async def send(self, topic, message):
        await __class__.sio.emit("recv", data = {"topic":topic, "message":message})

    def destroy(self):
        print("cpub destroy")