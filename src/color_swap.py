# -*- coding: utf-8 -*-
import cv2
import sys
import os
import random

# python .\color_swap.py .\test.jpg

# extract color function
def color_swap(src):
    # Hoán đổi kênh màu bằng cv2.cvtColor
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    return dst


if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    # Open image file
    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    # Apply color swap
    output_img = color_swap(input_img)

    # Create output/color directory if it doesn't exist
    output_dir = 'output/color'
    os.makedirs(output_dir, exist_ok=True)

    # Prepare the output file path
    output_path = os.path.join(output_dir, 'swap_' + os.path.basename(param[1]))

    # Check if the file already exists, and add a suffix if needed
    while os.path.exists(output_path):
        suffix = random.randint(1000, 9999)
        output_path = os.path.join(output_dir, f'swap_{suffix}_' + os.path.basename(param[1]))

    # Save the image
    cv2.imwrite(output_path, output_img)
    print(f"Swapped color image saved to {output_path}")
