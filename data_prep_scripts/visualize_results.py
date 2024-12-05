import argparse
from glob import glob
from os.path import join, isdir, isfile

import cv2
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser(description='This script visualizes estimated clusters.')

parser.add_argument('--clusters_path', type=str, help='File or directory path to generated clusters.')
parser.add_argument('--kmeans_img', type=str, help='Path to the kmeans-preprocessed image.')
parser.add_argument('--dst_img', type=str, help='Path to the image to be written.')


args = parser.parse_args()

def load_clusters(path):
    if isdir(path):
        files = glob(join(path, 'part-r-*[0-9]'))
    elif isfile(path):
        files = [path]
    else:
        raise Exception('Invalid file path.')

    centroids = [load_nparray(file)[:, 1:] for file in files]
    centroids = np.concatenate(centroids, axis=0).reshape(-1, centroids[0].shape[-1])
    return centroids


def load_nparray(file):
    data = []
    with open(file) as f:
        for line in f:
            data.append(np.array([float(num) for num in line.split(' ')]))

    return np.stack(data).astype(float)

# Binary image function
def binary_image(kmeans_img_path, threshold_value):

    GRAYSCALE_IMAGE = Image.open(kmeans_img_path).convert('L')
    GRAYSCALE_PIXEL = GRAYSCALE_IMAGE.load()

    horizontal_size = GRAYSCALE_IMAGE.size[0]
    vertical_size = GRAYSCALE_IMAGE.size[1]

    for x in range(horizontal_size):
        for y in range(vertical_size):
            if GRAYSCALE_PIXEL[x, y] < threshold_value:
                GRAYSCALE_PIXEL[x, y] = 0
            else:
                GRAYSCALE_PIXEL[x, y] = 255

    saved_filename = 'binary_image_' + str(threshold_value) + '.jpg'
    GRAYSCALE_IMAGE.save(saved_filename)


def main(clusters_path, kmeans_img, dst_img):
    clusters = load_clusters(clusters_path)
    img = cv2.imread(kmeans_img)
    shape = img.shape
    binary_image(kmeans_img, 100)
    gbr = cv2.imread('binary_image_100.jpg')
    # Taking a matrix of size 5 as the kernel
    kernel = np.ones((5,5), np.uint8)
    img_erosion = cv2.erode(gbr, kernel, iterations=4)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
    cv2.imwrite(dst_img,img_dilation)
    print(f'Opening image saved in:{dst_img}')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.clusters_path, args.kmeans_img, args.dst_img)
