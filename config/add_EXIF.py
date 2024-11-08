import piexif
from PIL import Image
from datetime import datetime
import os


def add_exif_date(file_path, date=None):
    """
    Thêm thông tin ngày giờ vào ảnh dưới dạng EXIF.

    Parameters:
    - file_path (str): Đường dẫn đến ảnh.
    - date (str, optional): Chuỗi ngày giờ theo định dạng 'YYYY:MM:DD HH:MM:SS'. Nếu không cung cấp, sẽ dùng thời gian hiện tại.
    """
    
    img = Image.open(file_path)

    
    if not date:
        date = datetime.now().strftime('%Y:%m:%d %H:%M:%S')

    
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}}
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date

    
    exif_bytes = piexif.dump(exif_dict)

    
    output_dir = "../input"
    os.makedirs(output_dir, exist_ok=True)

    
    output_path = os.path.join(output_dir, f"with_exif_{os.path.basename(file_path)}")

    
    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"Đã thêm thông tin ngày vào ảnh và lưu tại: {output_path}")



if __name__ == "__main__":
    file_path = "../input/test.jpg"  
    add_exif_date(file_path)
