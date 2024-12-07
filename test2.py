import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_images(image1_path, image2_path):
    """
    Hàm so sánh hai ảnh dựa trên MSE và SSIM.
    """
    # Đọc hai ảnh
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    
    # Kiểm tra kích thước của hai ảnh
    if img1.shape != img2.shape:
        raise ValueError(f"Kích thước ảnh không giống nhau: {image1_path} và {image2_path}")
    
    # Tính Mean Squared Error (MSE)
    mse = np.mean((img1 - img2) ** 2)
    
    # Tính Structural Similarity Index (SSIM)
    ssim_index = ssim(img1, img2)
    
    # Chuẩn hóa MSE
    max_mse = 255 ** 2  # MSE tối đa giữa 2 ảnh grayscale (cường độ pixel từ 0-255)
    normalized_mse = 1 - (mse / max_mse)
    
    # Tính độ giống nhau tổng hợp (dựa trên trọng số)
    weight_ssim = 0.7  # Trọng số của SSIM
    weight_mse = 0.3   # Trọng số của MSE
    similarity_percentage = (weight_ssim * ssim_index) + (weight_mse * normalized_mse)
    similarity_percentage *= 100  # Chuyển sang phần trăm

    return similarity_percentage, mse, ssim_index

def process_folders(output_folder, mask_folder, num_pairs):
    """
    Hàm xử lý so sánh ảnh trong hai thư mục output và mask.
    """
    results = []
    
    # Duyệt qua từng cặp ảnh (giả sử ảnh trong hai folder có cùng tên)
    for i in range(1, num_pairs + 1):
        output_image = os.path.join(output_folder, f"{i}.png")
        mask_image = os.path.join(mask_folder, f"{i}.png")
        
        # Kiểm tra file tồn tại
        if not os.path.exists(output_image) or not os.path.exists(mask_image):
            print(f"Lỗi: Không tìm thấy cặp ảnh {output_image} hoặc {mask_image}")
            continue
        
        try:
            # So sánh hai ảnh
            similarity, mse, ssim_value = compare_images(output_image, mask_image)
            results.append((i, similarity, mse, ssim_value))
            print(f"Cặp {i}: Giống nhau {similarity:.2f}%, MSE: {mse:.2f}, SSIM: {ssim_value:.4f}")
        except Exception as e:
            print(f"Lỗi khi xử lý cặp {i}: {e}")
    
    return results

if __name__ == "__main__":
    # Thư mục chứa ảnh
    output_folder = "output"  # Thay bằng đường dẫn thực tế
    mask_folder = "mask"     # Thay bằng đường dẫn thực tế
    
    # Số lượng cặp ảnh cần so sánh
    num_pairs = 50
    
    # Xử lý và so sánh các cặp ảnh
    results = process_folders(output_folder, mask_folder, num_pairs)
    
    # Lưu kết quả vào file (tùy chọn)
    with open("comparison_results.txt", "w") as f:
        f.write("Cặp Ảnh\tGiống Nhau (%)\tMSE\tSSIM\n")
        for result in results:
            f.write(f"{result[0]}\t{result[1]:.2f}\t{result[2]:.2f}\t{result[3]:.4f}\n")
    print("Kết quả đã được lưu vào comparison_results.txt")
