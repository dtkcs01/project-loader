import os
import json
import urllib

class Live_Loader(object):
    """docstring for Live_Loader."""

    def __init__(self, url):
        super(Live_Loader, self).__init__()
        self.decode_url(url)
        self._data = {
            'folders': {},
            'files': {}
        }
        self._data_size_units = [
            'bytes',
            'kB',
            'MB',
            'GB',
            'TB',
            'PB',
            'EB',
            'ZB',
            'YB'
        ]

    def decode_url(self, url):
        url = urllib.parse.urlparse(url)
        self._dirs = list(filter(lambda x: len(x) > 0, url.path.split('/')))[1: ]
        self._location = os.path.join(os.path.abspath(os.sep), *self._dirs)

    def build_url(self, name):
        if(name == '..'):
            return '/d/{}'.format('/'.join(self._dirs[: -1]))
        else:
            return '/d/{}/{}'.format('/'.join(self._dirs), name)

    def normalize_size(self, bytes):
        i = 0
        while(bytes//1024 > 0):
            bytes = bytes//1024
            i += 1
        return '{} {}'.format(bytes, self._data_size_units[i])

    def load_dirs(self, dirs):
        current = { 'folders': {}, 'files': {} }
        for dir in dirs:
            abs_path = os.path.abspath(os.path.join(self._location, dir))
            tmp = { 'url': self.build_url(dir) }
            if(os.path.isfile(abs_path)):
                tmp['type'] = 'file'
                tmp['size'] = self.normalize_size(os.path.getsize(abs_path))
                current['files'][dir] = tmp
            else:
                tmp['type'] = 'folder'
                current['folders'][dir] = tmp
        return current

    def detect_change(self, type, current):
        added = { k: v for k, v in current.items() if k not in self._data[type] }
        removed = { k: v for k, v in self._data[type].items() if k not in current }
        changed = {}
        if(type == 'files'):
            def condition(k, v):
                if(k in self._data[type]):
                    if(not v['size'] == self._data[type][k]['size']):
                        return True
                return False
            changed = { k: v for k, v in current.items() if condition(k, v) }
        return (added, removed, changed)

    def load(self):
        dirs = os.listdir(self._location)
        dirs.append('..')
        dirs.sort()
        current = self.load_dirs(dirs)
        packet = { 'folders': [], 'files': [] }
        for type in self._data:
            (added, removed, changed) = self.detect_change(type, current[type])
            packet[type] += [ (k, 1, v) for k, v in added.items() ]
            packet[type] += [ (k, 0, v) for k, v in changed.items() ]
            packet[type] += [ (k, -1, v) for k, v in removed.items() ]
            packet[type].sort()
        self._data = current
        return json.dumps(packet) if(packet['files'] or packet['folders']) else False

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_location):
        self._location = new_location
