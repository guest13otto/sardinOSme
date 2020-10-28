from aiohttp import web
import socketio
import asyncio
import yaml
from pubsub import pub
from Module_Base_Async import Module


class spub(Module):

    sio = socketio.AsyncServer()

    def __init__(self, ip, port, config_file):
        super().__init__()
        self.sio = __class__.sio
        self.app = web.Application()
        self.sio.attach(self.app)
        self.app.router.add_static('/static', 'static')
        self.app.router.add_get('/', self.index)
        self.ip = ip
        self.port = int(port)

        self.handlers = {}
        self.pub_senders = []
        self.topic_event = {}
        self.topic_message = {}
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
        self.topic_event[topic].set()

    async def pub_sender(self, event):
        while True:
            await event.wait()
            for topic, event_obj in self.topic_event.items():
                if event==event_obj:
                    event_obj.clear()
                    await self.send(topic = topic, message = self.topic_message[topic])

    def run_once(self):
        for pub_sender in self.pub_senders:
            pub.sendMessage("AsyncModuleManager", target = pub_sender, command = "start")

    @Module.asynconce
    async def run_start_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.ip, self.port)
        await site.start()
        print("server started")

        
    def index(self, request):
        with open('index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')

    @sio.event
    async def connect(sid, environ):
        print("connect ", sid)

    @sio.event
    async def disconnect(sid):
        print('disconnect ', sid)

    
    @sio.event
    async def recv(sid, data):
        pub.sendMessage(data["topic"], message = data["message"])

    async def send(self, topic, message):
        await __class__.sio.emit("recv", data = {"topic":topic, "message":message})