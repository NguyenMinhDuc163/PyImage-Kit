import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageTk

import cv2
import numpy as np
import os
import sys

# Import các hàm xử lý ảnh

from color_gray import color_gray
from color_sepia import color_sepia
from color_swap import color_swap
from extract_color import extract_color
from face_crop import detect
from face_crop_raspi import face_detect
from face_detection import face_detect_draw_rectangle
from face_detection_camera import face_detect_camera
from photo_cat import combine_photos
# Bộ lọc 3x3
from filter_3by3 import apply_3x3_filter
from photo_date_print import print_text
from watershed import watershed


def measure_color_average(image_path, color_space="rgb"):
    # Đọc ảnh
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        print(f"Không thể mở ảnh {image_path}")
        return None

    # Chuyển đổi ảnh sang HSV nếu cần
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV) if color_space == "hsv" else bgr_img

    # Tính trung bình màu
    average_color = [0, 0, 0]
    for i in range(3):
        extract_img = hsv_img[:, :, i] if color_space == "hsv" else bgr_img[:, :, i]
        extract_img = extract_img[extract_img > 0]
        average_color[i] = np.average(extract_img)

    # Lưu kết quả vào file
    output_dir = "output/other"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"average_color_{color_space}.txt")

    with open(output_path, "w") as file:
        if color_space == "rgb":
            file.write(f"Average RGB: {average_color[2]}, {average_color[1]}, {average_color[0]}\n")
        elif color_space == "hsv":
            file.write(f"Average HSV: {average_color[0]}, {average_color[1]}, {average_color[2]}\n")

    print(f"Average {color_space.upper()} saved to {output_path}")
    return average_color


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing GUI")
        self.root.geometry("1000x600")


        self.is_sift_feature_matching = False
        self.image_selection_stage = 1  # Trạng thái ban đầu là chọn ảnh đầu tiên
        self.image_path1 = None  # Đường dẫn cho ảnh thứ nhất
        self.image_path2 = None  # Đường dẫn cho ảnh thứ hai

        # Các biến để lưu trữ ảnh gốc và ảnh xử lý
        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.selected_images = []  # Danh sách lưu các đường dẫn ảnh đã chọn

        # Khung chính chứa các khung con
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Khung bên trái cho ảnh gốc
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Khung chứa các ảnh đã chọn cho Combine Photos
        self.selected_images_frame = tk.Frame(self.left_frame)
        self.selected_images_frame.pack()

        # Danh sách Label để hiển thị từng ảnh đã chọn
        self.selected_image_labels = []

        # Nút chọn ảnh cho Combine Photos (ẩn theo mặc định)
        self.combine_image_button = tk.Button(root, text="Chọn ảnh cho Combine Photos",
                                              command=self.select_image_for_combine)
        self.combine_image_button.pack(side=tk.TOP, pady=10)
        self.combine_image_button.pack_forget()  # Ẩn nút ngay từ đầu

        # Nút chọn ảnh
        self.select_image_button = tk.Button(root, text="Chọn ảnh", command=self.load_image)
        self.select_image_button.pack(side=tk.TOP, pady=10)

        # Nút mở camera phát hiện khuôn mặt
        self.camera_button = tk.Button(root, text="Mở Camera Phát Hiện Khuôn Mặt",
                                       command=self.open_camera_face_detection)
        self.camera_button.pack(side=tk.TOP, pady=10)

        # Khung giữa cho các nút chức năng
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Khung bên phải cho ảnh đã xử lý
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Canvas cho ảnh gốc và ảnh xử lý
        self.original_canvas = tk.Label(self.left_frame)
        self.original_canvas.pack()

        self.processed_canvas = tk.Label(self.right_frame)
        self.processed_canvas.pack()

        # Tạo các thành phần giao diện khác
        self.create_widgets()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.is_sift_feature_matching:
                # Nếu đang ở chế độ SIFT, chọn hai ảnh liên tiếp
                if self.image_selection_stage == 1:
                    # Lưu đường dẫn ảnh thứ nhất
                    self.image_path1 = file_path
                    self.original_image = cv2.imread(file_path)
                    if self.original_image is None:
                        print(f"Không thể mở tệp ảnh: {file_path}")
                        return
                    self.show_image(self.original_image, self.original_canvas)
                    print("Ảnh thứ nhất đã được chọn.")
                    self.image_selection_stage = 2  # Chuyển sang chọn ảnh thứ hai

                elif self.image_selection_stage == 2:
                    # Lưu đường dẫn ảnh thứ hai
                    self.image_path2 = file_path
                    self.processed_image = cv2.imread(file_path)
                    if self.processed_image is None:
                        print(f"Không thể mở tệp ảnh: {file_path}")
                        return
                    self.show_image(self.processed_image, self.processed_canvas)
                    print("Ảnh thứ hai đã được chọn.")
                    self.image_selection_stage = 1  # Trở về chọn ảnh thứ nhất để lần sau
                    # Thực hiện chức năng SIFT ngay sau khi chọn hai ảnh
                    self.apply_function()
            else:
                # Cho các chức năng khác, chỉ chọn một ảnh
                self.image_path = file_path
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    print(f"Không thể mở tệp ảnh: {file_path}")
                    return
                self.show_image(self.original_image, self.original_canvas)
                self.processed_image = None
                self.processed_canvas.config(image='')

    def resize_image(self, src, w_ratio, h_ratio):
        """Resize image based on width and height ratio."""
        height, width = src.shape[:2]
        resized_img = cv2.resize(src, (int(width * w_ratio / 100), int(height * h_ratio / 100)))
        return resized_img
    def select_image_for_combine(self):
        file_path = filedialog.askopenfilename(title="Chọn một ảnh")
        if file_path:
            # Thêm ảnh vào danh sách
            self.selected_images.append(file_path)

            # Đọc và hiển thị ảnh mới trong một Label riêng biệt
            image = cv2.imread(file_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_pil.thumbnail((100, 100))  # Giảm kích thước ảnh cho khung bên trái
            image_tk = ImageTk.PhotoImage(image_pil)

            label = tk.Label(self.selected_images_frame, image=image_tk)
            label.image = image_tk  # Giữ tham chiếu để tránh bị xóa
            label.pack(side=tk.LEFT, padx=5, pady=5)

            # Lưu Label vào danh sách để quản lý sau này
            self.selected_image_labels.append(label)

            print(f"Ảnh đã chọn: {file_path}")

            # Kiểm tra nếu đủ 4 ảnh thì tự động kết hợp
            if len(self.selected_images) == 4:
                self.apply_function()  # Tự động nhấn áp dụng khi đã đủ ảnh

    def show_image(self, image, canvas):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((300, 300))
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.image = image_tk  # Giữ tham chiếu
        canvas.config(image=image_tk)

    def combine_photos(self):
        combined_img = combine_photos(self.selected_images)
        if combined_img is not None:
            self.processed_image = combined_img
            self.show_image(self.processed_image, self.processed_canvas)
            print("Ảnh đã được kết hợp và hiển thị.")
            self.selected_images.clear()  # Xóa danh sách ảnh sau khi kết hợp

    def sift_matching(self, img1_path, img2_path):
        # Đọc ảnh từ đường dẫn
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        if img1 is None or img2 is None:
            messagebox.showerror("Error", "Không thể mở một hoặc cả hai ảnh.")
            return None

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Tạo đối tượng SIFT và tìm keypoints, descriptors
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # Khớp các mô tả đặc trưng giữa hai ảnh
        matcher = cv2.DescriptorMatcher_create("FlannBased")
        matches = matcher.match(des1, des2)

        # Vẽ các điểm đặc trưng và khớp trên ảnh
        output_img = self.drawMatches(img1, kp1, img2, kp2, matches[:100])

        # Tạo và lưu ảnh kết quả
        output_dir = 'output/other'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'matched_features.jpg')
        cv2.imwrite(output_path, output_img)
        print(f"Matched features image saved to {output_path}")

        return output_img  # Trả về ảnh kết quả để hiển thị

    def drawMatches(self, img1, kp1, img2, kp2, matches):
        rows1, cols1 = img1.shape[:2]
        rows2, cols2 = img2.shape[:2]

        # Tạo ảnh kết hợp từ hai ảnh đầu vào
        out = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')
        out[:rows1, :cols1, :] = img1
        out[:rows2, cols1:cols1 + cols2, :] = img2

        # Vẽ các điểm đặc trưng và các đường nối giữa chúng
        for mat in matches:
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx
            (x1, y1) = kp1[img1_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            cv2.circle(out, (int(x1), int(y1)), 4, (255, 0, 0), 1)
            cv2.circle(out, (int(x2) + cols1, int(y2)), 4, (255, 0, 0), 1)
            cv2.line(out, (int(x1), int(y1)), (int(x2) + cols1, int(y2)), (255, 0, 0), 1)

        return out

    def apply_function(self):
        if self.original_image is None and self.function_var.get() != "Combine Photos":
            print("Vui lòng chọn ảnh trước!")
            return

        selected_function = self.function_var.get()

        # Áp dụng các chức năng tương ứng
        if selected_function == "Grayscale":
            output_img = color_gray(self.original_image)
            prefix = 'gray'
        elif selected_function == "Sepia":
            output_img = color_sepia(self.original_image)
            prefix = 'sepia'
        elif selected_function == "Color Swap":
            output_img = color_swap(self.original_image)
            prefix = 'swap'
        elif selected_function == "Extract Color":
            # Kiểm tra xem các trường nhập liệu có tồn tại không
            if not hasattr(self, 'h_min_entry') or not hasattr(self, 'h_max_entry') or not hasattr(self,
                                                                                                   's_th_entry') or not hasattr(
                    self, 'v_th_entry'):
                print("Vui lòng chọn chức năng 'Extract Color' và nhập các giá trị cần thiết.")
                return

            # Lấy giá trị từ các ô nhập liệu
            try:
                h_min = int(self.h_min_entry.get())
                h_max = int(self.h_max_entry.get())
                s_th = int(self.s_th_entry.get())
                v_th = int(self.v_th_entry.get())
            except ValueError:
                messagebox.showerror("Lỗi giá trị", "Vui lòng nhập các giá trị số nguyên hợp lệ cho các tham số.")
                return

            # Kiểm tra giá trị nằm trong phạm vi cho phép
            if not (0 <= h_min <= 179):
                messagebox.showwarning("Cảnh báo", "Giá trị h_min phải nằm trong khoảng từ 0 đến 179.")
                return
            if not (0 <= h_max <= 179):
                messagebox.showwarning("Cảnh báo", "Giá trị h_max phải nằm trong khoảng từ 0 đến 179.")
                return
            if not (0 <= s_th <= 255):
                messagebox.showwarning("Cảnh báo", "Giá trị s_th phải nằm trong khoảng từ 0 đến 255.")
                return
            if not (0 <= v_th <= 255):
                messagebox.showwarning("Cảnh báo", "Giá trị v_th phải nằm trong khoảng từ 0 đến 255.")
                return

            # Áp dụng hàm `extract_color`
            mask_img = extract_color(self.original_image, h_min, h_max, s_th, v_th)
            output_img = cv2.bitwise_and(self.original_image, self.original_image, mask=mask_img)
            prefix = 'extract'

            # Hiển thị ảnh đã xử lý và lưu lại
            self.processed_image = output_img
            self.show_image(self.processed_image, self.processed_canvas)
            self.save_processed_image(prefix)
            print(f"Ảnh màu trích xuất đã được lưu vào thư mục output/color với tên {prefix}.")
            return
        elif selected_function == "Face Crop":
            cropped_faces = detect(self.original_image, os.path.basename(self.image_path))
            if cropped_faces:
                self.processed_image = cropped_faces[0]
                self.show_image(self.processed_image, self.processed_canvas)
                self.save_processed_image('face_crop')
            else:
                print("Không tìm thấy khuôn mặt nào.")
            return
        elif selected_function == "Face Crop (Raspi)":
            cropped_faces = face_detect(self.image_path)
            if cropped_faces:
                self.processed_image = cropped_faces[0]
                self.show_image(self.processed_image, self.processed_canvas)
                self.save_processed_image('face_crop_raspi')
            else:
                print("Không tìm thấy khuôn mặt nào.")
            return
        elif selected_function == "Face Detect (Save)":
            detected_faces = face_detect(self.image_path)
            if detected_faces:
                self.processed_image = detected_faces[0]
                self.show_image(self.processed_image, self.processed_canvas)
                print("Các khuôn mặt đã được phát hiện và lưu vào thư mục output/face.")
            else:
                print("Không tìm thấy khuôn mặt nào.")
            return
        elif selected_function == "Face Detect (Draw Rectangle)":
            output_img = face_detect_draw_rectangle(self.image_path)
            prefix = 'facedetect_rect'
        elif selected_function == "3x3 Filter":
            pil_image = Image.fromarray(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB))
            filtered_image = apply_3x3_filter(pil_image)
            self.processed_image = np.array(filtered_image)
            self.show_image(self.processed_image, self.processed_canvas)
            self.save_processed_image("filtered")
            print("Bộ lọc 3x3 đã được áp dụng và lưu lại.")
            return
        elif selected_function == "Average Color":
            color_space = self.color_space_var.get()
            if self.image_path:
                average_color = measure_color_average(self.image_path, color_space)
                if average_color:
                    tk.messagebox.showinfo("Average Color", f"Average {color_space.upper()} Color: {average_color}")
            else:
                print("Vui lòng chọn ảnh trước.")
            return
        elif selected_function == "Combine Photos":
            if len(self.selected_images) < 4:
                messagebox.showerror("Error", "Vui lòng chọn đủ 4 ảnh.")
                return

                # Kết hợp ảnh và hiển thị ở bên phải
            combined_img = combine_photos(self.selected_images)
            if combined_img is not None:
                self.processed_image = combined_img
                self.show_image(self.processed_image, self.processed_canvas)
                print("Ảnh đã được kết hợp và hiển thị.")
            return
        elif selected_function == "Print Text":
            # Lấy giá trị văn bản từ ô nhập liệu
            text = self.text_entry.get()

            # Sử dụng màu chữ được chọn (nếu có) hoặc mặc định là trắng
            font_color = getattr(self, 'font_color', (255, 255, 255))

            try:
                font_size = int(self.font_size_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Vui lòng nhập kích thước hợp lệ")
                return

            # Gọi hàm `print_text` với các tham số từ người dùng, bao gồm `font_color`
            output_img = print_text(self.image_path, text, font_color=font_color, font_size=font_size)
            prefix = "text_printed"  # Gán giá trị prefix để tránh lỗi UnboundLocalError

            # Hiển thị và lưu ảnh kết quả
            if output_img is not None and prefix is not None:
                self.processed_image = output_img
                self.show_image(self.processed_image, self.processed_canvas)
                self.save_processed_image(prefix)
                print("Ảnh có văn bản đã được lưu.")
        elif selected_function == "Resize Image":
            try:
                w_ratio = int(self.w_ratio_entry.get())
                h_ratio = int(self.h_ratio_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Vui lòng nhập tỷ lệ hợp lệ.")
                return

            # Gọi hàm resize_image với self
            output_img = self.resize_image(self.original_image, w_ratio, h_ratio)
            if output_img is not None:
                self.processed_image = output_img
                self.show_image(self.processed_image, self.processed_canvas)
                prefix = "resized"  # Gán giá trị cho prefix
                self.save_processed_image(prefix)
                print("Ảnh đã được thay đổi kích thước và lưu lại.")
        elif selected_function == "SIFT Feature Matching":

            if self.image_path1 and self.image_path2:

                output_img = self.sift_matching(self.image_path1, self.image_path2)

                if output_img is not None:
                    self.processed_image = output_img

                    self.show_image(self.processed_image, self.processed_canvas)

                    print("Ảnh khớp tính năng đã được hiển thị và lưu lại.")

            else:

                messagebox.showerror("Lỗi", "Vui lòng chọn đủ cả hai ảnh trước khi áp dụng.")
        elif selected_function == "Watershed":
            # Xử lý bằng watershed
            markers, output_img = watershed(self.original_image)

            # Lưu và hiển thị kết quả
            self.processed_image = output_img
            self.show_image(self.processed_image, self.processed_canvas)
            self.save_processed_image("watershed_image")

            # Lưu markers nếu cần
            output_dir = 'output/other'
            os.makedirs(output_dir, exist_ok=True)
            markers_path = os.path.join(output_dir, "watershed_markers_" + os.path.basename(self.image_path))
            cv2.imwrite(markers_path, markers)
            print(f"Markers saved to {markers_path}")

            print("Watershed processing completed and images saved.")
            return







        else:
            print("Vui lòng chọn chức năng hợp lệ.")
            return

        if selected_function not in ["Print Text", "Combine Photos", "Average Color"]:
            # Hiển thị và lưu ảnh đã xử lý nếu `prefix` được gán trước đó.
            if 'output_img' in locals():
                self.processed_image = output_img
                self.show_image(self.processed_image, self.processed_canvas)
                if 'prefix' in locals():
                    self.save_processed_image(prefix)


        # Hiển thị và lưu ảnh đã xử lý
        if 'output_img' in locals() and output_img is not None:
            self.processed_image = output_img
            self.show_image(self.processed_image, self.processed_canvas)
            # Chỉ lưu nếu prefix đã được định nghĩa
            if 'prefix' in locals():
                self.save_processed_image(prefix)

    def save_processed_image(self, prefix):
        output_dir = 'output/face'
        os.makedirs(output_dir, exist_ok=True)
        output_filename = f'{prefix}_' + os.path.basename(self.image_path)
        output_path = os.path.join(output_dir, output_filename)

        counter = 1
        base_filename, ext = os.path.splitext(output_filename)
        while os.path.exists(output_path):
            output_filename = f"{base_filename}_{counter}{ext}"
            output_path = os.path.join(output_dir, output_filename)
            counter += 1

        cv2.imwrite(output_path, self.processed_image)
        print(f"Ảnh {prefix} đã được lưu vào {output_path}")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Chọn màu chữ")
        if color_code[0] is not None:
            # Lưu giá trị RGB được chọn và hiển thị màu đã chọn trên giao diện
            self.font_color = tuple(map(int, color_code[0]))  # Lưu màu RGB dưới dạng tuple (R, G, B)
            self.color_display.config(bg=color_code[1])  # Hiển thị màu đã chọn



    def create_widgets(self):
        self.function_frame = tk.Frame(self.center_frame)
        self.function_frame.pack()

        title_label = tk.Label(self.function_frame, text="Chọn chức năng", font=("Arial", 16))
        title_label.pack(pady=10)

        self.function_var = tk.StringVar()
        self.function_var.set("Grayscale")

        functions = ["Grayscale", "Sepia", "Color Swap", "Extract Color", "Face Crop", "Face Crop (Raspi)", "Face Detection", "Face Detect (Save)"
            , "Face Detect (Draw Rectangle)", "3x3 Filter", "Average Color" , "Combine Photos","Print Text" , "Resize Image" , "SIFT Feature Matching" , "Watershed"]

        self.function_menu = ttk.Combobox(self.function_frame, textvariable=self.function_var, values=functions, state="readonly")
        self.function_menu.pack(pady=5)
        self.function_menu.bind("<<ComboboxSelected>>", self.on_function_select)

        self.params_frame = tk.Frame(self.function_frame)
        self.params_frame.pack(pady=5)

        apply_button = tk.Button(self.function_frame, text="Áp dụng", width=20, command=self.apply_function)
        apply_button.pack(pady=10)

        self.on_function_select()

    def on_function_select(self, event=None):
        # Xóa các widget hiện có trong params_frame để chuẩn bị hiển thị các widget mới
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        selected_function = self.function_var.get()

        # Hiển thị nút chọn ảnh khi chọn Combine Photos
        if selected_function == "Combine Photos":
            self.combine_image_button.pack(side=tk.TOP, pady=10)
            self.selected_images.clear()  # Đảm bảo danh sách ảnh bắt đầu từ đầu
        else:
            self.combine_image_button.pack_forget()  # Ẩn nút nếu không phải Combine Photos

        # Thêm các trường nhập liệu cho Extract Color
        if selected_function == "Extract Color":
            # Tạo các ô nhập liệu cho tham số h_min, h_max, s_th, v_th
            h_frame = tk.Frame(self.params_frame)
            h_frame.pack(pady=2)

            h_min_label = tk.Label(h_frame, text="H Min (0-179):")
            h_min_label.pack(side=tk.LEFT)
            self.h_min_entry = tk.Entry(h_frame, width=5)
            self.h_min_entry.insert(0, "0")  # Giá trị mặc định
            self.h_min_entry.pack(side=tk.LEFT)

            h_max_label = tk.Label(h_frame, text="H Max (0-179):")
            h_max_label.pack(side=tk.LEFT)
            self.h_max_entry = tk.Entry(h_frame, width=5)
            self.h_max_entry.insert(0, "179")  # Giá trị mặc định
            self.h_max_entry.pack(side=tk.LEFT)

            s_frame = tk.Frame(self.params_frame)
            s_frame.pack(pady=2)

            s_th_label = tk.Label(s_frame, text="S Threshold (0-255):")
            s_th_label.pack(side=tk.LEFT)
            self.s_th_entry = tk.Entry(s_frame, width=5)
            self.s_th_entry.insert(0, "0")  # Giá trị mặc định
            self.s_th_entry.pack(side=tk.LEFT)

            v_frame = tk.Frame(self.params_frame)
            v_frame.pack(pady=2)

            v_th_label = tk.Label(v_frame, text="V Threshold (0-255):")
            v_th_label.pack(side=tk.LEFT)
            self.v_th_entry = tk.Entry(v_frame, width=5)
            self.v_th_entry.insert(0, "0")  # Giá trị mặc định
            self.v_th_entry.pack(side=tk.LEFT)

        # Thêm lựa chọn không gian màu cho chức năng "Average Color"
        elif selected_function == "Average Color":
            color_choice_label = tk.Label(self.params_frame, text="Chọn không gian màu:")
            color_choice_label.pack(side=tk.LEFT)

            # Khởi tạo self.color_space_var để lưu trữ tùy chọn màu nếu chưa tồn tại
            if not hasattr(self, 'color_space_var'):
                self.color_space_var = tk.StringVar(value="rgb")  # Thiết lập mặc định là 'rgb'

            # Tạo combobox cho người dùng chọn giữa 'rgb' và 'hsv'
            color_choices = ["rgb", "hsv"]
            color_space_menu = ttk.Combobox(self.params_frame, textvariable=self.color_space_var, values=color_choices,
                                            state="readonly")
            color_space_menu.pack(side=tk.LEFT)


        elif selected_function == "Print Text":

            # Trường nhập liệu cho văn bản

            text_label = tk.Label(self.params_frame, text="Text:")

            text_label.pack(side=tk.LEFT)

            self.text_entry = tk.Entry(self.params_frame, width=20)

            self.text_entry.pack(side=tk.LEFT, padx=5)

            # Nút chọn màu sắc

            color_label = tk.Label(self.params_frame, text="Color:")

            color_label.pack(side=tk.LEFT, padx=5)

            self.color_display = tk.Label(self.params_frame, width=3, height=1, bg="#ffffff")

            self.color_display.pack(side=tk.LEFT)

            color_button = tk.Button(self.params_frame, text="Chọn màu", command=self.choose_color)

            color_button.pack(side=tk.LEFT, padx=5)

            # Trường nhập liệu cho kích cỡ chữ

            font_size_label = tk.Label(self.params_frame, text="Font Size:")

            font_size_label.pack(side=tk.LEFT, padx=5)

            self.font_size_entry = tk.Entry(self.params_frame, width=5)

            self.font_size_entry.insert(0, "20")  # Kích thước mặc định

            self.font_size_entry.pack(side=tk.LEFT)

        elif selected_function == "Resize Image":
            w_ratio_label = tk.Label(self.params_frame, text="Width Ratio (%):")
            w_ratio_label.pack(side=tk.LEFT)
            self.w_ratio_entry = tk.Entry(self.params_frame, width=5)
            self.w_ratio_entry.insert(0, "100")  # Giá trị mặc định
            self.w_ratio_entry.pack(side=tk.LEFT, padx=5)

            h_ratio_label = tk.Label(self.params_frame, text="Height Ratio (%):")
            h_ratio_label.pack(side=tk.LEFT)
            self.h_ratio_entry = tk.Entry(self.params_frame, width=5)
            self.h_ratio_entry.insert(0, "100")  # Giá trị mặc định
            self.h_ratio_entry.pack(side=tk.LEFT)
        elif selected_function == "SIFT Feature Matching":
                self.is_sift_feature_matching = True
                self.image_selection_stage = 1  # Đặt lại để chọn từ đầu
                self.image_path1 = None
                self.image_path2 = None
        else:
            self.is_sift_feature_matching = False

    def open_camera_face_detection(self):
        face_detect_camera()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)

    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
