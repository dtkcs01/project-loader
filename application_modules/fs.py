import os
import pathlib

class File_System(object):
    """docstring for File_System."""

    def __init__(self):
        super(File_System, self).__init__()
        self._size_units = units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']

    def explore(self, location):
        if(os.path.isfile(location)):
            return self.explore_file(location)
        else:
            return self.explore_folder(location)

    def explore_file(self, location):
        size = self.normalize_size(os.path.getsize(location))
        with open(location, 'r') as source:
            data = [ line.strip() for line in source ]
            source.close()
        return {
            'file_data': data,
            'size': size
        }

    def explore_folder(self, location):
        li = os.listdir(location)
        folders = []
        files = []
        for l in li:
            ap = os.path.join(location, l)
            if(os.path.isfile(ap)):
                size = self.normalize_size(os.path.getsize(ap))
                files.append({
                    'name': l,
                    'path': ap,
                    'size': size
                })
            else:
                folders.append({
                    'name': l,
                    'path': ap
                })
        return {
            'folders' : folders,
            'files' : files
        }

    def normalize_size(self, size):
        i = 0
        while size//1024 > 0:
            size = size//1024
            i += 1
        return '{} {}'.format(size, self._size_units[i])

    def add_clean_session_id(self, id, session_id):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cleaner.txt'), 'a') as file:
            file.write('\n{} {}'.format(id, session_id))
            file.close()
