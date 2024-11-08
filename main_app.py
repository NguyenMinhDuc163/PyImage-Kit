import tkinter as tk
from tkinter import filedialog, ttk, messagebox, colorchooser
from PIL import Image, ImageTk

import cv2
import numpy as np
import os
import sys



from src.color_gray import color_gray
from src.color_sepia import color_sepia
from src.color_swap import color_swap
from src.extract_color import extract_color
from src.face_crop import detect
from src.face_crop_raspi import face_detect
from src.face_detection import face_detect_draw_rectangle
from src.face_detection_camera import face_detect_camera
from src.photo_cat import combine_photos

from src.filter_3by3 import apply_3x3_filter
from src.photo_date_print import print_text
from src.watershed import watershed
from src.photo_exif_date_print import get_date_of_image, put_date, save_with_unique_name, get_exif_of_image



def measure_color_average(image_path, color_space="rgb"):
    
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        print(f"Không thể mở ảnh {image_path}")
        return None

    
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV) if color_space == "hsv" else bgr_img

    
    average_color = [0, 0, 0]
    for i in range(3):
        extract_img = hsv_img[:, :, i] if color_space == "hsv" else bgr_img[:, :, i]
        extract_img = extract_img[extract_img > 0]
        average_color[i] = np.average(extract_img)

    
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
        self.image_selection_stage = 1  
        self.image_path1 = None  
        self.image_path2 = None  

        
        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.selected_images = []  

        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        
        self.selected_images_frame = tk.Frame(self.left_frame)
        self.selected_images_frame.pack()

        
        self.selected_image_labels = []

        
        self.combine_image_button = tk.Button(root, text="Chọn ảnh cho Combine Photos",
                                              command=self.select_image_for_combine)
        self.combine_image_button.pack(side=tk.TOP, pady=10)
        self.combine_image_button.pack_forget()  

        
        self.select_image_button = tk.Button(root, text="Chọn ảnh", command=self.load_image)
        self.select_image_button.pack(side=tk.TOP, pady=10)

        
        self.camera_button = tk.Button(root, text="Mở Camera Phát Hiện Khuôn Mặt",
                                       command=self.open_camera_face_detection)
        self.camera_button.pack(side=tk.TOP, pady=10)

        
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(side=tk.LEFT, padx=10, pady=10)

        
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        
        self.original_canvas = tk.Label(self.left_frame)
        self.original_canvas.pack()

        self.processed_canvas = tk.Label(self.right_frame)
        self.processed_canvas.pack()

        
        self.create_widgets()

        self.clear_button = tk.Button(self.root, text="Clear Data", command=self.clear_data)
        self.clear_button.pack(side=tk.BOTTOM, anchor='se', padx=10, pady=10)


    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.is_sift_feature_matching:
                
                if self.image_selection_stage == 1:
                    
                    self.image_path1 = file_path
                    self.original_image = cv2.imread(file_path)
                    if self.original_image is None:
                        print(f"Không thể mở tệp ảnh: {file_path}")
                        return
                    self.show_image(self.original_image, self.original_canvas)
                    print("Ảnh thứ nhất đã được chọn.")
                    self.image_selection_stage = 2  

                elif self.image_selection_stage == 2:
                    
                    self.image_path2 = file_path
                    self.processed_image = cv2.imread(file_path)
                    if self.processed_image is None:
                        print(f"Không thể mở tệp ảnh: {file_path}")
                        return
                    self.show_image(self.processed_image, self.processed_canvas)
                    print("Ảnh thứ hai đã được chọn.")
                    self.image_selection_stage = 1  
                    
                    self.apply_function()
            else:
                
                self.image_path = file_path
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    print(f"Không thể mở tệp ảnh: {file_path}")
                    return
                self.show_image(self.original_image, self.original_canvas)
                self.processed_image = None
                self.processed_canvas.config(image='')

    def display_exif_info(self, image_path):
        
        exif_info = get_exif_of_image(image_path)

        
        self.exif_text.delete('1.0', tk.END)

        
        for key, value in exif_info.items():
            self.exif_text.insert(tk.END, f"{key}: {value}\n")

    def resize_image(self, src, w_ratio, h_ratio):
        """Resize image based on width and height ratio."""
        height, width = src.shape[:2]
        resized_img = cv2.resize(src, (int(width * w_ratio / 100), int(height * h_ratio / 100)))
        return resized_img
    def select_image_for_combine(self):
        file_path = filedialog.askopenfilename(title="Chọn một ảnh")
        if file_path:
            
            self.selected_images.append(file_path)

            
            image = cv2.imread(file_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_pil.thumbnail((100, 100))  
            image_tk = ImageTk.PhotoImage(image_pil)

            label = tk.Label(self.selected_images_frame, image=image_tk)
            label.image = image_tk  
            label.pack(side=tk.LEFT, padx=5, pady=5)

            
            self.selected_image_labels.append(label)

            print(f"Ảnh đã chọn: {file_path}")

            
            if len(self.selected_images) == 4:
                self.apply_function()  

    def show_image(self, image, canvas):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil.thumbnail((300, 300))
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.image = image_tk  
        canvas.config(image=image_tk)

    def combine_photos(self):
        combined_img = combine_photos(self.selected_images)
        if combined_img is not None:
            self.processed_image = combined_img
            self.show_image(self.processed_image, self.processed_canvas)
            print("Ảnh đã được kết hợp và hiển thị.")
            self.selected_images.clear()  

    def clear_data(self):
        
        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.image_path1 = None
        self.image_path2 = None

        
        self.original_canvas.config(image='')
        self.processed_canvas.config(image='')

        
        self.selected_images.clear()
        for label in self.selected_image_labels:
            label.pack_forget()  
            label.destroy()  
        self.selected_image_labels.clear()

        
        print("Dữ liệu đã được xóa và giao diện đã được làm mới.")

    def sift_matching(self, img1_path, img2_path):
        
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        if img1 is None or img2 is None:
            messagebox.showerror("Error", "Không thể mở một hoặc cả hai ảnh.")
            return None

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        
        matcher = cv2.DescriptorMatcher_create("FlannBased")
        matches = matcher.match(des1, des2)

        
        output_img = self.drawMatches(img1, kp1, img2, kp2, matches[:100])

        
        output_dir = 'output/other'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'matched_features.jpg')
        cv2.imwrite(output_path, output_img)
        print(f"Matched features image saved to {output_path}")

        return output_img  

    def drawMatches(self, img1, kp1, img2, kp2, matches):
        rows1, cols1 = img1.shape[:2]
        rows2, cols2 = img2.shape[:2]

        
        out = np.zeros((max([rows1, rows2]), cols1 + cols2, 3), dtype='uint8')
        out[:rows1, :cols1, :] = img1
        out[:rows2, cols1:cols1 + cols2, :] = img2

        
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
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước khi áp dụng chức năng.")
            print("Vui lòng chọn ảnh trước!")
            return

        selected_function = self.function_var.get()

        
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
            
            if not hasattr(self, 'h_min_entry') or not hasattr(self, 'h_max_entry') or not hasattr(self,
                                                                                                   's_th_entry') or not hasattr(
                    self, 'v_th_entry'):
                print("Vui lòng chọn chức năng 'Extract Color' và nhập các giá trị cần thiết.")
                return

            
            try:
                h_min = int(self.h_min_entry.get())
                h_max = int(self.h_max_entry.get())
                s_th = int(self.s_th_entry.get())
                v_th = int(self.v_th_entry.get())
            except ValueError:
                messagebox.showerror("Lỗi giá trị", "Vui lòng nhập các giá trị số nguyên hợp lệ cho các tham số.")
                return

            
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

            
            mask_img = extract_color(self.original_image, h_min, h_max, s_th, v_th)
            output_img = cv2.bitwise_and(self.original_image, self.original_image, mask=mask_img)
            prefix = 'extract'

            
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

                
            combined_img = combine_photos(self.selected_images)
            if combined_img is not None:
                self.processed_image = combined_img
                self.show_image(self.processed_image, self.processed_canvas)
                print("Ảnh đã được kết hợp và hiển thị.")
            return
        elif selected_function == "Print Text":
            
            text = self.text_entry.get()

            
            font_color = getattr(self, 'font_color', (255, 255, 255))

            try:
                font_size = int(self.font_size_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Vui lòng nhập kích thước hợp lệ")
                return

            
            output_img = print_text(self.image_path, text, font_color=font_color, font_size=font_size)
            prefix = "text_printed"  

            
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

            
            output_img = self.resize_image(self.original_image, w_ratio, h_ratio)
            if output_img is not None:
                self.processed_image = output_img
                self.show_image(self.processed_image, self.processed_canvas)
                prefix = "resized"  
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
            
            markers, output_img = watershed(self.original_image)

            
            self.processed_image = output_img
            self.show_image(self.processed_image, self.processed_canvas)
            self.save_processed_image("watershed_image")

            
            output_dir = 'output/other'
            os.makedirs(output_dir, exist_ok=True)
            markers_path = os.path.join(output_dir, "watershed_markers_" + os.path.basename(self.image_path))
            cv2.imwrite(markers_path, markers)
            print(f"Markers saved to {markers_path}")

            print("Watershed processing completed and images saved.")
            return
        elif selected_function == "Print Date from EXIF":
            date = get_date_of_image(self.image_path)

            
            self.display_exif_info(self.image_path)

            if date:
                output_img = put_date(self.image_path, date)
                prefix = "date_exif"
                if output_img is not None:
                    self.processed_image = output_img
                    self.show_image(self.processed_image, self.processed_canvas)
                    save_with_unique_name('output/photo',
                                          f"{date.replace(':', '_').replace(' ', '_')}_{os.path.basename(self.image_path)}",
                                          output_img)
                    print("Ảnh đã được thêm ngày EXIF và lưu lại.")
            else:
                print("Không tìm thấy ngày trong dữ liệu EXIF của ảnh.")
        elif selected_function == "Face Detection":
            output_img = face_detect_draw_rectangle(self.image_path)
            prefix = 'facedetect'
        else:
            print("Vui lòng chọn chức năng hợp lệ.")
            return

        if selected_function not in ["Print Text", "Combine Photos", "Average Color"]:
            
            if 'output_img' in locals():
                self.processed_image = output_img
                self.show_image(self.processed_image, self.processed_canvas)
                if 'prefix' in locals():
                    self.save_processed_image(prefix)


        
        if 'output_img' in locals() and output_img is not None:
            self.processed_image = output_img
            self.show_image(self.processed_image, self.processed_canvas)
            
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
            
            self.font_color = tuple(map(int, color_code[0]))  
            self.color_display.config(bg=color_code[1])  



    def create_widgets(self):
        self.function_frame = tk.Frame(self.center_frame)
        self.function_frame.pack()

        title_label = tk.Label(self.function_frame, text="Chọn chức năng", font=("Arial", 16))
        title_label.pack(pady=10)

        self.function_var = tk.StringVar()
        self.function_var.set("Grayscale")

        functions = ["Grayscale", "Sepia", "Color Swap", "Extract Color", "Face Crop", "Face Crop (Raspi)", "Face Detection", "Face Detect (Save)"
            , "Face Detect (Draw Rectangle)", "3x3 Filter", "Average Color" , "Combine Photos","Print Text" , "Resize Image" , "SIFT Feature Matching" ,
                     "Watershed", "Print Date from EXIF"]

        self.function_menu = ttk.Combobox(self.function_frame, textvariable=self.function_var, values=functions, state="readonly")
        self.function_menu.pack(pady=5)
        self.function_menu.bind("<<ComboboxSelected>>", self.on_function_select)

        self.params_frame = tk.Frame(self.function_frame)
        self.params_frame.pack(pady=5)

        apply_button = tk.Button(self.function_frame, text="Áp dụng", width=20, command=self.apply_function)
        apply_button.pack(pady=10)

        self.on_function_select()

    def on_function_select(self, event=None):
        
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        selected_function = self.function_var.get()

        
        if selected_function == "Combine Photos":
            self.combine_image_button.pack(side=tk.TOP, pady=10)
            self.selected_images.clear()  
        else:
            self.combine_image_button.pack_forget()  

        
        if selected_function == "Extract Color":
            
            h_frame = tk.Frame(self.params_frame)
            h_frame.pack(pady=2)

            h_min_label = tk.Label(h_frame, text="H Min (0-179):")
            h_min_label.pack(side=tk.LEFT)
            self.h_min_entry = tk.Entry(h_frame, width=5)
            self.h_min_entry.insert(0, "0")  
            self.h_min_entry.pack(side=tk.LEFT)

            h_max_label = tk.Label(h_frame, text="H Max (0-179):")
            h_max_label.pack(side=tk.LEFT)
            self.h_max_entry = tk.Entry(h_frame, width=5)
            self.h_max_entry.insert(0, "179")  
            self.h_max_entry.pack(side=tk.LEFT)

            s_frame = tk.Frame(self.params_frame)
            s_frame.pack(pady=2)

            s_th_label = tk.Label(s_frame, text="S Threshold (0-255):")
            s_th_label.pack(side=tk.LEFT)
            self.s_th_entry = tk.Entry(s_frame, width=5)
            self.s_th_entry.insert(0, "0")  
            self.s_th_entry.pack(side=tk.LEFT)

            v_frame = tk.Frame(self.params_frame)
            v_frame.pack(pady=2)

            v_th_label = tk.Label(v_frame, text="V Threshold (0-255):")
            v_th_label.pack(side=tk.LEFT)
            self.v_th_entry = tk.Entry(v_frame, width=5)
            self.v_th_entry.insert(0, "0")  
            self.v_th_entry.pack(side=tk.LEFT)

        
        elif selected_function == "Average Color":
            color_choice_label = tk.Label(self.params_frame, text="Chọn không gian màu:")
            color_choice_label.pack(side=tk.LEFT)

            
            if not hasattr(self, 'color_space_var'):
                self.color_space_var = tk.StringVar(value="rgb")  

            
            color_choices = ["rgb", "hsv"]
            color_space_menu = ttk.Combobox(self.params_frame, textvariable=self.color_space_var, values=color_choices,
                                            state="readonly")
            color_space_menu.pack(side=tk.LEFT)


        elif selected_function == "Print Text":

            

            text_label = tk.Label(self.params_frame, text="Text:")

            text_label.pack(side=tk.LEFT)

            self.text_entry = tk.Entry(self.params_frame, width=20)

            self.text_entry.pack(side=tk.LEFT, padx=5)

            

            color_label = tk.Label(self.params_frame, text="Color:")

            color_label.pack(side=tk.LEFT, padx=5)

            self.color_display = tk.Label(self.params_frame, width=3, height=1, bg="#ffffff")

            self.color_display.pack(side=tk.LEFT)

            color_button = tk.Button(self.params_frame, text="Chọn màu", command=self.choose_color)

            color_button.pack(side=tk.LEFT, padx=5)



            font_size_label = tk.Label(self.params_frame, text="Font Size:")

            font_size_label.pack(side=tk.LEFT, padx=5)

            self.font_size_entry = tk.Entry(self.params_frame, width=5)

            self.font_size_entry.insert(0, "20")  

            self.font_size_entry.pack(side=tk.LEFT)

        elif selected_function == "Resize Image":
            w_ratio_label = tk.Label(self.params_frame, text="Width Ratio (%):")
            w_ratio_label.pack(side=tk.LEFT)
            self.w_ratio_entry = tk.Entry(self.params_frame, width=5)
            self.w_ratio_entry.insert(0, "100")  
            self.w_ratio_entry.pack(side=tk.LEFT, padx=5)

            h_ratio_label = tk.Label(self.params_frame, text="Height Ratio (%):")
            h_ratio_label.pack(side=tk.LEFT)
            self.h_ratio_entry = tk.Entry(self.params_frame, width=5)
            self.h_ratio_entry.insert(0, "100")  
            self.h_ratio_entry.pack(side=tk.LEFT)
        elif selected_function == "SIFT Feature Matching":
                self.is_sift_feature_matching = True
                self.image_selection_stage = 1  
                self.image_path1 = None
                self.image_path2 = None


        else:
            self.is_sift_feature_matching = False
        if selected_function == "Print Date from EXIF":
            self.exif_text = tk.Text(self.params_frame, wrap=tk.WORD, width=50, height=10)
            self.exif_text.pack(pady=10)
    def open_camera_face_detection(self):
        face_detect_camera()


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)

    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
