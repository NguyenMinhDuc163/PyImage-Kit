import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import sys
import os

def print_text(file, text, font_color=(255, 255, 255), font_size=20):
    base_img_cv2 = cv2.imread(file)
    base_img = Image.open(file).convert('RGBA')
    txt = Image.new('RGBA', base_img.size, (0, 0, 0, 0))  # RGBA để có độ trong suốt cho text layer
    draw = ImageDraw.Draw(txt)

    # Sử dụng font Arial hoặc font mặc định nếu không tìm thấy Arial
    try:
        fnt = ImageFont.truetype("arial.ttf", size=font_size)
    except IOError:
        print("Font Arial không tìm thấy. Đang dùng font mặc định.")
        fnt = ImageFont.load_default()

    # Ngắt dòng nếu cần
    max_width = base_img.size[0] * 0.9  # Độ rộng tối đa cho text là 90% chiều rộng ảnh
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
    lines.append(line)  # Thêm dòng cuối

    # Vẽ từng dòng văn bản trên ảnh
    text_height = draw.textbbox((0, 0), lines[0], font=fnt)[3] - draw.textbbox((0, 0), lines[0], font=fnt)[1]
    total_text_height = len(lines) * text_height
    y = base_img.size[1] - total_text_height - 20  # 20px từ mép dưới

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        width = bbox[2] - bbox[0]
        x = base_img.size[0] - width - 20  # 20px từ mép phải
        draw.text((x, y), line, font=fnt, fill=font_color + (255,))  # Thêm alpha = 255 để đảm bảo màu đầy đủ
        y += text_height

    # Kết hợp layer văn bản với ảnh gốc
    combined_img = Image.alpha_composite(base_img, txt)  # Sử dụng alpha_composite để duy trì màu chữ rõ ràng
    output_img = cv2.cvtColor(np.array(combined_img), cv2.COLOR_RGBA2BGR)  # Chuyển ảnh kết hợp về BGR cho OpenCV
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

    # Đảm bảo thư mục output/photo tồn tại
    output_dir = 'output/photo'
    os.makedirs(output_dir, exist_ok=True)

    # Đọc ảnh và văn bản từ các tham số
    file = param[1]
    text = param[2]
    font_color = (255, 255, 255)  # Màu trắng mặc định
    font_size = 20  # Kích thước mặc định

    # Nếu có thêm tham số màu sắc
    if len(param) >= 6:
        font_color = (int(param[3]), int(param[4]), int(param[5]))

    # Nếu có thêm tham số kích cỡ
    if len(param) >= 7:
        font_size = int(param[6])

    # Tạo ảnh có văn bản với các tùy chọn màu sắc và kích cỡ
    output_img = print_text(file, text, font_color=font_color, font_size=font_size)

    # Lưu ảnh với tên không trùng lặp
    output_filename = f"{text.replace(':', '_').replace(' ', '_')}_{os.path.basename(file)}"
    save_with_unique_name(output_dir, output_filename, output_img)
