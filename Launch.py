from Module_Loader import Loader
import sys
from Module_Base_Async import AsyncModuleManager

AsyncModuleManager = AsyncModuleManager()
config_name = "config.yaml"

if len(sys.argv) > 1:
    config_name = sys.argv[1]

nodes = Loader.load_all(config_name)

for n in nodes:
    n["node"].start(n["frequency"])
    AsyncModuleManager.register_module(n["node"])

try:
    AsyncModuleManager.run_forever()
except KeyboardInterrupt:
    pass
except BaseException:
    pass
finally:
    print("Closing Loop")
    AsyncModuleManager.stop_all()
