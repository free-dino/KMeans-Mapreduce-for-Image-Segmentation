#!/usr/bin/env python3
import sys
import os

def process_line(line, image_name):
    """
    Process each line of data and output in <image_name>\t<point> format.
    """
    point_values = line.strip()  # Clean any surrounding whitespace
    print(f"{image_name}\t{point_values}")

if __name__ == '__main__':
    image_name = None
    
    # Read from stdin as Hadoop streaming passes input here
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        process_line(line, image_name)

