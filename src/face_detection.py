
import cv2
import sys
import os
import random


cascade_path = "./cascades/haarcascade_frontalface_alt.xml"  
color = (255, 255, 255)  

def face_detect_draw_rectangle(file):
    image = cv2.imread(file)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)

    return image


if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    
    output_img = face_detect_draw_rectangle(param[1])

    
    output_dir = 'output/face'
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, 'facedetect_' + os.path.basename(param[1]))

    
    while os.path.exists(output_path):
        suffix = random.randint(1000, 9999)
        output_path = os.path.join(output_dir, f'facedetect_{suffix}_' + os.path.basename(param[1]))

    
    cv2.imwrite(output_path, output_img)
    print(f"Face-detected image saved to {output_path}")
