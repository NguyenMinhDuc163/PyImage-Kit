
import cv2
import sys
import os
import random
import numpy as np





def color_sepia(src):
    img_bgr = cv2.split(src)
    
    b = img_bgr[0].astype(np.float32) * 0.55
    g = img_bgr[1].astype(np.float32) * 0.8
    r = img_bgr[2].astype(np.float32) * 1.0

    
    b = np.clip(b, 0, 255).astype(np.uint8)
    g = np.clip(g, 0, 255).astype(np.uint8)
    r = np.clip(r, 0, 255).astype(np.uint8)

    dst = cv2.merge((b, g, r))
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

    
    output_img = color_sepia(input_img)

    
    output_dir = 'output/color'
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, 'sepia_' + os.path.basename(param[1]))

    
    while os.path.exists(output_path):
        suffix = random.randint(1000, 9999)
        output_path = os.path.join(output_dir, f'sepia_{suffix}_' + os.path.basename(param[1]))

    
    cv2.imwrite(output_path, output_img)
    print(f"Sepia image saved to {output_path}")
