# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
import os

# python .\watershed.py .\test.jpg
def watershed(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(src, markers)
    src[markers == -1] = [255, 0, 0]
    return markers, src

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    input_img = cv2.imread(param[1])
    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    markers, img = watershed(input_img)

    output_dir = 'output/other'
    os.makedirs(output_dir, exist_ok=True)

    markers_path = os.path.join(output_dir, "watershed_markers_" + os.path.basename(param[1]))
    img_path = os.path.join(output_dir, "watershed_image_" + os.path.basename(param[1]))

    cv2.imwrite(markers_path, markers)
    cv2.imwrite(img_path, img)
    print(f"Markers saved to {markers_path}")
    print(f"Watershed image saved to {img_path}")
