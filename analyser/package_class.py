import os
import sys
from gitignore_parser import parse_gitignore

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base_class import Analyse_Base

class Package_Class(Analyse_Base):
    """docstring for Package_Class."""
    gitignores = []

    def __init__(self, name, location):
        super(Package_Class, self).__init__(name, location)
        self.load_contents()
        self.load_gitignore()

    def load_contents(self): # TODO: add try-except
        out = {}
        contents = os.listdir(self.location)
        for content in contents:
            abs_path = os.path.join(self.location, content)
            if(os.path.isdir(abs_path)): out[content] = Package_Class(content, abs_path)
            else: out[content] = Analyse_Base(content, abs_path)
        self._contents = out

    def load_gitignore(self):
        if('.gitignore' in self._contents):
            path = self._contents['.gitignore'].location
            Package_Class.add_gitignore(parse_gitignore(path))

    @classmethod
    def add_gitignore(self, parser):
        Package_Class.gitignores.append(parser)

    def clean_package(self):
        for parser in Package_Class.gitignores:
            if(parser(self._location) or self._name == '.git'):
                self._contents = {}
        for k, v in self._contents.items():
            if(isinstance(v, Package_Class)):
                v.clean_package()

    def display(self):
        print('\n - {} [{}]'.format(self.name, self.location))
        for k, v in self._contents.items():
            if(isinstance(v, Package_Class)):
                v.display()
        print()
