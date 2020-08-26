import asyncio
import threading
from pubsub import pub
import time

'''
-----------------------------------------------------------------------
NOTE: Modules define like this:
from Module_Base_Async import Module


class test(Module):
    def __init__(self):
        super().__init__()                    #Must have this line
                        
    @Module.loop(2)                           #Add this decorator to allow methods with name that starts with "run" to loop
    def run_another_loop(self):               #Loop functions must have the first three characters "run"
        print("from another loop")

    @Module.loop(0.1)                         #Argument to specify relative speed of run loops. run_another_loop loops 2x faster than run
    def run_useless(self):
        pass             

    @Module.asyncloop(1)                      #For coroutines 
    async def run_async_loop(self):
        await someCoroutine()                 #Can use await and other async keywords
        pass                     

    def run(self):                            #Method named "run" specifically will loop by itself, with run speed multiplier of 1
        print("from test")

    def run_once(self):                       #Method name starts with "run" but without loop/asyncloop decorator will run once at the start
        print("run once when Module starts")

    @Module.asynconce                         #Similar to run_once method, but allows the use of await and asynchronous functions inside
    async run_once_as_well(self):
        print("run once when Module starts") 
        await someCoroutine()                 #Can use await and other async keywords

    def cancel_run_useless(self):             #Method name "cancel_"+loop_name (ex. cancel_run, cancel_run_another_loop)
        print("run_useless clean-up done")    #Method called automatically if the specified loop is cancelled, used for task clean-up

    def destroy(self):                        #Add this if there are any clean-up code that needs to run when Module is destroyed
        print("Closed")

-----------------------------------------------------------------------
NOTE: Run Modules in main like this:

from Test import test                                               #Import the Module made above

test_object = test()
another_test = AnotherModule()         
test_object.start(10)                                               #10 represents 10 times per second
another_test.start(10)
AsyncModuleManager.register_modules(test_object, another_test)      #Must have this to work

try:
    AsyncModuleManager.run_forever()                                 
except KeyboardInterrupt:
    pass
except BaseException:
    pass
finally:
    print("Closing Loop")
    AsyncModuleManager.stop_all()
-----------------------------------------------------------------------
NOTE: Pub commands to AsyncModuleManager:
NOTE: Use within a Module

pub.sendMessage("AsyncModuleManager", target = "testModule", command = "destroy")               #Destroy a active Module
pub.sendMessage("AsyncModuleManager", target = "testModule", command = "restart")               #Restart a destroyed Module
pub.sendMessage("AsyncModuleManager", target = "testModule.some_method", command = "cancel")    #Cancel a running task
pub.sendMessage("AsyncModuleManager", target = "testModule.some_method", command = "start")     #Start a cancelled task
pub.sendMessage("AsyncModuleManager", target = "AsyncModuleManager", command = "status")        #Print out a report of the states of tasks
-----------------------------------------------------------------------
'''
class Thread_Task():
    class thread_default_name:
        val = 0

        @classmethod
        def __iter__(cls):
            cls.val+=1
            yield f"Thread_Task_{str(cls.val)}"

    class run_flag():
        def __init__(self):
            self.__is_activated = False

        def activate(self):
            self.__is_activated = True

        def deactivate(self):
            self.__is_activated = False

        def is_activated(self):
            return self.__is_activated


    def __init__(self, target, record_name = None, args=(), kwargs={}):
        self._running = self.run_flag()
        self.target = target
        self.record_name = record_name
        self.args = args
        self.kwargs = kwargs
        self.kwargs["__thread__"] = self._running
        if self.record_name==None:
            self.record_name = next(iter(__class__.thread_default_name()))
        self.thread = threading.Thread(target = self.target, args = self.args, kwargs = self.kwargs, daemon= True)

    def start(self):
        self._running.activate()
        self._alive = self.thread.is_alive()
        self.thread.start()

    def cancel(self):
        self._running.deactivate()

    def cancelled(self):
        return not self._running.is_activated()

    def done(self):
        return not self.thread.is_alive()

    def get_name(self):
        return self.record_name


    


