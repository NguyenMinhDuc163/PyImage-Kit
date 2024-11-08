
import sys

import cv2
import numpy as np
import math
import random
import os
from os import path




cascades_dir = path.join("cascades")
max_size = 720


def detect(img, filename):
    
    cascade_f = cv2.CascadeClassifier(
        path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml')
    )
    cascade_e = cv2.CascadeClassifier(
        path.join(cascades_dir, 'haarcascade_eye.xml')
    )

    
    if cascade_f.empty() or cascade_e.empty():
        print("Không thể tải các file cascade. Vui lòng kiểm tra đường dẫn và các file cascade.")
        return []

    
    rows, cols, _ = img.shape
    if max(rows, cols) > max_size:
        scale = max_size / max(rows, cols)
        img = cv2.resize(img, (int(cols * scale), int(rows * scale)))
    rows, cols, _ = img.shape

    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    hypot = int(math.ceil(math.hypot(rows, cols)))
    frame = np.zeros((hypot, hypot), np.uint8)
    x_offset = int((hypot - cols) / 2)
    y_offset = int((hypot - rows) / 2)
    frame[y_offset:y_offset + rows, x_offset:x_offset + cols] = gray

    
    output_dir = 'output/face'
    os.makedirs(output_dir, exist_ok=True)

    
    cropped_faces = []

    
    numb = 0

    
    for deg in range(-48, 49, 6):
        
        M = cv2.getRotationMatrix2D((hypot / 2, hypot / 2), deg, 1.0)
        rotated = cv2.warpAffine(frame, M, (hypot, hypot))

        
        faces = cascade_f.detectMultiScale(rotated, scaleFactor=1.08, minNeighbors=2)
        print(f"Góc xoay: {deg}°, Số khuôn mặt phát hiện: {len(faces)}")

        for (x, y, w, h) in faces:
            
            y_offset_face = int(h * 0.1)
            roi = rotated[y + y_offset_face:y + h, x:x + w]

            
            eyes = cascade_e.detectMultiScale(roi, scaleFactor=1.05)
            eyes = [
                e for e in eyes if
                (e[0] > w / 2 or e[0] + e[2] < w / 2) and
                e[1] + e[3] < h / 2
            ]

            
            if len(eyes) == 2 and abs(eyes[0][0] - eyes[1][0]) > w / 4:
                
                dx = abs(eyes[1][0] - eyes[0][0])
                dy = abs(eyes[1][1] - eyes[0][1])
                score = math.atan2(dy, dx)
                if eyes[0][1] == eyes[1][1]:
                    score = 0.0
                if score < 0.15:  
                    print(f"Vị trí khuôn mặt: {x}, {y}, {w}, {h}")
                    print(f"Độ nghiêng: {score}")
                    print(f"Số thứ tự khuôn mặt: {numb}")

                    
                    output_img = rotated[y:y + h, x:x + w]
                    cropped_faces.append(output_img)  

                    
                    output_path = path.join(
                        output_dir, f"{numb:02d}_face_{filename}"
                    )
                    
                    while path.exists(output_path):
                        suffix = random.randint(1000, 9999)
                        output_path = path.join(
                            output_dir, f"{numb:02d}_face_{suffix}_{filename}"
                        )
                    cv2.imwrite(output_path, output_img)
                    numb += 1

    return cropped_faces  

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    detect(input_img, path.basename(param[1]))
