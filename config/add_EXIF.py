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
    # Mở ảnh
    img = Image.open(file_path)

    # Nếu không có ngày giờ, dùng thời gian hiện tại
    if not date:
        date = datetime.now().strftime('%Y:%m:%d %H:%M:%S')

    # Tạo cấu trúc EXIF nếu không có EXIF ban đầu
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "Interop": {}}
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date

    # Chuyển đổi dữ liệu EXIF thành định dạng bytes để lưu vào ảnh
    exif_bytes = piexif.dump(exif_dict)

    # Đảm bảo thư mục đầu ra là 'input'
    output_dir = "../input"
    os.makedirs(output_dir, exist_ok=True)

    # Đặt tên cho ảnh đã xử lý
    output_path = os.path.join(output_dir, f"with_exif_{os.path.basename(file_path)}")

    # Lưu ảnh với EXIF mới
    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"Đã thêm thông tin ngày vào ảnh và lưu tại: {output_path}")


# Sử dụng chương trình
if __name__ == "__main__":
    file_path = "../input/test.jpg"  # Đường dẫn tới ảnh của bạn trong thư mục input
    add_exif_date(file_path)
