import os
import lark
from pprint import pprint
from analyser.grammers import main

parser = main()
def explore(location):
    if(os.path.isfile(location)):
        if(location[-2:] == 'py'):
            print(' {} : [ "{}" ]'.format(os.path.basename(location), location))
            imports = parser.parse(open(location, 'r').read()).children[0].children
            for obj in imports:
                print('\t- ', build(obj))
    else:
        for c in os.listdir(location):
            explore(os.path.join(location, c))
def build(import_object):
    module = []
    for child in import_object.children:
        if(isinstance(child, lark.Tree)):
            if(child.data == 'id_seq'):
                module.append(build(child))
            elif(child.data == 'id_dot'):
                module.append(build(child))
        elif(isinstance(child, lark.lexer.Token) and child.type == 'ID'):
            module.append(child.value)
    return '.'.join(module)

explore(os.getcwd())
