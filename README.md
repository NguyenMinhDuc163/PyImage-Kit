



- Nguyễn Minh Đức - B21DCCN249

- Lâm Tiến Dưỡng - B21DCCN290

- Vũ Công Duy - B21DCCN302



---





```bash
python -m venv venv
```
**Trên Windows:**

```bash

.\venv\Scripts\activate

```

**Trên macOS/Linux:**

```bash

source venv/bin/activate

```



Sau khi kích hoạt môi trường ảo, cài đặt các gói từ file `requirements.txt`:

```bash

pip install -r requirements.txt

```



Sau khi cài đặt, khởi động ứng dụng bằng lệnh sau:

```bash

python main_app.py

```

Ứng dụng sẽ mở giao diện xử lý ảnh với các chức năng cơ bản.

---



1\. **Nhận diện khuôn mặt, tuổi và giới tính (face_detect_camera)**  

   Phát hiện khuôn mặt trong thời gian thực từ camera, dự đoán giới tính và độ tuổi, hiển thị trực tiếp thông tin trên khung hình và lưu ảnh phát hiện vào thư mục `output/face`.

2\. **Chuyển ảnh sang màu xám (color_gray)**  

   Chuyển đổi hình ảnh thành dạng màu xám, làm nổi bật độ tương phản và chi tiết bằng sắc thái trắng đen.

3\. **Bộ lọc màu nâu (color_sepia)**  

   Áp dụng hiệu ứng màu nâu cổ điển lên ảnh, tạo cảm giác hoài niệm.

4\. **Hoán đổi màu (color_swap)**  

   Hoán đổi các kênh màu để tạo ra hiệu ứng màu sắc độc đáo trên ảnh.

5\. **Trích xuất màu (extract_color)**  

   Chọn và giữ lại một phạm vi màu cụ thể trên ảnh, làm nổi bật màu đó và mờ đi các phần còn lại.

6\. **Cắt khuôn mặt từ ảnh (face_crop, face_crop_raspi, face_crop_simple)**  

   Xác định và cắt khuôn mặt từ ảnh với các phiên bản tối ưu cho Raspberry Pi (`face_crop_raspi`) và phiên bản đơn giản (`face_crop_simple`).

7\. **Phát hiện khuôn mặt (face_detection)**  

   Nhận diện và đánh dấu khuôn mặt bằng hình chữ nhật, giúp xác định nhanh các khuôn mặt trên ảnh.

8\. **Phát hiện khuôn mặt từ camera (face_detection_camera)**  

   Phát hiện khuôn mặt trong thời gian thực từ camera, lưu lại hình ảnh có khuôn mặt được phát hiện.

9\. **Bộ lọc 3x3 (filter_3by3)**  

   Áp dụng bộ lọc 3x3 trên ảnh, có thể sử dụng để làm sắc nét hoặc làm mờ.

10\. **Đo màu trung bình (measure_color_average)**  

    Tính toán màu trung bình của ảnh trong không gian màu RGB hoặc HSV, giúp phân tích đặc điểm màu tổng thể.

11\. **Ghép ảnh (photo_cat)**  

    Kết hợp nhiều ảnh thành một ảnh duy nhất, phù hợp cho tạo album hoặc ghép các ảnh lại với nhau.

12\. **Thêm ngày tháng lên ảnh (photo_date_print)**  

    In ngày tháng lên ảnh, phù hợp cho việc lưu trữ thời gian chụp hoặc đánh dấu ngày tháng.

13\. **In ngày tháng từ dữ liệu EXIF (photo_exif_date_print)**  

    Tự động lấy ngày từ dữ liệu EXIF của ảnh và in lên ảnh, giúp lưu giữ thông tin thời gian chụp.

14\. **Xử lý cơ bản với Pillow và Numpy (pillow_numpy_basic)**  

    Thực hiện các thao tác cơ bản trên ảnh sử dụng Pillow và Numpy, tạo nền tảng cho các xử lý ảnh nâng cao hơn.

15\. **Thay đổi kích thước ảnh (resize)**  

    Thay đổi kích thước ảnh theo tỷ lệ phần trăm của chiều rộng và chiều cao, tối ưu ảnh cho các ứng dụng khác nhau.

16\. **SIFT - So khớp đặc trưng (sift)**  

    Tìm và so khớp các đặc trưng giữa hai ảnh bằng thuật toán SIFT, phù hợp cho nhận diện và so sánh hình ảnh.

17\. **Phân đoạn ảnh bằng Watershed (watershed)**  

    Áp dụng phương pháp Watershed để phân đoạn các vùng khác nhau trên ảnh, giúp phân tích hình dạng và cấu trúc đối tượng.
---



Dự án **Bộ công cụ xử lý cơ bản ảnh bằng Python** cung cấp các chức năng xử lý ảnh thiết yếu, phục vụ việc học tập và nghiên cứu trong lĩnh vực xử lý ảnh. Bộ công cụ này phù hợp với yêu cầu của bài tập lớn môn Xử lý ảnh và có thể mở rộng trong các dự án phân tích và nhận dạng hình ảnh.