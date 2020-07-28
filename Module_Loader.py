import yaml

class Loader(): 
    def load_all(YAML_File):
        nodes = []
        try:
            content = yaml.load(open(str(YAML_File), 'r'), Loader = yaml.FullLoader)
            frequency = 1
            for nodeName in content:
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

