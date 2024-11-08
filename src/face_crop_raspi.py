
import cv2
import sys
from os import path, makedirs
import random




cascades_dir = path.join("cascades")


def face_detect(file):
    image = cv2.imread(file)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade_f = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
    cascade_e = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_eye.xml'))

    facerect = cascade_f.detectMultiScale(image_gray, scaleFactor=1.08, minNeighbors=1, minSize=(200, 200))
    print("face rectangle")
    print(facerect)

    
    cropped_faces = []

    if len(facerect) > 0:
        for rect in facerect:
            x, y, w, h = rect
            
            roi = image_gray[y: y + h, x: x + w]
            eyes = cascade_e.detectMultiScale(roi, scaleFactor=1.05, minSize=(20, 20))
            
            if len(eyes) > 1:
                image_face = image[y:y + h, x:x + w]
                cropped_faces.append(image_face)  

    return cropped_faces  



if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    face_detect(param[1])
