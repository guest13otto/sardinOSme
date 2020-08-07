import asyncio
from pubsub import pub

'''
-----------------------------------------------------------------------
Modules define like this:
from Module_Base_Async import Module


class test(Module):
    def __init__(self):
        super().__init__()                    #Must have this line

    @Module.loop(1)                           #Add this decorator to method name run to allow it to loop
    def run(self):                            #Loop functions must be name have the first three characters "run"
        print("from test")

    @Module.loop(2)                           #Argument to specify relative speed of run loops. run_another_loop loops 2x faster than run
    def run_another_loop(self):
        print("from another loop")

    @Module.loop(0.1)
    def run_cancel(self):
        self.cancel_all_local_task()          #End all loops in this object


Run Modules in main like this:
from Test import test

test_object = test()         
test_object.start(10)                         #10 represents 10 times per second

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()


-----------------------------------------------------------------------
'''

class Module():
    def __init__(self):
        self.relative_speed_multiplier = {}   # {"Test.run": 10}
        self.tasks = {}                       # {"Test.run: <Task pending coro=.......>"}
        self.inst = {}                        # {""}
        pub.subscribe(self.cancel_task_handler, self.__class__.__name__)
    
    async def exec_periodically(self, wait_time, func):
        while True:
            await asyncio.sleep(wait_time)
            func(self)

    async def schedule_task_periodically(self, wait_time, func):
        return asyncio.create_task(await self.exec_periodically(wait_time, func))

    @staticmethod
    def loop(speed_multiplier):
        def loop(func):
            def wrapper(varclass, record_name):
                varclass.relative_speed_multiplier[record_name] = [func, speed_multiplier]
            return wrapper
        return loop

    def start(self, interval):
        self.run_funcs = [method for method in dir(self) if method[:3]=="run" and callable(getattr(self, method))]
        for func_name in self.run_funcs:
            record_name = str(self.__class__.__name__)+"."+func_name
            exec(f"self.{func_name}('{record_name}')")
            self.inst[self.__class__.__name__] = self.__class__
            self.tasks[record_name] = asyncio.ensure_future(self.schedule_task_periodically((1/self.relative_speed_multiplier[record_name][1])*(1/interval), self.relative_speed_multiplier[record_name][0]))
    
    def clean_up(self):
        print("cleaned up")

    @staticmethod
    def start_loop():
        return asyncio.get_event_loop()

    def cancel_local_task(self, task, check_clean_up = True):
        if "." not in task:
            task = self.__class__.__name__+"."+task
        
        if not self.tasks[task].cancelled():
            self.tasks[task].cancel()
            print(self.tasks[task].cancelled())
        else:
            self.tasks[task] = None

        if check_clean_up:
            print([task.cancelled() for task in self.tasks.values()])
            if False not in [task.cancelled() for task in self.tasks.values()]:
                self.clean_up()

        
    def cancel_all_local_task(self):
        for record_name in self.tasks:
            self.cancel_local_task(record_name, check_clean_up=False)
        self.clean_up()

    def cancel_all_global_task(self, class_name):
        pub.sendMessage(class_name, task = class_name)

    def cancel_global_task(self, task):
        #print(task[:task.find(".")+1])
        pub.sendMessage(task[:task.find(".")], task = task)

    def cancel_task_handler(self, task):
        if "." in task:
            self.cancel_local_task(task)
        else:
            self.cancel_all_local_task()





if __name__ == "__main__":
    class Something(Module):
        def __init__(self):
            self.var = 0
            pub.subscribe(self.handler , "topic")
            super().__init__()

        def something_operation(self, num1, num2):
            return num1 *num1 + num2 * num2
        
        @Module.loop(10)
        def run(self):
            print(self.var)
            #self.var += 1

        @Module.loop(1)
        def run2(self):
            self.cancel_local_task("run")
            self.cancel_local_task("run2")


        def handler(self, var):
            self.var = var




    class Something2(Module):
        def __init__(self):
            self.var = 0
            super().__init__()

        @Module.loop(1)
        def run1(self):
            self.var +=1

        @Module.loop(10)
        def run2(self):
            pub.sendMessage("topic", var = self.var)
            #self.test(self.run1)

        '''
        @Module.loop(0.1)
        def run_canceller(self):
            print("cancel starts")
            self.cancel_all_global_task("Something")
            #self.cancel_global_task("Something.run2")
            print("task cancelled")
            #self.cancel_local_task("run_canceller")
            self.cancel_all_local_task()
            print("cancelled self")'''
    

    class EXIT(Module):
        def __init__(self):
            super().__init__()

        @Module.loop(1)
        def run(self):
            pass

        @Module.loop(0.05)
        def run_exit(self):
            print("exiting")
            exit()




    s = Something()
    s2 = Something2()
    Exit = EXIT()
    loop = Module.start_loop()
    s.start(1)
    s2.start(1)
    Exit.start(1)
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()


