# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
import os

#python .\measure_color_average.py .\test.jpg rgb
#python .\measure_color_average.py .\test.jpg hsv



def measure_color_average(image_path, color_space="rgb"):
    # Đọc ảnh
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        print(f"Không thể mở ảnh {image_path}")
        return None

    # Chuyển đổi ảnh sang HSV nếu cần
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV) if color_space == "hsv" else bgr_img

    # Tính trung bình màu
    average_color = [0, 0, 0]
    for i in range(3):
        extract_img = hsv_img[:, :, i] if color_space == "hsv" else bgr_img[:, :, i]
        extract_img = extract_img[extract_img > 0]
        average_color[i] = np.average(extract_img)

    # Lưu kết quả vào file
    output_dir = "output/other"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"average_color_{color_space}.txt")

    with open(output_path, "w") as file:
        if color_space == "rgb":
            file.write(f"Average RGB: {average_color[2]}, {average_color[1]}, {average_color[0]}\n")
        elif color_space == "hsv":
            file.write(f"Average HSV: {average_color[0]}, {average_color[1]}, {average_color[2]}\n")

    print(f"Average {color_space.upper()} saved to {output_path}")
    return average_color



if __name__ == '__main__':
    param = sys.argv
    if len(param) != 3:
        print("Usage: $ python " + param[0] + " sample.jpg rgb or hsv")
        quit()

    # Mở tệp ảnh
    bgr_img = cv2.imread(param[1])
    if bgr_img is None:
        print(f"Failed to load image {param[1]}")
        quit()

    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

    average_bgr = [0, 0, 0]
    average_hsv = [0, 0, 0]

    # Tính trung bình màu RGB
    for i in range(3):
        extract_img = bgr_img[:, :, i]
        extract_img = extract_img[extract_img > 0]
        average_bgr[i] = np.average(extract_img)

    # Tính trung bình màu HSV
    for i in range(3):
        extract_img = hsv_img[:, :, i]
        extract_img = extract_img[extract_img > 0]
        average_hsv[i] = np.average(extract_img)

    # Tạo thư mục output/other nếu chưa tồn tại
    output_dir = "output/other"
    os.makedirs(output_dir, exist_ok=True)

    # Tạo tên tệp đầu ra dựa trên lựa chọn định dạng màu
    output_path = os.path.join(output_dir, f"average_color_{param[2]}.txt")

    # Lưu kết quả vào file
    with open(output_path, "w") as file:
        if param[2] == "rgb":
            file.write(f"Average RGB: {average_bgr[2]}, {average_bgr[1]}, {average_bgr[0]}\n")
            print(f"Average RGB saved to {output_path}")
        elif param[2] == "hsv":
            file.write(f"Average HSV: {average_hsv[0]}, {average_hsv[1]}, {average_hsv[2]}\n")
            print(f"Average HSV saved to {output_path}")
        else:
            print("Option is wrong. Please select 'rgb' or 'hsv'")
