import argparse
from os.path import join
from pathlib import Path

import cv2
import numpy as np
from scipy.spatial import distance

parser = argparse.ArgumentParser(
    description='This script creates points.txt and clusters.txt files for a given image.')

parser.add_argument('--src_img', type=str, help='Path to the source image.')
parser.add_argument('--dst_folder', type=str,
                    help='Directory in which points.txt and clusters.txt will be saved.')
parser.add_argument('--k_init_centroids', type=int,
                    help='Number of initial centroids to seed using KMeans++.', default=5)

args = parser.parse_args()


def nparray_to_str(X):
    to_save = '\n'.join([' '.join(str(X[i])[1:-1].split())
                        for i in range(len(X))])
    return to_save


def kmeans_plus_plus(data, k):
    # Randomly choose the first centroid
    centroids = [data[np.random.choice(range(len(data)))]]

    for _ in range(1, k):
        # Calculate squared distances from the closest centroid
        D2 = np.array(
            [min(np.linalg.norm(x - c) ** 2 for c in centroids) for x in data])

        D2_sum = D2.sum()
        if D2_sum > 0:
            probabilities = D2 / D2_sum
        else:
            # Default to uniform distribution if sum is zero
            probabilities = np.ones_like(D2) / len(D2)

        # Choose the next centroid based on the probabilities
        cumulative_probs = probabilities.cumsum()
        r = np.random.rand()
        next_centroid = data[np.searchsorted(cumulative_probs, r)]
        centroids.append(next_centroid)

    return np.array(centroids)


def kmeans(data, initial_centroids, max_iter=30):
    """
    KMeans clustering algorithm.
    """
    k = len(initial_centroids)
    n = data.shape[0]
    centers = initial_centroids.copy()
    labels = np.zeros(n, dtype=np.int32)

    for iteration in range(max_iter):
        # Assign each point to the nearest center
        for i in range(n):
            distances = np.linalg.norm(data[i] - centers, axis=1)
            labels[i] = np.argmin(distances)

        # Update centers
        new_centers = np.zeros_like(centers)
        for j in range(k):
            points = data[labels == j]
            if len(points) > 0:
                new_centers[j] = np.mean(points, axis=0)
            else:
                # Handle empty clusters (optional: reinitialize to random point)
                new_centers[j] = data[np.random.choice(len(data))]

        # Check for convergence
        if np.allclose(new_centers, centers):
            print(f"Converged at iteration {iteration}")
            break

        centers = new_centers

    return labels, centers



def main(src_img, dst_folder, k):
    # files to be created
    points_path = join(dst_folder, 'points.txt')
    clusters_path = join(dst_folder, 'clusters.txt')

    # create directory
    Path(dst_folder).mkdir(parents=True, exist_ok=True)

    # load and prepare data
    img = cv2.imread(src_img)
    br, kl, _ = img.shape
    data = img.reshape((-1, 3)).astype(np.float32) / \
        255.0  # Normalize to [0, 1]

    # Write points
    with open(points_path, 'w') as f:
        f.write(nparray_to_str(data))
    print(f'Points saved in: {points_path}')

    # Generate and save KMeans++ centroids
    initial_centroids = kmeans_plus_plus(data, k)
    labels, centers = kmeans(data, initial_centroids)

    # Reshape results for image display
    labels_img = labels.reshape((br, kl))
    centers = (centers * 255).astype(np.uint8)
    segmented_img = np.zeros_like(img)
    for i in range(br):
        for j in range(kl):
            segmented_img[i, j] = centers[int(labels_img[i, j])]

    # Save the segmented image
    segmented_img_path = join(dst_folder, 'segmented_image.png')
    cv2.imwrite(segmented_img_path, segmented_img)
    print(f'Segmented image saved at: {segmented_img_path}')

    # Save cluster centroids
    cluster_data = np.hstack((np.arange(1, k + 1).reshape((-1, 1)), centers))
    with open(clusters_path, 'w') as f:
        f.write(nparray_to_str(cluster_data))
    print(f'Centroids saved in: {clusters_path}')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.src_img, args.dst_folder, args.k_init_centroids)
