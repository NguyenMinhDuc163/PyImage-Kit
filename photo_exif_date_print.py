# -*- coding: utf-8 -*-
import cv2
import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

#python .\photo_exif_date_print.py .\test.jpg
font_color = (255, 255, 255)

def get_exif(file, field):
    img = Image.open(file)
    exif = img._getexif()
    if not exif:
        return []
    exif_data = []
    for id, value in exif.items():
        if TAGS.get(id) == field:
            tag = TAGS.get(id, id), value
            exif_data.extend(tag)
    return exif_data

def get_exif_of_image(file):
    im = Image.open(file)
    try:
        exif = im._getexif()
    except AttributeError:
        return {}
    if not exif:
        return {}
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
    return exif_table

def get_date_of_image(file):
    exif_table = get_exif_of_image(file)
    return exif_table.get("DateTimeOriginal")

def put_date(file, date):
    base_img_cv2 = cv2.imread(file)
    base_img = Image.open(file).convert('RGBA')
    txt = Image.new('RGB', base_img.size, (0, 0, 0))
    draw = ImageDraw.Draw(txt)

    # Sử dụng font hệ thống hoặc font mặc định nếu không tìm thấy
    try:
        fnt = ImageFont.truetype("arial.ttf", size=(int)((base_img.size[0] + base_img.size[1]) / 100))
    except IOError:
        print("Font Arial không tìm thấy. Đang dùng font mặc định.")
        fnt = ImageFont.load_default()

    textw, texth = draw.textsize(date, font=fnt)
    draw.text(((base_img.size[0] * 0.95 - textw), (base_img.size[1] * 0.95 - texth)),
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
    if len(param) != 2:
        print("Usage: $ python " + param[0] + " sample.jpg")
        quit()

    # Đảm bảo thư mục output/photo tồn tại
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Lấy ngày từ EXIF
        date = get_date_of_image(param[1])
        if date:
            output_img = put_date(param[1], date)
            output_filename = f"{date.replace(':', '_').replace(' ', '_')}_{os.path.basename(param[1])}"
            save_with_unique_name(output_dir, output_filename, output_img)
        else:
            # Nếu không có ngày trong EXIF, lưu ảnh với tiền tố 'nodate_'
            print("No date found in EXIF data.")
            output_img = cv2.imread(param[1])
            output_filename = f"nodate_{os.path.basename(param[1])}"
            save_with_unique_name(output_dir, output_filename, output_img)
    except Exception as e:
        print(f"Error processing image: {e}")
