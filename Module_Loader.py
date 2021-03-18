import yaml
import sys
import os

class Loader():
    @staticmethod
    def loadall(YAML_File):
        nodes = []
        try:
            content = yaml.load(open(str(YAML_File), 'r'), Loader = yaml.FullLoader)
            frequency = 1
            for nodeName in content:
                #Exceptions
                if nodeName == "Subfolders":
                    for folder in content[nodeName]:
                        currentdir = os.path.dirname(os.path.realpath(__file__))
                        sys.path.insert(0, os.path.join(currentdir, f"{folder}"))
                        print(f"{currentdir}/{folder} inserted to sys.path") 
                    continue
                args = ''
                moduleName = content[nodeName]
                for key in moduleName:
                    value = moduleName[key]

                    #Required
                    if key == 'file':
                        file = value
                    elif key == 'varclass':
                        varclass = value
                    elif key == 'frequency':
                        frequency = value
                    #Exceptions
                    elif key == 'gui':
                        pass
                    #Arguments
                    else:
                        args = args + f"{key}='{value}',"

                #Complete argument
                try:
                    if args[-1] == ',':
                        args = args[:-1]
                except IndexError:
                    pass

                #Execute one node
                exec(f"from {file} import {varclass}")
                _node = eval(varclass +"(" + args +")")
                nodes.append( { "node": _node, "class": varclass, "frequency": frequency, "args": args} )
                print(f"{nodeName} successfully loaded")
        except FileNotFoundError:
            print('File not found')
        return nodes