class Module():
    @staticmethod
    async def __main_run__():
        while True:
            await asyncio.sleep(2)

    asyncio.ensure_future(__main_run__.__func__())
    def __init__(self):
        self.destroyed = False
        self.relative_speed_multiplier = {}     # {"Test.run": [<function Test.test at 0x...>, 10]}
        self.tasks = {}                         # {"Test.run": <Task pending coro=...>"}
        self.inst = {}                          # {"Test" : <__main__.test object at 0x...>}
        self.run_once_tasks = set()             # {"Test.run_once", "Test2.run_once"} no async      
        self.set_task_args_kwargs = {}          # {"Test.pub_handler":[<bound method Test.pub_handler>, [1, 3, "arg"], {"a": 2, "b": 5}]}    
    
    async def exec_periodically(self, wait_time, func, special_run = False):
        try:
            while True:
                await asyncio.sleep(wait_time)
                if special_run:
                    func()
                else:
                    func(self)
        except Exception as e:
            print(e)

    async def async_exec_periodically(self, wait_time, coro, special_run = False):
        while True:
            await asyncio.sleep(wait_time)
            if special_run:
                await coro()
            else:
                await coro(self)

    def thread_exec_periodically(self, wait_time, func, **kwargs):
        '''
        while kwargs["__thread__"].is_activated():
            time.sleep(wait_time)
            func(self)'''
        
        #print(wait_time)
        stopEvent = threading.Event()
        nextTime=time.time()+wait_time
        while (not stopEvent.wait(nextTime-time.time())) and kwargs["__thread__"].is_activated():
            nextTime+=wait_time
            func(self)

        

    def thread_exec_once(self, func, **kwargs):
        if kwargs["__thread__"].is_activated():
            func(self)




    @staticmethod
    def loop(speed_multiplier = 1):
        def outer(func):
            def wrapper(varclass, record_name, interval):
                varclass.relative_speed_multiplier[record_name] = [func, speed_multiplier]
                wait_time = 1/varclass.relative_speed_multiplier[record_name][1]*(1/interval)
                varclass.tasks[record_name] = asyncio.ensure_future(varclass.exec_periodically(wait_time, func))
            return wrapper
        return outer

    @staticmethod
    def asyncloop(speed_multiplier = 1):
        def outer(func):
            def wrapper(varclass, record_name, interval):
                coro = func
                varclass.relative_speed_multiplier[record_name] = [coro, speed_multiplier]
                wait_time = 1/varclass.relative_speed_multiplier[record_name][1]*(1/interval)
                varclass.tasks[record_name] = asyncio.ensure_future(varclass.async_exec_periodically(wait_time, coro))
            return wrapper
        return outer

    @staticmethod
    def threadloop(speed_multiplier = 1):
        def outer(func):
            def wrapper(varclass, record_name, interval):
                varclass.relative_speed_multiplier[record_name] = [func, speed_multiplier]
                wait_time = 1/varclass.relative_speed_multiplier[record_name][1]*(1/interval)
                thread = Thread_Task(target = varclass.thread_exec_periodically, record_name = record_name, args=(wait_time, func))
                varclass.tasks[record_name] = thread
                thread.start()
            return wrapper
        return outer

    @staticmethod
    def asynconce(func):
        def wrapper(varclass, record_name):
            coro= func
            varclass.tasks[record_name]=asyncio.ensure_future(coro(varclass))
        return wrapper

    @staticmethod
    def threadonce(func):
        def wrapper(varclass, record_name):
            varclass.tasks[record_name]=Thread_Task(target = varclass.thread_exec_once, record_name=record_name, args = ([func]))
            varclass.tasks[record_name].start()
        return wrapper


    def task_cleanup(self, task_name):
        cancel_task_name = "cancel_"+task_name[task_name.find(".")+1:]
        if hasattr(self, cancel_task_name):
            getattr(self, cancel_task_name)()

    def create_task(self, func_name, record_name, interval):
        try:
            getattr(self, func_name)(record_name = record_name, interval = interval)
        except TypeError:
            if func_name == "run":
                self.relative_speed_multiplier[record_name] = [getattr(self, "run"), 1]
                self.tasks[record_name] = asyncio.ensure_future(self.exec_periodically(1/interval, getattr(self, "run"), special_run=True))
            else:
                try:
                    getattr(self, func_name)(record_name = record_name)
                except:
                    self.run_once_tasks.add(record_name)
                    getattr(self, func_name)()

    def set_task(self, coro, record_name, *args, **kwargs):
        try:
            self.tasks[record_name] = asyncio.ensure_future(coro(*args, **kwargs))
            self.set_task_args_kwargs[record_name] = [coro, args, kwargs]
        except:
            print("Error in set task")

    def start(self, interval):
        self.destroyed = False
        self.interval = interval
        self.run_funcs = [method for method in dir(self) if method[:3]=="run" and callable(getattr(self, method))]
        for func_name in self.run_funcs:
            run_record_name = str(self.__class__.__name__)+"."+func_name
            self.create_task(func_name, run_record_name, interval)
        if len(self.tasks)==0:
            self.relative_speed_multiplier["run"] = [self.__run, 1]
            self.tasks["run"] = asyncio.ensure_future(self.exec_periodically(1, self.__run, special_run=True))
                
        self.inst[self.__class__.__name__] = self

    def __run(self):
        pass
                       
    def destroy(self):
        pass


