from PIL import Image
import numpy as np
import sys
import os


filter = [0, 1, 0, 1, -4, 1, 0, 1, 0]

from PIL import Image
import numpy as np


filter = [0, 1, 0, 1, -4, 1, 0, 1, 0]

def apply_3x3_filter(src):
    width, height = src.size
    dst = Image.new('RGB', (width, height))

    img_pixels = np.array([[src.getpixel((x, y)) for y in range(height)] for x in range(width)])
    color = np.zeros((len(filter), 3))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            color[0] = img_pixels[x - 1][y - 1]
            color[1] = img_pixels[x - 1][y]
            color[2] = img_pixels[x - 1][y + 1]
            color[3] = img_pixels[x][y - 1]
            color[4] = img_pixels[x][y]
            color[5] = img_pixels[x][y + 1]
            color[6] = img_pixels[x + 1][y - 1]
            color[7] = img_pixels[x + 1][y]
            color[8] = img_pixels[x + 1][y + 1]

            sum_color = np.zeros(3)
            for num in range(len(filter)):
                sum_color += color[num] * filter[num]

            r, g, b = map(int, sum_color)
            r = min(max(r, 0), 255)
            g = min(max(g, 0), 255)
            b = min(max(b, 0), 255)

            dst.putpixel((x, y), (r, g, b))

    return dst


if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    
    try:
        input_img = Image.open(param[1])
    except:
        print('Failed to load %s' % param[1])
        quit()

    
    output_img = apply_3x3_filter(input_img)

    
    base_name = os.path.basename(param[1])
    output_dir = "output/other"
    os.makedirs(output_dir, exist_ok=True)  
    output_path = os.path.join(output_dir, f"filtered_{base_name}")
    output_img.save(output_path)
    output_img.show()

    print(f"Filtered image saved to {output_path}")
