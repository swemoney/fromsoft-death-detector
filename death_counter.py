import time
from os.path import exists as file_exists

COOLDOWN = 4

class DeathCounter:
    def __init__(self, filename):
        self.filename = filename
        self.count = self.count_from_file
        self.last_inc = time.time()

    @property
    def count_from_file(self):
        if file_exists(self.filename):
            with open(self.filename, 'r') as f:
                return int(f.read())
        return 0

    @property
    def on_cooldown(self):
        time_since_inc = time.time() - self.last_inc
        return time_since_inc < COOLDOWN

    def inc_counter(self):
        self.last_inc = time.time()
        self.count = self.count_from_file
        self.count += 1
        self.write_to_file(f"{self.count}")

    def write_to_file(self, to_write):
        with open(self.filename, 'w') as f:
            f.write(to_write)
