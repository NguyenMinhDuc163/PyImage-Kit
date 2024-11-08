import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import os
# python .\photo_date_print.py test.jpg "2024-11-07"
font_color = (255, 255, 255)

def print_date(file, date):
    base_img_cv2 = cv2.imread(file)
    base_img = Image.open(file).convert('RGBA')
    txt = Image.new('RGB', base_img.size, (0, 0, 0))
    draw = ImageDraw.Draw(txt)

    # Sử dụng font Arial hoặc font mặc định nếu không tìm thấy Arial
    try:
        fnt = ImageFont.truetype("arial.ttf", size=(int)((base_img.size[0] + base_img.size[1]) / 100))
    except IOError:
        print("Font Arial không tìm thấy. Đang dùng font mặc định.")
        fnt = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), date, font=fnt)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(((base_img.size[0] * 0.95 - text_width),
              (base_img.size[1] * 0.95 - text_height)),
              date, font=fnt, fill=font_color)

    txt_array = np.array(txt)
    output_img = cv2.addWeighted(base_img_cv2, 1.0, txt_array, 1.0, 0)
    return output_img

def save_with_unique_name(directory, filename, img):
    name, ext = os.path.splitext(filename)
    counter = 1
    output_path = os.path.join(directory, filename)
    while os.path.exists(output_path):
        output_path = os.path.join(directory, f"{name}_{counter}{ext}")
        counter += 1
    cv2.imwrite(output_path, img)
    print(f"Image saved to {output_path}")

if __name__ == '__main__':
    param = sys.argv
    if len(param) != 3:
        print("Usage: $ python " + param[0] + " <image filename> <date>")
        quit()

    # Đảm bảo thư mục output/photo tồn tại
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    # Tạo ảnh có ngày
    output_img = print_date(param[1], param[2])

    # Lưu ảnh với tên không trùng lặp
    output_filename = f"{param[2].replace(':', '_').replace(' ', '_')}_{os.path.basename(param[1])}"
    save_with_unique_name(output_dir, output_filename, output_img)
