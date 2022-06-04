import json
from types import SimpleNamespace
from os.path import exists as file_exists

DEFAULT_CONFIG = {
    "output_filename": "C:\\Users\\username\\Documents\\deaths.txt",
    "monitor": 1,
    "resize_console": False,
    "debug": {
        "preview_window": False,
        "save_death_image": False
    }
}

class Config:
    def __init__(self, filename):
        if file_exists(filename):
            self.config = self.read_file(filename)
        else:
            self.config = DEFAULT_CONFIG
            self.write_file(filename)

    def read_file(self, filename):
        with open(filename) as f:
            return json.load(f, object_hook=lambda x: SimpleNamespace(**x))

    def write_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=4)

    def __getattr__(self, name):
        return getattr(self.config, name)
