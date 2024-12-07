import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def compare_images(img1, img2):
    """
    So sánh hai ảnh, tập trung vào các vùng sáng (pixel khác 0).
    """
    # Tạo mặt nạ để chỉ giữ pixel khác 0
    mask1 = img1 > 0
    mask2 = img2 > 0
    combined_mask = mask1 | mask2  # Giữ lại vùng có pixel khác 0 của cả hai ảnh

    # Áp dụng mặt nạ lên ảnh
    img1_focus = img1[combined_mask]
    img2_focus = img2[combined_mask]

    # Tính MSE (chỉ trên vùng sáng)
    mse = np.mean((img1_focus - img2_focus) ** 2)
    max_mse = 255 ** 2  # MSE tối đa cho ảnh grayscale
    normalized_mse = 1 - (mse / max_mse)

    # Tính SSIM (chỉ trên vùng sáng)
    ssim_index = ssim(img1_focus, img2_focus)

    # Kết hợp MSE và SSIM
    weight_ssim = 0.7 
    weight_mse = 0.3
    similarity_percentage = (weight_ssim * ssim_index) + (weight_mse * normalized_mse)
    similarity_percentage *= 100

    return similarity_percentage

def process_folders(result_folder, mask_folder, output_file = "./comparison_results.txt"):
    """
    Duyệt qua hai thư mục và so sánh từng cặp ảnh tương ứng.
    """
    result_files = sorted([f for f in os.listdir(result_folder) if f.endswith('.jpg')])
    mask_files = sorted([f for f in os.listdir(mask_folder) if f.endswith('.jpg')])

    if len(result_files) != len(mask_files):
        print("Số lượng ảnh trong hai thư mục không khớp!")
        return

    similarities = []

    with open(output_file, "w") as file:
        file.write("KET QUA SO SANH:\n\n")
        
        for result_file, mask_file in zip(result_files, mask_files):
            result_path = os.path.join(result_folder, result_file)
            mask_path = os.path.join(mask_folder, mask_file)

            # Đọc ảnh
            img1 = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            if img1.shape != img2.shape:
                print(f"Kích thước không khớp: {result_file} và {mask_file}")
                continue

            # Tính toán mức độ giống nhau
            similarity = compare_images(img1, img2)
            similarities.append(similarity)
        
            file.write(f"{result_file} và {mask_file} giống nhau: {similarity:.2f}%\n")
            print(f"{result_file} và {mask_file} giống nhau {similarity:.2f}%")

        # Tính max, trung bình
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
