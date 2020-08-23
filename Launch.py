from Module_Loader import Loader
import sys

config_name = "config.yaml"

if len(sys.argv) > 1:
    config_name = sys.argv[1]

nodes = Loader.load_all(config_name)

for n in nodes:
    n["node"].start(n["frequency"])
