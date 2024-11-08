# -*- coding: utf-8 -*-
import cv2
import sys
import os
from os import path
import random

# Đặt đường dẫn tới thư mục chứa các tệp cascade
cascades_dir = path.join("cascades")

color = (255, 255, 255)  # Màu của hình chữ nhật khi phát hiện khuôn mặt


def face_detect(file):
    image = cv2.imread(file)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade_f = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
    cascade_e = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_eye.xml'))

    facerect = cascade_f.detectMultiScale(image_gray, scaleFactor=1.08, minNeighbors=1, minSize=(50, 50))
    detected_faces = []  # Danh sách lưu các khuôn mặt được phát hiện

    if len(facerect) > 0:
        for rect in facerect:
            x, y, w, h = rect
            # Kiểm tra mắt để xác nhận đó là khuôn mặt
            y_offset = int(h * 0.1)
            eye_area = image_gray[y + y_offset: y + h, x: x + w]
            eyes = cascade_e.detectMultiScale(eye_area, 1.05)
            eyes = [e for e in eyes if (e[0] > w / 2 or e[0] + e[2] < w / 2) and e[1] + e[3] < h / 2]

            if len(eyes) > 0:
                image_face = image[y:y + h, x:x + h]
                detected_faces.append(image_face)  # Thêm khuôn mặt vào danh sách

    return detected_faces



if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    face_detect(param[1])
