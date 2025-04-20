from rgbmatrix import RGBMatrix, RGBMatrixOptions
import configparser
import os
import inspect
import math
import time
import sys
import logging
from PIL import Image, ImageDraw

img = Image.open("temp_album.png")
resized_img = img.resize((64, 64), resample=Image.LANCZOS)

frame = Image.new("RGB", (64, 64), (0, 0, 0))
draw = ImageDraw.Draw(frame)

frame.paste(resized_img, (0, 0))

# get config
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(currentdir + "/rpi-rgb-led-matrix/bindings/python")

config = configparser.ConfigParser()
parsed_configs = config.read('../config.ini')

if len(parsed_configs) == 0:
    logging.info("no config file found")
    sys.exit()

config = configparser.ConfigParser()

options = RGBMatrixOptions()
options.hardware_mapping = config.get('Matrix', 'hardware_mapping', fallback='regular')
options.rows = 64
options.cols = 64
options.brightness = config.getint('Matrix', 'brightness', fallback=100)
options.gpio_slowdown = config.getint('Matrix', 'gpio_slowdown', fallback=1)
options.limit_refresh_rate_hz = config.getint('Matrix', 'limit_refresh_rate_hz', fallback=0)
options.drop_privileges = False
matrix = RGBMatrix(options=options)

shutdown_delay = config.getint('Matrix', 'shutdown_delay', fallback=600)
black_screen = Image.new("RGB", (64, 64), (0, 0, 0))
last_active_time = math.floor(time.time())

matrix.SetImage(frame)
