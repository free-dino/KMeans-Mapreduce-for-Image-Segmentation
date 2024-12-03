#!/usr/bin/env python3
import sys
import numpy as np
from data_prep import kmeans_plus_plus, kmeans

def process_image(image_name, points):
    """
    Performs KMeans clustering on points.
    Outputs: <image_name>\t<centroid_values>.
    """
    k = 3  # Number of clusters
    points_array = np.array(points)

    # Run KMeans++
    initial_centroids = kmeans_plus_plus(points_array, k)
    _, centroids = kmeans(points_array, initial_centroids)

    # Output centroids in the desired format
    for centroid in centroids:
        centroid_values = ' '.join(map(str, centroid))
        print(f"{image_name}\t{centroid_values}")

if __name__ == '__main__':
    current_image = None
    points = []

    # Read input from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            # Parse mapper output into image_name and points
            image_name, point_str = line.split('\t')
            point = list(map(float, point_str.split()))

            # If the image_name changes, process the previous one
            if current_image and image_name != current_image:
                print(f"Processing image: {current_image}")  # Debugging line
                process_image(current_image, points)
                points = []  # Reset points for the new image

            current_image = image_name
            points.append(point)
        except ValueError:
            # Handle cases where the line does not have the expected format
            print(f"Skipping invalid line: {line}")  # Debugging line
            continue

    # Process the last image
    if current_image:
        print(f"Processing final image: {current_image}")  # Debugging line
        process_image(current_image, points)

