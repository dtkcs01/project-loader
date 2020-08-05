import os
from lark import Lark
def main():
    grammer = get_grammer()
    return Lark(grammer, parser = 'lalr', debug = True)
def get_grammer():
    python = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'python')
    grammers = os.listdir(python)
    return '\n'.join(open(os.path.join(python, grammer), 'r').read() for grammer in grammers)
