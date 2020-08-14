import asyncio
from pubsub import pub

'''
-----------------------------------------------------------------------
Modules define like this:
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

    def run(self):                            #Method called "run" specifically will loop by itself, with run speed multiplier of 1
        print("from test")

    def destroy(self):                        #Add this if there are any clean-up code that needs to run when Module is destroyed
        print("Closed")

-----------------------------------------------------------------------
Run Modules in main like this:

from Test import test                                                #Import the Module made above

test_object = test()
another_test = AnotherModule()         
test_object.start(10)                                                #10 represents 10 times per second
another_test.start(10)
AsyncModuleManager.register_modules(test_object, another_test)       #Must have this to work

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
Pub commands to AsyncModuleManager:
#Use within a Module

pub.sendMessage("AsyncModuleManager", target = "othertest", command = "destroy")           #Destroy a active Module
pub.sendMessage("AsyncModuleManager", target = "othertest", command = "restart")           #Restart a destroyed Module
pub.sendMessage("AsyncModuleManager", target = "othertest.somefunc", command = "cancel")   #Cancel a running task
pub.sendMessage("AsyncModuleManager", target = "othertest.somefunc", command = "start")    #Start a cancelled task
-----------------------------------------------------------------------
'''

class Module():
    def __init__(self):
        self.destroyed = False
        self.relative_speed_multiplier = {}   # {"Test.run": [<function Test.test at 0x...>, 10]}
        self.tasks = {}                       # {"Test.run": <Task pending coro=...>"}
        self.inst = {}                        # {"Test" : <__main__.test object at 0x...>}
        #pub.subscribe(self.cancel_task_handler, self.__class__.__name__)
    
    async def exec_periodically(self, wait_time, func, special_run = False):
        while True:
            await asyncio.sleep(wait_time)
            if special_run:
                func()
            else:
                func(self)





    @staticmethod
    def loop(speed_multiplier = 1):
        def outer(func):
            def wrapper(varclass, record_name, interval):
                varclass.relative_speed_multiplier[record_name] = [func, speed_multiplier]
                varclass.tasks[record_name] = asyncio.ensure_future(varclass.exec_periodically((1/varclass.relative_speed_multiplier[record_name][1])*(1/interval), func))
            return wrapper
        return outer

    def task_cleanup(self, task_name):
        cancel_task_name = "cancel_"+task_name[task_name.find(".")+1:]
        if hasattr(self, cancel_task_name):
            getattr(self, cancel_task_name)()

    def create_task(self, func_name, record_name, interval):
        try:
            getattr(self, func_name)(record_name, interval)
        except:
            if func_name == "run":
                self.relative_speed_multiplier[record_name] = [getattr(self, "run"), 1]
                self.tasks[record_name] = asyncio.ensure_future(self.exec_periodically(1/interval, getattr(self, "run"), special_run=True))
            else:
                getattr(self, func_name)()


    def start(self, interval):
        self.destroyed = False
        self.interval = interval
        self.run_funcs = [method for method in dir(self) if method[:3]=="run" and callable(getattr(self, method))]
        for func_name in self.run_funcs:
            run_record_name = str(self.__class__.__name__)+"."+func_name
            self.create_task(func_name, run_record_name, interval)
                
        self.inst[self.__class__.__name__] = self

                       
    def destroy(self):
        pass


class AsyncModuleManager():
    inst = {}
    relative_speed_multiplier = {}
    tasks = {}

    '''
    @classmethod
    def start(cls, *args):
        pub.subscribe(cls.module_command_handler, "AsyncModuleManager")
        for module, interval in args:
            module.start(interval)
            cls.register_module(module)'''

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
        except:
            raise TypeError("Must provide Modules as arguments")

    @classmethod
    def register_modules(cls, *args):
        for module in args:
            cls.register_module(module)

    @classmethod
    def update_manager(cls, module):
        cls.inst.update(module.inst)
        cls.tasks.update(module.tasks)
        cls.relative_speed_multiplier.update(module.relative_speed_multiplier)

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
            if varclass.tasks[task_name].cancelled():
                varclass.create_task(cls.get_method_name(task_name), task_name, varclass.interval)
                cls.update_manager(varclass)
    
    @classmethod
    def cancel_task(cls, method_name):   
        varclass = cls.get_instance(method_name)  

        if not varclass.tasks[method_name].cancelled():
            varclass.tasks[method_name].cancel()
            varclass.task_cleanup(method_name)
            cls.update_manager(varclass)

        if not varclass.destroyed:
            if False not in [task.cancelled() for task in varclass.tasks.values()]:
                varclass.destroy()
                varclass.destroyed = True

    @classmethod
    def restart_module(cls, module_name):
        varclass = cls.get_instance(module_name)
        if varclass.destroyed:
            varclass.start(varclass.interval)
            cls.update_manager(varclass)
    
    @classmethod
    def destroy_module(cls, module_name):
        varclass = cls.get_instance(module_name)

        for task_name, task in varclass.tasks.items():
            if not task.cancelled():
                task.cancel()
                varclass.task_cleanup(task_name)

        if not varclass.destroyed:
            varclass.destroy()
            varclass.destroyed = True

        cls.update_manager(varclass)

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

        @Module.loop(0.1)
        def run2(self):
            pass



        def handler(self, var):
            self.var = var

        def destroy(self):
            print("Something destroyed")





    class Something2(Module):
        def __init__(self):
            self.var = 0
            super().__init__()

        def run(self):
            self.var +=1
            #print(self.tasks)

        @Module.loop(10)
        def run2(self):
            pub.sendMessage("topic", var = self.var)
            #self.test(self.run1)

        def cancel_run2(self):
            print("Something2.run2 cancel cleanup done")

        def cancel_run(self):
            print("Something2.run cancel cleanup done")

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
            if self.cancelled_counter < 2:
                try:
                    #pub.sendMessage("AsyncModuleManager", target = "Something2.run", command = "cancel")
                    #pub.sendMessage("AsyncModuleManager", target = "Something2.run2", command = "cancel")
                    pub.sendMessage("AsyncModuleManager", target = "Something2.run2", command = "cancel")
                    print("cancelled")
                    print("len", len(asyncio.Task.all_tasks()))
                    self.cancelled_counter +=1
                except Exception as e:
                    print(e)
                #print("exiting")
                #exit()

        @Module.loop(0.15)
        def run_start(self):
            #pub.sendMessage("AsyncModuleManager", target = "Something2.run1", command = "start")
            #pub.sendMessage("AsyncModuleManager", target = "Something2.run2", command = "start")
            #pub.sendMessage("AsyncModuleManager", target = "Something2.run", command = "start")
            pub.sendMessage("AsyncModuleManager", target = "Something2.run2", command = "start")
            print("restarted")
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
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        AsyncModuleManager.stop_all()



