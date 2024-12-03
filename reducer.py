#!/usr/bin/env python3
import sys
import numpy as np
from data_prep import kmeans_plus_plus, kmeans  # Import your existing functions

def process_image(points_file):
    # Load points from file
    data = np.loadtxt(points_file)

    # Perform K-Means++ initialization and clustering
    k = 5  # Number of clusters; can be adjusted
    initial_centroids = kmeans_plus_plus(data, k)
    labels, centers = kmeans(data, initial_centroids)

    # Save clusters to a new file
    output_file = points_file.replace('.txt', '_clusters.txt')
    with open(output_file, 'w') as f:
        for point, label in zip(data, labels):
            f.write(f"{point[0]} {point[1]} {point[2]} {int(label)}\n")

    print(f"{output_file} created.")

if __name__ == '__main__':
    for line in sys.stdin:  # Read .txt paths from stdin
        process_image(line.strip())
