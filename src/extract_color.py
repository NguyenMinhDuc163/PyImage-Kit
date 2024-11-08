# -*- coding: utf-8 -*-
import cv2
import sys
import os
import numpy as np
import random


# python .\extract_color.py .\test.jpg 10 40 10 50

# extract color function

def extract_color(src, h_th_low, h_th_up, s_th, v_th):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    if h_th_low > h_th_up:
        _, h_dst_1 = cv2.threshold(h, h_th_low, 255, cv2.THRESH_BINARY)
        _, h_dst_2 = cv2.threshold(h, h_th_up, 255, cv2.THRESH_BINARY_INV)
        dst = cv2.bitwise_or(h_dst_1, h_dst_2)
    else:
        _, dst = cv2.threshold(h, h_th_low, 255, cv2.THRESH_TOZERO)
        _, dst = cv2.threshold(dst, h_th_up, 255, cv2.THRESH_TOZERO_INV)
        _, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)

    _, s_dst = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
    _, v_dst = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_and(dst, s_dst)
    dst = cv2.bitwise_and(dst, v_dst)

    # Đảm bảo kiểu dữ liệu là uint8
    dst = dst.astype(np.uint8)

    return dst


if __name__ == '__main__':
    param = sys.argv
    if len(param) != 6:
        print("Usage: $ python " + param[0] + " sample.jpg h_min h_max s_th v_th")
        quit()

    # Open image file
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    # Parameter setting
    h_min = int(param[2])
    h_max = int(param[3])
    s_th = int(param[4])
    v_th = int(param[5])

    # Make mask using the extract color function
    msk_img = extract_color(input_img, h_min, h_max, s_th, v_th)

    # Mask processing
    output_img = cv2.bitwise_and(input_img, input_img, mask=msk_img)

    # Create output/color directory if it doesn't exist
    output_dir = 'output/color'
    os.makedirs(output_dir, exist_ok=True)

    # Save the result in the output/color directory with the prefix 'extract_'
    output_path = os.path.join(output_dir, 'extract_' + os.path.basename(param[1]))

    # Check if the file already exists, and add a suffix if needed
    while os.path.exists(output_path):
        suffix = random.randint(1000, 9999)
        output_path = os.path.join(output_dir, f'extract_{suffix}_' + os.path.basename(param[1]))

    cv2.imwrite(output_path, output_img)
    print(f"Extracted color image saved to {output_path}")
