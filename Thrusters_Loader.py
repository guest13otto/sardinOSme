import yaml
from pubsub import pub

class Loader():
    def load_all(self, YAML_File):
        nodes = []
        try:
            content = yaml.load(open(str(YAML_File), 'r'), Loader = yaml.FullLoader)
            for nodeName in content:
                args = ""
                moduleName = content[nodeName]

                for key,value in moduleName.items():

                    if key == "file":
                        file = value
                    elif key == "varclass":
                        varclass = value
                    elif key == "frequency":
                        frequency = value
                    elif key[:8] == "Thruster":
                        args = args + f"{key} = {value}"
                    else:
                        args = args + f"{key}={value},"

                try:
                    if args[-1] == ',':
                        args = args[:-1]
                except IndexError:
                    pass

                exec(f"from {file} import {varclass}")
                _node = eval(varclass + "(" + args + ")")
                nodes.append({"node": _node, "class": varclass, "frequency": frequency, "args": args})




        except FileNotFoundError:
            print("File not found error")
            #pub.sendMessage("log.ThrusterLoader.error", message = FileNotFoundError)
        return nodes

if __name__ == "__main__":
    #def logger_ThrusterLoader_error(message):
        #print("File not found: ", message)

    Loader = Loader()
    nodes = Loader.load_all("Thruster.yaml")

    for n in nodes:
        n["node"].start(n["frequency"])

    #pub.subscribe(logger_ThrusterLoader_error, "log.ThrusterLoader.error")
