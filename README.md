# Motion Detection System

This program uses OpenCV library to detect motion through a camera feed. If motion is detected, the program will open a web page and a file on the system.


## Requirements

* Python 3
* OpenCV library
* configparser library

## Installation

1. Clone or download the repository.
2. Install the required libraries using pip: 

```pip install opencv-python configparser```

3. Edit `settings.ini` with the path to the file you want to open and the URL you want to open in your web browser.


## Usage

1. Run the `motion_detection.py` script from the command line.
2. The camera feed will open up in a new window.
3. The program will detect motion and open the file and URL specified in the `settings.ini` file.


## Configuration

You can customize the following parameters in the `settings.ini` file:

* `program` - The name of the program to run.
* `filepath` - The full path to the file to open.
* `url` - The URL to open in the web browser.
* `motion_threshold` - The minimum area (in pixels) for a contour to be considered as motion.
* `motion_delay` - The number of seconds to wait before detecting motion again.


## License

This project is licensed under the MIT License.
