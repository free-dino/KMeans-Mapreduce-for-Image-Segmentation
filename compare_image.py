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

def compare_images(img1, img2):
    """
    Compares two images using Dice coefficient
    Returns a combined similarity percentage based on Dice.
    """
    dice = dice_coefficient(img1, img2)
    
    similarity_percentage = dice * 100
    
    return similarity_percentage  # Return metrics


def process_folders(result_folder, mask_folder, output_file="./comparison_results.txt"):
    """
    Processes two folders, comparing image pairs from the result folder with mask images.
    """
    result_files = sorted([f for f in os.listdir(result_folder)])
    mask_files = sorted([f for f in os.listdir(mask_folder)])

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
            similarity = compare_images(img1, img2)
            similarities.append(similarity)
        
            file.write(f"{result_file} và {mask_file} giống nhau: {similarity:.2f}%")
            print(f"{result_file} và {mask_file} giống nhau {similarity:.2f}%")

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