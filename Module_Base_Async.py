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
        self.destroyed = False
        self.relative_speed_multiplier = {}   # {"Test.run": [<function Test.test at 0x...>, 10]}
        self.tasks = {}                       # {"Test.run": <Task pending coro=...>"}
        self.inst = {}                        # {"Test" : <__main__.test object at 0x...>}
        #pub.subscribe(self.cancel_task_handler, self.__class__.__name__)
    
    async def exec_periodically(self, wait_time, func):
        while True:
            await asyncio.sleep(wait_time)
            func(self)


    @staticmethod
    def loop(speed_multiplier):
        def loop(func):
            def wrapper(varclass, record_name, interval):
                varclass.relative_speed_multiplier[record_name] = [func, speed_multiplier]
                varclass.tasks[record_name] = asyncio.ensure_future(varclass.exec_periodically((1/varclass.relative_speed_multiplier[record_name][1])*(1/interval), varclass.relative_speed_multiplier[record_name][0]))
            return wrapper
        return loop

    def start(self, interval):
        self.run_funcs = [method for method in dir(self) if method[:3]=="run" and callable(getattr(self, method))]
        for func_name in self.run_funcs:
            record_name = str(self.__class__.__name__)+"."+func_name
            try:
                exec(f"self.{func_name}('{record_name}', {interval})")
                #self.tasks[record_name] = asyncio.ensure_future(self.exec_periodically((1/self.relative_speed_multiplier[record_name][1])*(1/interval), self.relative_speed_multiplier[record_name][0]))
            except:
                exec(f"self.{func_name}()")
            finally:
                self.inst[self.__class__.__name__] = self.__class__
            #self.tasks[record_name] = asyncio.ensure_future(self.schedule_task_periodically((1/self.relative_speed_multiplier[record_name][1])*(1/interval), self.relative_speed_multiplier[record_name][0]))
            
    def destroy(self):
        pass


    @staticmethod
    def start_loop():
        return asyncio.get_event_loop()

    '''
    def cancel_local_task(self, task, check_clean_up = True):
        if "." not in task:
            task = self.__class__.__name__+"."+task

        
        if not self.tasks[task].cancelled:
            self.tasks[task].cancel()
        else:
            self.tasks[task] = None

        if check_clean_up:
            if False not in [task.cancelled() for task in self.tasks.values()]:
                self.destroy()
                self.destroyed = True

        
    def cancel_all_local_task(self):
        for record_name in self.tasks:
            self.cancel_local_task(record_name, check_clean_up=False)
        if not self.destroyed:
            self.destroy()
            self.destroyed = True

    def cancel_all_global_task(self, class_name):
        pub.sendMessage(class_name, task = class_name)

    def cancel_global_task(self, task):
        pub.sendMessage(task[:task.find(".")], task = task)

    def cancel_task_handler(self, task):
        if "." in task:
            self.cancel_local_task(task)
        else:
            self.cancel_all_local_task()'''




class AsyncModuleManager(Module):
    def __init__(self):
        pub.subscribe(self.async_module_manager_handler, self.__class__.__name__)
        super().__init__()

    def run(self):
        print("manager")

    def async_module_manager_handler(self, target, command):
        pass

    def accept_modules(self, *args):
        try:
            for module in args:
                self.inst.update(module.inst)
                self.tasks.update(module.tasks)
                self.relative_speed_multiplier.update(module.relative_speed_multiplier)
            print(self.inst)
            print(self.tasks)
            print(self.relative_speed_multiplier)
        except:
            print("Must provide Modules as arguments")

    def get_instance(self, method_name):
        return self.inst[method_name[:method_name.find(".")]]   
    

    def start_task(self):
        pass
    
    def cancel_task(self, method_name):   
        varclass = self.get_instance(method_name)  
        if not self.tasks[method_name].cancelled:
            self.tasks[method_name].cancel()

        if False not in [task.cancelled() for task in self.tasks.values()]:
            varclass.destroy()
            varclass.destroyed = True

    def restart_module(self):
        pass
    
    def destroy_module(self):
        pass










if __name__ == "__main__":
    class Something(Module):
        def __init__(self):
            self.var = 0
            pub.subscribe(self.handler , "topic")
            super().__init__()

        def something_operation(self, num1, num2):
            return num1 *num1 + num2 * num2
        
        @Module.loop(1)
        def run(self):
            print(self.var)
            #self.var += 1

        @Module.loop(0.1)
        def run2(self):
            print("cancel")
            #self.cancel_all_global_task("Something2")
            #self.cancel_local_task("run")
            #self.cancel_local_task("run2")


        def handler(self, var):
            self.var = var

        def destroy(self):
            pass





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

        def destroy(self):
            pass

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
            pass
            #print("exiting")
            #exit()



    manager = AsyncModuleManager()
    s = Something()
    s2 = Something2()
    Exit = EXIT()
    loop = Module.start_loop()
    manager.start(0.0000000001)
    s.start(1)
    s2.start(1)
    Exit.start(1)
    manager.accept_modules(s, s2, Exit)
    

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except BaseException:
        pass
    finally:
        print("Closing Loop")
        loop.close()


