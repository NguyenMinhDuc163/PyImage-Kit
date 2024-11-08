import os
import shutil


def clear_output_images():
    
    output_dir = '../output'
    subfolders = ['color', 'face', 'other', 'photo', 'resize']

    for folder in subfolders:
        folder_path = os.path.join(output_dir, folder)

        
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)  
                        print(f"Đã xóa: {file_path}")
                except Exception as e:
                    print(f"Không thể xóa {file_path}: {e}")
        else:
            print(f"Thư mục {folder_path} không tồn tại.")

    print("Dọn dẹp hoàn tất.")



clear_output_images()
