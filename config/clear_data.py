import os
import shutil


def clear_output_images():
    # Đường dẫn thư mục output chứa các thư mục con cần dọn dẹp
    output_dir = '../output'
    subfolders = ['color', 'face', 'other', 'photo', 'resize']

    for folder in subfolders:
        folder_path = os.path.join(output_dir, folder)

        # Kiểm tra xem thư mục con có tồn tại không
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Xóa tệp
                        print(f"Đã xóa: {file_path}")
                except Exception as e:
                    print(f"Không thể xóa {file_path}: {e}")
        else:
            print(f"Thư mục {folder_path} không tồn tại.")

    print("Dọn dẹp hoàn tất.")


# Gọi hàm để xóa ảnh trong các thư mục con của output
clear_output_images()
