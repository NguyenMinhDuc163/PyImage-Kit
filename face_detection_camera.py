#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os

# Đường dẫn tới file cascade để phát hiện khuôn mặt
cascade_path = "./cascades/haarcascade_frontalface_alt.xml"
color = (255, 255, 255)  # Màu của hình chữ nhật phát hiện khuôn mặt


def face_detect_camera():
    # Khởi tạo camera
    cam = cv2.VideoCapture(0)

    # Kiểm tra xem camera có được mở thành công không
    if not cam.isOpened():
        print("Không thể mở camera.")
        return

    # Tạo thư mục output để lưu ảnh phát hiện khuôn mặt
    output_dir = 'output/face'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'facedetect_capture.jpg')

    while True:
        ret, capture = cam.read()
        if not ret:
            print('Không thể lấy khung hình từ camera')
            break

        # Chuyển đổi ảnh sang màu xám để phát hiện khuôn mặt
        image_gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(cascade_path)
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

        # Kiểm tra và vẽ hình chữ nhật xung quanh khuôn mặt nếu phát hiện
        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(capture, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)

            # Lưu ảnh có khuôn mặt với tên file cố định
            cv2.imwrite(output_path, capture)
            print(f"Đã lưu ảnh phát hiện khuôn mặt tại {output_path}")

        # Hiển thị khung hình với phát hiện khuôn mặt
        cv2.imshow('Face Detector - Nhấn "q" để thoát', capture)

        # Nhấn phím 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Thoát chương trình phát hiện khuôn mặt.")
            break

    # Giải phóng camera và đóng cửa sổ hiển thị
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    face_detect_camera()
