from Module_Base import ModuleManager

mm = ModuleManager("config.yaml")#, (400, 400))
mm.start(1)
mm.register_all()
mm.start_all()
try:
    mm.run_forever()
    #AsyncModuleManager.run_forever()
except KeyboardInterrupt:
    pass
except BaseException:
    pass
finally:
    print("Closing Loop")
