class Analyse_Base(object):
    """docstring for Analyse_Base."""

    def __init__(self, name, location):
        super(Analyse_Base, self).__init__()
        self.name = name
        self.location = location
        self.watch = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, nname):
        self._name = nname

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, nlocation):
        self._location = nlocation

    @property
    def watch(self):
        return self._watch

    @watch.setter
    def watch(self, nwatch):
        self._watch = nwatch
