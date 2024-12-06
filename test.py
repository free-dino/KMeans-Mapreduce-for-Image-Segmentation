import cv2
import numpy as np

def compare_images(image_path_1, image_path_2):
    #read image
    image1 = cv2.imread(image_path_1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image_path_2, cv2.IMREAD_GRAYSCALE)


    #calculate the difference
    difference = cv2.absdiff(image1, image2)
    total_pixels = image1.shape[0] * image1.shape[1]
    non_zero_count = np.count_nonzero(difference)

    similarity_percentage = 100 - ((non_zero_count / total_pixels) * 100)
    return similarity_percentage

if __name__ == "__main__":
    image_path_1 = "./output/opening_image.jpg"
    image_path_2 = "./dataset/mask/Tr-me_0016_m.jpg"

    try:
        similarity = compare_images(image_path_1, image_path_2)
        print(f"Similarity between 2 image: {similarity:.2f}%")
    except Exception as e:
        print(f"error: {e}")