class AsyncModuleManager():
    inst = {}
    relative_speed_multiplier = {}
    tasks = {}
    cancelling = set()
    run_once_tasks = set()

    @classmethod
    def module_command_handler(cls, target, command):
        try:
            if command == "start" or command == "restart":
                if "." in target:
                    cls.start_task(target)
                else:
                    cls.restart_module(target)
            elif command == "cancel" or command == "destroy":
                if "." in target:
                    cls.cancel_task(target)
                else:
                    cls.destroy_module(target)
            elif command == "status":
                cls.show_status(target)
            else:
                print(f"Invalid command sent: {command}")
        except:
            print(f"An error occured when trying to send [command: {command}] to [target: {target}]")
    
    @classmethod
    def register_module(cls, module):
        try:
            cls.inst.update(module.inst)
            cls.tasks.update(module.tasks)
            cls.relative_speed_multiplier.update(module.relative_speed_multiplier)
            cls.run_once_tasks = cls.run_once_tasks|module.run_once_tasks
        except:
            raise TypeError("Must provide Modules as arguments")

    @classmethod
    def register_modules(cls, *args):
        for module in args:
            cls.register_module(module)

    @classmethod
    def update_manager(cls, module=None):
        if module==None:
            try:
                for module_ref in cls.inst.values():
                    cls.update_manager(module_ref)
            except:
                print("problem with update manager")
        else:
            cls.inst.update(module.inst)
            cls.tasks.update(module.tasks)
            cls.relative_speed_multiplier.update(module.relative_speed_multiplier)
            cls.run_once_tasks = cls.run_once_tasks|module.run_once_tasks

    @classmethod
    def update_cancelling(cls):
        temp_cancelling = cls.cancelling.copy()
        for cancelling_task_name in temp_cancelling:
            varclass = cls.get_instance(cancelling_task_name)
            if varclass.tasks[cancelling_task_name].done():
                cls.cancelling.remove(cancelling_task_name)


    @classmethod
    def get_instance(cls, module_or_method):
        if "." in module_or_method:
            return cls.inst[module_or_method[:module_or_method.find(".")]]   
        else:
            return cls.inst[module_or_method]

    @classmethod
    def get_method_name(cls, task):
        return task[task.find(".")+1:]
    
    @classmethod
    def start_task(cls, task_name):
        varclass = cls.get_instance(task_name)
        if not varclass.destroyed:
            if varclass.tasks[task_name].done():
                if task_name in varclass.set_task_args_kwargs:
                    varclass.set_task(varclass.set_task_args_kwargs[task_name][0], task_name, *varclass.set_task_args_kwargs[task_name][1], **varclass.set_task_args_kwargs[task_name][2])
                else:
                    varclass.create_task(cls.get_method_name(task_name), task_name, varclass.interval)
                if task_name in cls.cancelling:
                    cls.cancelling.remove(task_name)
                cls.update_manager(varclass)
    
    @classmethod
    def cancel_task(cls, method_name):   
        varclass = cls.get_instance(method_name)  

        if not varclass.tasks[method_name].done():
            varclass.tasks[method_name].cancel()
            varclass.task_cleanup(method_name)
            cls.cancelling.add(method_name)
            cls.update_manager(varclass)

        if not varclass.destroyed:
            if False not in [non_cancelling_task.done() for task_name, non_cancelling_task in varclass.tasks.items() if task_name not in cls.cancelling]:
                varclass.destroy()
                varclass.destroyed = True

    @classmethod
    def restart_module(cls, module_name):
        varclass = cls.get_instance(module_name)
        if varclass.destroyed:
            varclass.start(varclass.interval)
            for task_name in varclass.tasks:
                if task_name in cls.cancelling:
                    cls.cancelling.remove(task_name)
            cls.update_manager(varclass)
    
    @classmethod
    def destroy_module(cls, module_name):
        varclass = cls.get_instance(module_name)
        cls.update_cancelling()

        for task_name, task in varclass.tasks.items():
            if not task.done():
                task.cancel()
                cls.cancelling.add(task_name)
                varclass.task_cleanup(task_name)

        if not varclass.destroyed:
            varclass.destroy()
            varclass.destroyed = True

        cls.update_manager(varclass)

    @classmethod
    def show_status(cls, target):
        def status_report(reference):
            import itertools
            cancelled_tasks = []
            active_tasks = []
            longest_name=20
            
            
            cls.update_manager()
            cls.update_cancelling()
            for task_name, task in reference.tasks.items():
                if len(task_name)>longest_name:
                    longest_name = len(task_name)
                if not task.done():
                    if task_name not in cls.cancelling:
                        active_tasks.append(task_name)
                else:
                    cancelled_tasks.append(task_name)
            for run_once_name in cls.run_once_tasks:
                if len(run_once_name) > longest_name:
                    longest_name = len(run_once_name)
                cancelled_tasks.append(run_once_name)
            longest_name+=5
            yield f"{'ACTIVE':{longest_name}}{'CANCELLING':{longest_name}}{'CANCELLED':{longest_name}}"
            for active_task, cancelling_task, cancelled_task in itertools.zip_longest(active_tasks, cls.cancelling, cancelled_tasks):
                if active_task==None:
                    active_task=  ""
                if cancelled_task== None:
                    cancelled_task = ""
                if cancelling_task ==None:
                    cancelling_task = ""

                yield f"{active_task:{longest_name}}{cancelling_task:{longest_name}}{cancelled_task:{longest_name}}"


        try:
            if target=="AsyncModuleManager":
                reference = cls
            #elif target in cls.inst:
            #    reference = cls.get_instance(target)
            
            print("\n")
            for line in status_report(reference):
                print(line)
            print("\n")
        except Exception as e:
            print("status report", e)


    @classmethod
    def run_forever(cls):
        pub.subscribe(cls.module_command_handler, "AsyncModuleManager")
        asyncio.get_event_loop().run_forever()

    @classmethod
    def stop_all(cls):
        for module in cls.inst:
            cls.destroy_module(module)







