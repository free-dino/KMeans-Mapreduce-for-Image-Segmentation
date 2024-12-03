import os
import cv2
import numpy as np
from pathlib import Path

# Specify the source and destination directories
src_folder = 'dataset/image/2/'
dst_folder = 'input'

# Create the destination folder if it doesn't exist
Path(dst_folder).mkdir(parents=True, exist_ok=True)

def image_to_points(image_path):
    """
    Converts an image to a normalized points array.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: Could not read image {image_path}")
        return None
    data = img.reshape((-1, 3)).astype(np.float32) / 255.0  # Normalize to [0, 1]
    return data

def save_points_to_file(points, output_path):
    """
    Saves a points array to a text file.
    """
    with open(output_path, 'w') as f:
        f.write('\n'.join([' '.join(map(str, point)) for point in points]))

def process_images(src_folder, dst_folder):
    """
    Processes all images in the source folder and saves their points arrays.
    """
    for filename in os.listdir(src_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            src_path = os.path.join(src_folder, filename)
            dst_path = os.path.join(dst_folder, f"{Path(filename).stem}.txt")

            points = image_to_points(src_path)
            if points is not None:
                save_points_to_file(points, dst_path)
                print(f"Saved points for {filename} to {dst_path}")
            else:
                print(f"Skipped {filename} due to read error.")

# Run the processing
process_images(src_folder, dst_folder)
