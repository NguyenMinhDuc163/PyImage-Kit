# -*- coding: utf-8 -*-
import sys

import cv2
import numpy as np
import math
import random
import os
from os import path

# python .\face_crop.py .\test.jpg

# Chỉ định thư mục cascades của dự án
cascades_dir = path.join("cascades")
max_size = 720


def detect(img, filename):
    # Tải các bộ phân loại Haar cascade cho khuôn mặt và mắt
    cascade_f = cv2.CascadeClassifier(
        path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml')
    )
    cascade_e = cv2.CascadeClassifier(
        path.join(cascades_dir, 'haarcascade_eye.xml')
    )

    # Kiểm tra xem các cascade có được tải thành công không
    if cascade_f.empty() or cascade_e.empty():
        print("Không thể tải các file cascade. Vui lòng kiểm tra đường dẫn và các file cascade.")
        return []

    # Resize ảnh nếu quá lớn để tăng tốc độ xử lý
    rows, cols, _ = img.shape
    if max(rows, cols) > max_size:
        scale = max_size / max(rows, cols)
        img = cv2.resize(img, (int(cols * scale), int(rows * scale)))
    rows, cols, _ = img.shape

    # Chuyển ảnh sang màu xám để xử lý
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Tạo một khung vuông đủ lớn để chứa ảnh khi xoay
    hypot = int(math.ceil(math.hypot(rows, cols)))
    frame = np.zeros((hypot, hypot), np.uint8)
    x_offset = int((hypot - cols) / 2)
    y_offset = int((hypot - rows) / 2)
    frame[y_offset:y_offset + rows, x_offset:x_offset + cols] = gray

    # Tạo thư mục output/face nếu chưa tồn tại
    output_dir = 'output/face'
    os.makedirs(output_dir, exist_ok=True)

    # Danh sách để lưu các ảnh khuôn mặt đã cắt
    cropped_faces = []

    # Biến đếm số lượng khuôn mặt
    numb = 0

    # Xoay ảnh từ -48 đến 48 độ với bước nhảy 6 độ
    for deg in range(-48, 49, 6):
        # Tạo ma trận xoay và áp dụng xoay ảnh
        M = cv2.getRotationMatrix2D((hypot / 2, hypot / 2), deg, 1.0)
        rotated = cv2.warpAffine(frame, M, (hypot, hypot))

        # Phát hiện khuôn mặt trong ảnh đã xoay
        faces = cascade_f.detectMultiScale(rotated, scaleFactor=1.08, minNeighbors=2)
        print(f"Góc xoay: {deg}°, Số khuôn mặt phát hiện: {len(faces)}")

        for (x, y, w, h) in faces:
            # Vùng quan tâm cho việc phát hiện mắt
            y_offset_face = int(h * 0.1)
            roi = rotated[y + y_offset_face:y + h, x:x + w]

            # Phát hiện mắt trong vùng khuôn mặt
            eyes = cascade_e.detectMultiScale(roi, scaleFactor=1.05)
            eyes = [
                e for e in eyes if
                (e[0] > w / 2 or e[0] + e[2] < w / 2) and
                e[1] + e[3] < h / 2
            ]

            # Kiểm tra nếu tìm thấy 2 mắt và khoảng cách giữa chúng đủ lớn
            if len(eyes) == 2 and abs(eyes[0][0] - eyes[1][0]) > w / 4:
                # Tính độ nghiêng của khuôn mặt dựa trên vị trí của mắt
                dx = abs(eyes[1][0] - eyes[0][0])
                dy = abs(eyes[1][1] - eyes[0][1])
                score = math.atan2(dy, dx)
                if eyes[0][1] == eyes[1][1]:
                    score = 0.0
                if score < 0.15:  # Chỉ chấp nhận khuôn mặt có độ nghiêng nhỏ
                    print(f"Vị trí khuôn mặt: {x}, {y}, {w}, {h}")
                    print(f"Độ nghiêng: {score}")
                    print(f"Số thứ tự khuôn mặt: {numb}")

                    # Cắt ảnh khuôn mặt từ ảnh đã xoay
                    output_img = rotated[y:y + h, x:x + w]
                    cropped_faces.append(output_img)  # Thêm ảnh vào danh sách

                    # Lưu ảnh khuôn mặt vào thư mục output/face
                    output_path = path.join(
                        output_dir, f"{numb:02d}_face_{filename}"
                    )
                    # Kiểm tra và thêm hậu tố nếu file đã tồn tại
                    while path.exists(output_path):
                        suffix = random.randint(1000, 9999)
                        output_path = path.join(
                            output_dir, f"{numb:02d}_face_{suffix}_{filename}"
                        )
                    cv2.imwrite(output_path, output_img)
                    numb += 1

    return cropped_faces  # Trả về danh sách các ảnh khuôn mặt đã cắt

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    # Mở file ảnh
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    detect(input_img, path.basename(param[1]))
