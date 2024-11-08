
import cv2
import sys
import os
import random





def color_gray(src):
    img_bgr = cv2.split(src)
    
    gray_value = ((img_bgr[0].astype('float32') + img_bgr[1].astype('float32') + img_bgr[2].astype('float32')) / 3).astype('uint8')
    dst = cv2.merge((gray_value, gray_value, gray_value))
    return dst



if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    
    output_img = color_gray(input_img)

    
    output_dir = 'output/color'
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, 'gray_' + os.path.basename(param[1]))

    
    while os.path.exists(output_path):
        suffix = random.randint(1000, 9999)
        output_path = os.path.join(output_dir, f'gray_{suffix}_' + os.path.basename(param[1]))

    
    cv2.imwrite(output_path, output_img)
    print(f"Gray image saved to {output_path}")
