# -*- encoding: utf-8 -*-

"""feather.py

Streams video from the webcam using OpenCV and converts the video stream to
black and white to determine brightness.
"""

import curses
import cv2
import os
import sys


def log(text):
    text = str(text)

    with open("log.txt", "w+") as f:
        f.write(text)


# Returns the number of rows and columns of characters
def get_winsize():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def pixel_to_char(pixel):
    ramp = '  .:-=+*#%@'
    brightness = pixel/255.0
    ramp_index = int(len(ramp)*brightness)
    return ramp[ramp_index]


def main(arg):

    # Initialize curses
    curses.initscr()
    curses.curs_set(0)
    curses.use_default_colors()

    # Create the window
    rows, columns = get_winsize()
    rows, columns = int(rows), int(columns)
    win = curses.newwin(rows, columns, 0, 0)

    # Initialize the capture device
    cap = cv2.VideoCapture(0)
    win.refresh()

    # Get the initial compression_factor
    ret, img = cap.read()
    compression_factor = max(len(img)/rows, len(img[0])/columns)
    compression_factor = int(compression_factor)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('~/Desktop/output.avi',fourcc, 20.0, (640,480))

    # Function for drawing the image as characters
    def draw(img):
        output_rows = len(img)/compression_factor
        output_cols = len(img[0])/compression_factor
        padding_rows = (rows - output_rows) / 2
        padding_cols = (columns - output_cols) / 2
        for row in range(output_rows):
            for col in range(output_cols):
                if curses.is_term_resized(rows, columns):
                    return
                try:
                    pixel = img[row * compression_factor][col * compression_factor]
                    char = pixel_to_char(pixel)
                    win.addch(row + padding_rows, col + padding_cols, char)
                except:
                    # win.addch() causes an exception if we try to draw beyond
                    # the boundaries of the window. We can just ignore it.
                    pass
    
    
    # Loop forever, handling terminal resizes
    while(cap.isOpened()):
        ret, img = cap.read()
        
        draw(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

        if curses.is_term_resized(rows, columns):
            rows, columns = get_winsize() 
            win = curses.newwin(rows, columns, 0, 0)
            compression_factor = max(len(img)/rows, len(img[0])/columns)
        win.refresh()

# Ensure curses is cleaned up correctly
curses.wrapper(main)

