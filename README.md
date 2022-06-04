# FromSoft Death Detector

A simple death detector for From Software games.

## Description

FromSoft Death Detector is a rather simple death detector for FromSoft games that watches your screen and incriments a counter in a specified filename. Currently, only Elden Ring is implemented (I don't own any of the other games right now) but the script has been designed to be easily extendable so it should be easy enough to add. Ultimately this was created for my Twitch stream and probably won't receive a lot of updates unless they're required for extra Twitch features. Feel free to hack away at it, though!

## Getting Started

### Dependencies

* Python 3.10 (could work on older versions of Python 3 but hasn't been tested)
  * mss
  * numpy
  * opencv

### Installing

* Clone this repo.
* `python -m pip3 install -r requirements.txt`

### Executing program

You can create your own death detector script using the `DeathDetector` and `DeathCounter` modules but the included `main.py` file should work out of the box.

`python main.py`

The first time you run the script, a default `settings.json` file will get created. You'll want to change things in that file to suit your needs. There's a good chance the script will crash the first time it's run so you can adjust the `output_filename`.

* `output_filename`: The filename to read and write the current count to. This should be a filename with nothing but a number in it. It should be created if it doesn't exist.
* `monitor`: The monitor number to watch.
* `resize_console`: Resize the console to fit the counter so it's nice and compact (sadly, Windows new Terminal doesn't support this right now)
* `debug.preview_window`: Show a preview window of what the screen reader is seeing. Useful for defining a newly supported resolution
* `save_death_image`: Save images to the `debug` directory when it detects a death (or detects something "close" to a death). Useful for checking confidence settings to avoid false positives or negatives.

## Help

Currently, 1080p and 1440p are supported for Elden Ring. If you wish to add support for another resolution or game, you'll need to do some trial and error to define the area on the screen for the script to search (searching the entire screen is much more resource intesive so defining an area just larger than the `You Died` text is what you want). The script will look for whatever resolution your monitor is in the `.json` file for the game you want to detect under the `capture_frame`. Then it will use the image in the `templates` folder named `{gamename}_{resolution_width}x{resolution_height}.png` to find a match. Use the existing settings and template files to help you add your own.

## Authors

swemoney
* [Twitch](https://twitch.tv/swemoney) 
* [Twitter](https://twitter.com/swemoney)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [jogeuncheol/Death_Counter](https://github.com/jogeuncheol/Death_Counter) Inspiration was drawn from this project. Check it out for a more fully featured (just works) version of this script.
