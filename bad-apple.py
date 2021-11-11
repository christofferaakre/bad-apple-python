#!/usr/bin/env python3

import numpy as np
from PIL import Image
import subprocess
import os
import time

video_length = 3 * 60 + 39

files = sorted(os.listdir('frames'))
number_of_frames = len(files)

fps = int(number_of_frames / video_length)
frame_duration = 1 / fps
size = 32

char_ramp = " .:-=+*#%@"
#char_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

columns, rows = os.get_terminal_size(0)

@np.vectorize
def brightness_to_char(brightness: int) -> str:
    brightness_rank = max(0, int(brightness / 255 * len(char_ramp)) - 1)
    return char_ramp[brightness_rank]

def print_image_as_ascii(filename: str):
    try:
        image = Image.open(filename)
        width, height = image.size
        resized_height = int(rows)
        resized_width = int(width * resized_height / height)
        image = Image.open(filename).resize((resized_width, resized_height))

        pixels = np.asarray(image).T
        chars = brightness_to_char(pixels)

        string = ''
        for y in range(chars.shape[1]):
            for x in range(chars.shape[0]):
                string += chars[x][y]
            string += '\n'

        subprocess.run('clear')
        #subprocess.run(f'echo "{string}"', shell=True)
        for line in string.split('\n'):
            print(line.center(columns))

        print(filename.center(columns))
        time.sleep(frame_duration)
    except KeyboardInterrupt:
        exit
    except Exception as e:
        print(e)
        exit

for filename in files:
    print_image_as_ascii(f'frames/{filename}')
exit
