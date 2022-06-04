from death_detector import DeathDetector, GameType
from death_counter import DeathCounter
from config import Config
from fps import FPS
import cv2 as cv
import time

# This is the script I use on my Twitch stream to detect deaths in Elden Ring 
# and update a text file so OBS can display it. The bulk of the work is done
# in the death_detector and death_counter modules so you can create your own
# script using those pieces if you'd like, or tailor this script to your needs.

DEBUG_WINDOW_NAME = "FromSoft Death Detector Preview"

settings = Config("settings.json")
counter = DeathCounter(filename=settings.output_filename)
last_close_match = time.time()
fps = FPS(60)

import os
os.system('title FromSoft Death Counter')
if settings.resize_console:
    os.system('mode con: cols=40 lines=3')

def main():
    print("")
    detector = DeathDetector(
        game_type=GameType.ELDENRING,
        monitor=settings.monitor)
    detector.add_death_detected_observer(death_detected)
    detector.add_frame_complete_observer(frame_complete)
    detector.add_close_detected_observer(close_detected)

    setup_preview_window()
    detector.start()

def frame_complete(frame, confidence):
    update_preview_window(frame)
    print_progress(fps(), confidence)

def death_detected(frame, confidence):
    if counter.on_cooldown == False:
        counter.inc_counter()
        update_preview_window(frame)
        save_frame(frame, confidence)
    print_progress(fps(), confidence)

def close_detected(frame, confidence):
    global last_close_match
    if time.time() - last_close_match > 4:
        last_close_match = time.time()
        save_frame(frame, confidence, "close")
    update_preview_window(frame)
    print_progress(fps(), confidence)

def setup_preview_window():
    if settings.debug.preview_window:
        cv.startWindowThread()
        cv.namedWindow(DEBUG_WINDOW_NAME)

def update_preview_window(frame):
    if settings.debug.preview_window:
        cv.imshow(DEBUG_WINDOW_NAME, frame)
        cv.waitKey(1)

def save_frame(frame, confidence, path="match"):
    if settings.debug.save_death_image:
        t = time.strftime("%H_%M_%S", time.localtime())
        filename = f"{t}-{(confidence*100):0.2f}.png"
        cv.imwrite(f"debug/{path}/{filename}", frame)

def color(clr, bright=True):
    colors = ["black","red","green","yellow","blue","violet","beige","white"]
    return f"\33[{9 if bright else 3}{colors.index(clr)}m"

def print_progress(fps, c):
    s = f"  {''.join([dot(d,c) for d in range(0,9)])} " # Print the array of dots
    s += f"{color('white')}{c*100:0.2f}%".ljust(12)     # Print the confidence
    s += f"{color('black')}{fps:0.1f}fps     {color('green') if counter.on_cooldown else color('white',False)}{counter.count}".rjust(29) # Print FPS and death counter
    print(f"{s}\033[?25l", end="\r")                    # Hide the cursor and go back to the beginning of the line

def dot(dot_num, confidence=0):
    colors = [color('red',False), color('red',False), color('red'), color('yellow',False), color('yellow'), color('green',False), color('green'), color('blue',False), color('blue'), color('violet')]
    s = colors[dot_num] if confidence > dot_num / 10 else color('black')
    return f"{s}•"

if __name__ == "__main__":
    main()