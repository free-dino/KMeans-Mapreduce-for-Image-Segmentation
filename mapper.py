#!/usr/bin/env python3
import sys
import cv2
import numpy as np
import os

def image_to_points(image_path):
    img = cv2.imread(image_path)
    data = img.reshape((-1, 3)).astype(np.float32) / 255.0  # Normalize pixels

    # Generate output file name (replace extension)
    img_name = os.path.basename(image_path).split('.')[0]  # Extract name without extension
    output_file = f"{img_name}.txt"

    # Save points to a text file
    with open(output_file, 'w') as f:
        for point in data:
            f.write(f"{point[0]} {point[1]} {point[2]}\n")

    print(f"{output_file} created.")  # Log creation

if __name__ == '__main__':
    for line in sys.stdin:  # Read image paths from stdin
        image_to_points(line.strip())
