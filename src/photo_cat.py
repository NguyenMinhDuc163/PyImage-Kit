# -*- coding: utf-8 -*-
import cv2
import sys
import os

# python .\photo_cat.py .\test.jpg .\test.jpg .\test.jpg .\test.jpg


def combine_photos(image_paths):
    # Đọc các ảnh từ đường dẫn
    images = [cv2.imread(path) for path in image_paths]

    # Kiểm tra nếu ảnh nào đó không tồn tại hoặc không thể đọc
    if any(img is None for img in images):
        print("One or more images could not be loaded. Please check the file paths.")
        return None

    # Đảm bảo rằng có đúng 4 ảnh để ghép
    if len(images) != 4:
        print("Số lượng ảnh không đủ để kết hợp.")
        return None

    # Thay đổi kích thước tất cả ảnh theo kích thước của ảnh đầu tiên
    height, width = images[0].shape[:2]
    resized_images = [cv2.resize(img, (width, height)) for img in images]

    # Kết hợp ảnh theo đúng thứ tự
    img5 = cv2.vconcat([resized_images[0], resized_images[1]])
    img6 = cv2.vconcat([resized_images[2], resized_images[3]])
    combined_img = cv2.hconcat([img5, img6])

    # Tạo thư mục đầu ra nếu chưa tồn tại
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'combined_output.jpg')
    cv2.imwrite(output_path, combined_img)
    print(f"Combined image saved to {output_path}")

    return combined_img





if __name__ == '__main__':
    # Kiểm tra nếu đủ số lượng ảnh đầu vào
    param = sys.argv
    if len(param) != 5:
        print("Usage: $ python " + param[0] + " image1.jpg image2.jpg image3.jpg image4.jpg")
        quit()

    # Đọc các ảnh từ tham số đầu vào
    img1 = cv2.imread(param[1])
    img2 = cv2.imread(param[2])
    img3 = cv2.imread(param[3])
    img4 = cv2.imread(param[4])

    # Kiểm tra nếu ảnh nào đó không tồn tại hoặc không thể đọc
    if img1 is None or img2 is None or img3 is None or img4 is None:
        print("One or more images could not be loaded. Please check the file paths.")
        quit()

    # Kết hợp ảnh
    img5 = cv2.vconcat([img1, img2])
    img6 = cv2.vconcat([img3, img4])
    img7 = cv2.hconcat([img5, img6])

    # Đảm bảo thư mục output/other tồn tại
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    # Lưu ảnh kết quả với tên khác trong thư mục output/other
    output_path = os.path.join(output_dir, 'combined_output.jpg')
    cv2.imwrite(output_path, img7)
    print(f"Combined image saved to {output_path}")
