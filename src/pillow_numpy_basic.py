from PIL import Image
import numpy as np
import sys
import os

#python .\pillow_numpy_basic.py .\test.jpg

def image_process(src):
    width, height = src.size
    dst = Image.new('RGB', (width, height))

    img_pixels = np.array([[src.getpixel((x, y)) for y in range(height)] for x in range(width)])

    for y in range(height):
        for x in range(width):
            r, g, b = img_pixels[x][y]
            dst.putpixel((x, y), (r, g, b))

    return dst

def save_with_unique_name(directory, filename, img):
    """Lưu ảnh với tên không trùng lặp trong thư mục."""
    name, ext = os.path.splitext(filename)
    counter = 1
    output_path = os.path.join(directory, filename)
    while os.path.exists(output_path):
        output_path = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1
    img.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    # Mở file ảnh
    try:
        input_img = Image.open(param[1])
    except:
        print('Failed to load %s' % param[1])
        quit()

    if input_img is None:
        print('Failed to load %s' % param[1])
        quit()

    # Xử lý ảnh
    output_img = image_process(input_img)

    # Đảm bảo thư mục output/other tồn tại
    output_dir = 'output/other'
    os.makedirs(output_dir, exist_ok=True)

    # Lưu ảnh với tên không trùng lặp
    output_filename = f"process_{os.path.basename(param[1])}"
    save_with_unique_name(output_dir, output_filename, output_img)
