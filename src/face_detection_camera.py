#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import os

# Đường dẫn tới file cascade để phát hiện khuôn mặt và các mô hình giới tính, độ tuổi
cascade_path = "./cascades/haarcascade_frontalface_alt.xml"
age_proto = "./models/age_deploy.prototxt"
age_model = "./models/age_net.caffemodel"
gender_proto = "./models/gender_deploy.prototxt"
gender_model = "./models/gender_net.caffemodel"

# Màu của hình chữ nhật phát hiện khuôn mặt
color = (255, 255, 255)

# Tải các mô hình nhận diện tuổi và giới tính
age_net = cv2.dnn.readNet(age_model, age_proto)
gender_net = cv2.dnn.readNet(gender_model, gender_proto)
face_cascade = cv2.CascadeClassifier(cascade_path)

# Các nhãn cho độ tuổi và giới tính
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Nam', 'Nữ']


def detect_age_gender(face_img):
    blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

    # Nhận diện giới tính
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = gender_list[gender_preds[0].argmax()]

    # Nhận diện độ tuổi
    age_net.setInput(blob)
    age_preds = age_net.forward()
    age = age_list[age_preds[0].argmax()]

    return gender, age


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
        facerect = face_cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

        # Kiểm tra và vẽ hình chữ nhật xung quanh khuôn mặt nếu phát hiện
        if len(facerect) > 0:
            for (x, y, w, h) in facerect:
                face_img = capture[y:y + h, x:x + w]  # Cắt khuôn mặt
                gender, age = detect_age_gender(face_img)  # Nhận diện giới tính và tuổi
                label = f"{gender}, {age}"

                # Vẽ hình chữ nhật và nhãn trên khung hình
                cv2.rectangle(capture, (x, y), (x + w, y + h), color, thickness=2)
                cv2.putText(capture, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

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
