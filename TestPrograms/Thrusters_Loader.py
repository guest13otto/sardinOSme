import yaml
from pubsub import pub
from Module_Base import Module

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
                        args = args + f"{key} = {value},"
                    else:
                        args = args + f"{key} = '{value}',"

                try:
                    if args[-1] == ',':
                        args = args[:-1]
                except IndexError:
                    pass

                exec(f"from {file} import {varclass}")
                _node = varclass + "(" + args + ")"
                print(_node)
                _node = eval(varclass + "(" + args + ")")
                print(f"{file} is running")
                nodes.append({"node": _node, "class": varclass, "frequency": frequency, "args": args})




        except FileNotFoundError:
            print("File not found error")
            #pub.sendMessage("log.ThrusterLoader.error", message = FileNotFoundError)
        return nodes

class __Test_Case_Send__(Module):
    def run(self):
        pub.sendMessage("command.movement", message = (0,1,0,0,0,0))

if __name__ == "__main__":
    #def logger_ThrusterLoader_error(message):
        #print("File not found: ", message)

    Loader = Loader()
    nodes = Loader.load_all("Thruster.yaml")

    for n in nodes:
        n["node"].start(n["frequency"])

    test_case_send = __Test_Case_Send__()
    test_case_send.start(1)

    #pub.subscribe(logger_ThrusterLoader_error, "log.ThrusterLoader.error")