if __name__ == "__main__":
    class Something(Module):
        def __init__(self):
            self.var = 0
            pub.subscribe(self.handler , "topic")
            super().__init__()

        def something_operation(self, num1, num2):
            return num1 *num1 + num2 * num2
        
        def run(self):
            print(self.var)
            #print(self.inst)
            #self.var += 1

        @Module.asynconce
        async def run_test(self):
            while True:
                print("#@#@#@#@#@#@$@#@#@#@#@#@#@#@#")
                await asyncio.sleep(2)
                print(len(asyncio.all_tasks()))

        @Module.asyncloop(0.2)
        async def run2(self):
            pass
            #print("######################################")
            #await self.test()



        def handler(self, var):
            self.var = var

        def destroy(self):
            print("Something destroyed")





    class Something2(Module):
        def __init__(self):
            self.var = 0
            super().__init__()

        @Module.asyncloop(1)
        async def run_async_increment(self):
            self.var +=1
            #print(self.tasks)

        @Module.threadloop(10)
        def run_thread_pub(self):
            pub.sendMessage("topic", var = self.var)
            #self.test(self.run1)

        @Module.threadonce
        def run_thread_once(self):
            print("Something2 thread run_once")

        def cancel_run_thread_pub(self):
            print("Something2.run_thread_pub cancel cleanup done")

        def cancel_run(self):
            print("Something2.run cancel cleanup done")

        def run_once(self):
            print("SOMETHING2.RUN_ONCE")

        def destroy(self):
            print("Something2 destroyed")
    

    class EXIT(Module):
        def __init__(self):
            self.cancelled_counter = 0
            super().__init__()

        @Module.loop()
        def run(self):
            pass

        @Module.loop(0.2)
        def run_exit(self):
            if self.cancelled_counter < 1:
                try:
                    #pub.sendMessage("AsyncModuleManager", target = "Something2", command = "cancel")
                    pub.sendMessage("AsyncModuleManager", target = "Something.run2", command = "cancel")
                    #pub.sendMessage("AsyncModuleManager", target = "Something2.run", command = "cancel")
                    
                    
                    print("cancelled")
                    print("len", len(asyncio.Task.all_tasks()))
                    
                except Exception as e:
                    print(e)
                #print("exiting")
                #exit()
            elif self.cancelled_counter==2:
                print("STARTED")
                pub.sendMessage("AsyncModuleManager", target = "Something2", command = "start")
            self.cancelled_counter +=1
            pub.sendMessage("AsyncModuleManager", target = "AsyncModuleManager", command = "status")

        @Module.loop(0.15)
        def run_start(self):
            #pub.sendMessage("AsyncModuleManager", target = "Something2.run1", command = "start")
            #pub.sendMessage("AsyncModuleManager", target = "Something.run2", command = "start")
            #pub.sendMessage("AsyncModuleManager", target = "Something2.run", command = "start")
            
            pub.sendMessage("AsyncModuleManager", target = "Something2", command = "cancel")
            #pub.sendMessage("AsyncModuleManager", target = "AsyncModuleManager", command = "status")
            #print("restarted")
            print("len", len(asyncio.Task.all_tasks()))

        def destroy(self):
            print("EXIT destroyed")



    s = Something()
    s2 = Something2()
    Exit = EXIT()
    s.start(1)
    s2.start(1)
    Exit.start(1)
    AsyncModuleManager.register_modules(s, s2, Exit)

    try:
        AsyncModuleManager.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        print(type(e), e)
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()



