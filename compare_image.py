import cv2
import numpy as np
import os

def dice_coefficient(img1, img2):
    """
    Computes the Dice coefficient between two binary images.
    Dice = 2 * (|A ∩ 😎) / (|A| + |B|)
    """
    intersection = np.sum((img1 > 0) & (img2 > 0))  # Count overlapping foreground pixels
    total_pixels = np.sum((img1 > 0)) + np.sum((img2 > 0))  # Count total pixels in both masks
    
    if total_pixels == 0:
        return 1.0  # If both images are empty, the similarity is perfect (1.0)
    
    dice = 2 * intersection / total_pixels
    return dice


def iou_score(img1, img2):
    """
    Computes the Intersection over Union (IoU) between two binary images.
    IoU = |A ∩ 😎 / |A ∪ 😎
    """
    intersection = np.sum((img1 > 0) & (img2 > 0))  # Count overlapping foreground pixels
    union = np.sum((img1 > 0) | (img2 > 0))  # Count the union of foreground pixels in both masks
    
    if union == 0:
        return 1.0  # If both images are empty, the similarity is perfect (1.0)
    
    iou = intersection / union
    return iou


def compare_images(img1, img2):
    """
    Compares two images using Dice coefficient and IoU.
    Returns a combined similarity percentage based on IoU and Dice.
    """
    dice = dice_coefficient(img1, img2)
    iou = iou_score(img1, img2)
    
    # You can combine them if you want, or just return them separately
    similarity_percentage = (0.5 * dice + 0.5 * iou) * 100  # Weighted combination (optional)
    
    return similarity_percentage, dice * 100, iou * 100  # Return separate metrics as well


def process_folders(result_folder, mask_folder, output_file="./comparison_results.txt"):
    """
    Processes two folders, comparing image pairs from the result folder with mask images.
    """
    result_files = sorted([f for f in os.listdir(result_folder) if f.endswith('.png')])
    mask_files = sorted([f for f in os.listdir(mask_folder) if f.endswith('.png')])

    if len(result_files) != len(mask_files):
        print("Số lượng ảnh trong hai thư mục không khớp!")
        return

    similarities = []

    with open(output_file, "w") as file:
        file.write("KẾT QUẢ SO SÁNH:\n\n")
        
        for result_file, mask_file in zip(result_files, mask_files):
            result_path = os.path.join(result_folder, result_file)
            mask_path = os.path.join(mask_folder, mask_file)

            # Đọc ảnh
            img1 = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            if img1.shape != img2.shape:
                print(f"Kích thước không khớp: {result_file} và {mask_file}")
                continue

            # So sánh hai ảnh
            similarity, dice, iou = compare_images(img1, img2)
            similarities.append(similarity)
        
            file.write(f"{result_file} và {mask_file} giống nhau: {similarity:.2f}% (Dice: {dice:.2f}%, IoU: {iou:.2f}%)\n")
            print(f"{result_file} và {mask_file} giống nhau {similarity:.2f}% (Dice: {dice:.2f}%, IoU: {iou:.2f}%)")

        # Tính mức độ giống nhau cao nhất và trung bình
        if similarities:
            max_similarity = np.max(similarities)
            avg_similarity = np.mean(similarities)
        
            file.write("\n")
            file.write(f"Độ giống nhau cao nhất: {max_similarity:.2f}%\n")
            file.write(f"Độ giống nhau trung bình: {avg_similarity:.2f}%\n")

            print(f"\nĐộ giống nhau cao nhất: {max_similarity:.2f}%")
            print(f"Độ giống nhau trung bình: {avg_similarity:.2f}%")
        else:
            file.write("\nKhông có kết quả nào để tính trung bình.\n")
            print("\nKhông có kết quả nào để tính trung bình.")


if __name__ == "__main__":
    # Đường dẫn tới hai thư mục
    result_folder = "./dataset/result"  
    mask_folder = "./dataset/mask"      

    process_folders(result_folder, mask_folder)