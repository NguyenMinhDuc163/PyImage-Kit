import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def print_text(file, text, font_color=(255, 255, 255), font_size=20):
    base_img_cv2 = cv2.imread(file)
    base_img = Image.open(file).convert('RGBA')
    txt = Image.new('RGBA', base_img.size, (0, 0, 0, 0))  
    draw = ImageDraw.Draw(txt)

    
    try:
        fnt = ImageFont.truetype("arial.ttf", size=font_size)
    except IOError:
        print("Font Arial không tìm thấy. Đang dùng font mặc định.")
        fnt = ImageFont.load_default()

    
    max_width = base_img.size[0] * 0.9  
    lines = []
    words = text.split()
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=fnt)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)  

    
    text_height = draw.textbbox((0, 0), lines[0], font=fnt)[3] - draw.textbbox((0, 0), lines[0], font=fnt)[1]
    total_text_height = len(lines) * text_height
    y = base_img.size[1] - total_text_height - 20  

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        width = bbox[2] - bbox[0]
        x = base_img.size[0] - width - 20  
        draw.text((x, y), line, font=fnt, fill=font_color + (255,))  
        y += text_height

    
    combined_img = Image.alpha_composite(base_img, txt)  
    output_img = cv2.cvtColor(np.array(combined_img), cv2.COLOR_RGBA2BGR)  
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
    if len(param) < 3:
        print("Usage: $ python " + param[0] + " <image filename> <text> [<font color R G B>] [<font size>]")
        quit()

    
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    
    file = param[1]
    text = param[2]
    font_color = (255, 255, 255)  
    font_size = 20  

    
    if len(param) >= 6:
        font_color = (int(param[3]), int(param[4]), int(param[5]))

    
    if len(param) >= 7:
        font_size = int(param[6])

    
    output_img = print_text(file, text, font_color=font_color, font_size=font_size)

    
    output_filename = f"{text.replace(':', '_').replace(' ', '_')}_{os.path.basename(file)}"
    save_with_unique_name(output_dir, output_filename, output_img)
