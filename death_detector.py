from config import Config
from functools import cached_property
from enum import Enum
from mss import mss
import time
import cv2 as cv
import numpy as np

# Shades of red we're looking for
LOWER_RED1 = (0, 67, 80)
UPPER_RED1 = (5, 255, 255)
LOWER_RED2 = (170, 67, 80)
UPPER_RED2 = (180, 255, 255)

# After a death is detected, don't really do anything for
# this amount of time (seconds) so we don't detect the same
# death again.
COOLDOWN = 4

class GameType(Enum):
    DARKSOULS = 1
    SEKIRO = 2
    ELDENRING = 3

class DeathDetector:
    def __init__(self, game_type, monitor = 1):
        with mss() as screen_capture:
            self.capture = screen_capture

        self.game_type = game_type
        self.monitor_num = monitor
        self.monitor = self.capture.monitors[self.monitor_num]
        self.gamedata = Config(f"games/{game_type.name.lower()}.json")
        self.template = cv.imread(f"templates/{game_type.name.lower()}_{self._screen_size_string}.png", 0)

        # Observers to call back to
        self._frame_complete_observers = []
        self._death_detected_observers = []
        self._close_detected_observers = []

    def start(self):
        while "Capturing Screen":
            frame, frame_mask = self._get_screen_mask()
            res = cv.matchTemplate(frame_mask, self.template, cv.TM_CCOEFF_NORMED)
            _, conf, loc, _ = cv.minMaxLoc(res)
            
            if conf > self.gamedata.confidence:
                self._notify_death_detected(frame_mask, conf)
            elif conf > self.gamedata.close:
                self._notify_close_detected(frame_mask, conf)
            else:
                self._notify_frame_complete(frame, conf)

    @property
    def _screen_size_string(self):
        return f"{self.monitor['width']}x{self.monitor['height']}"

    def _get_screen_mask(self):
        box = self.gamedata.capture_frame.__dict__[self._screen_size_string]
        mon = {"top": box.top, "left": box.left, "width": box.width, "height": box.height, "mon": self.monitor_num}
        frame = np.array( self.capture.grab(mon) )
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        frame_mask1 = cv.inRange(frame_hsv, LOWER_RED1, UPPER_RED1)
        frame_mask2 = cv.inRange(frame_hsv, LOWER_RED2, UPPER_RED2)
        frame_mask = frame_mask1 + frame_mask2
        return (frame, frame_mask)

    def add_frame_complete_observer(self, fn):
        self._frame_complete_observers.append(fn)

    def add_death_detected_observer(self, fn):
        self._death_detected_observers.append(fn)

    def add_close_detected_observer(self, fn):
        self._close_detected_observers.append(fn)

    def _notify_frame_complete(self, frame, conf):
        for observer in self._frame_complete_observers:
            observer(frame, conf)

    def _notify_death_detected(self, frame, conf):
        for observer in self._death_detected_observers:
            observer(frame, conf)

    def _notify_close_detected(self, frame, conf):
        for observer in self._close_detected_observers:
            observer(frame, conf)
