
<h1 align="center">Hệ Thống Nhận Diện Chống Đẩy</h1>

<div align="center">

 <img src="https://github.com/user-attachments/assets/a7ad8c17-5216-4f9c-9bc5-715bfdc7283a"  width="200">
 <img src="https://github.com/user-attachments/assets/4ae892ff-d1c4-479f-8376-697cc9364a5d" width="200">


[![Made by AIoTLab](https://img.shields.io/badge/Made%20by%20AIoTLab-blue?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Fit DNU](https://img.shields.io/badge/Fit%20DNU-green?style=for-the-badge)](https://fitdnu.net/)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

</div>


Dự án này là một hệ thống nhận diện chống đẩy sử dụng thị giác máy tính và học máy để đếm số lần chống đẩy và nhận diện người dùng. Hệ thống bao gồm giao diện web để giám sát thời gian thực và cơ sở dữ liệu để lưu trữ thông tin người dùng và nhật ký chống đẩy.

## Mục Lục

- [Sơ Đồ Hệ Thống](#sơ-đồ-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Thiết Lập Cơ Sở Dữ Liệu](#thiết-lập-cơ-sở-dữ-liệu)
- [Chạy Ứng Dụng](#chạy-ứng-dụng)
- [Sử Dụng](#sử-dụng)
- [Các API](#các-api)
- [Huấn Luyện Mô Hình](#huấn-luyện-mô-hình)
- [Thu Thập Dữ Liệu Khuôn Mặt](#thu-thập-dữ-liệu-khuôn-mặt)
- [Xem Thành Tích và Lịch Sử](#xem-thành-tích-và-lịch-sử)
- [Giới Thiệu Các Chức Năng](#giới-thiệu-các-chức-năng)
- [Poster](#poster)

## Sơ Đồ Hệ Thống

![image](https://github.com/user-attachments/assets/bef6feb0-ed91-4cfc-8ddd-57ea1e9e8614)

## Cài Đặt

1. **Clone repository:**

   ```sh
   git clone https://github.com/nguyenthanhbinh0411/BTL_AI-IoT-Nhom8.git
   cd BTL_AI-IoT-Nhom8
   ```

2. **Cài đặt các gói Python cần thiết:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Cài đặt tất cả các thư viện liên quan (nếu cần):**

   ```sh
   pip install Flask opencv-python numpy pandas mysql-connector-python scikit-learn matplotlib dlib
   ```

4. **Cài đặt MySQL:**
   - Tải và cài đặt MySQL từ [MySQL Downloads](https://dev.mysql.com/downloads/installer/).
   - Tạo một người dùng và cơ sở dữ liệu MySQL cho dự án.

## Thiết Lập Cơ Sở Dữ Liệu

1. **Tạo và thiết lập cơ sở dữ liệu:**
   - Mở file `database_setup.sql` và chỉnh sửa tên người dùng và mật khẩu MySQL nếu cần.
   - Chạy script SQL để tạo cơ sở dữ liệu và các bảng:
   ```sh
   mysql -u root -p < database_setup.sql
   ```

## Chạy Ứng Dụng

1. **Khởi động ứng dụng Flask:**

   ```sh
   python video.py
   ```

2. **Truy cập giao diện web:**
   - Mở trình duyệt web và truy cập `http://localhost:5000`.

## Sử Dụng

### Giám Sát Thời Gian Thực

- Trang chính hiển thị luồng video thời gian thực từ camera.
- Hệ thống sẽ nhận diện người dùng và đếm số lần chống đẩy.
- Người dùng có thể xác nhận danh tính, lưu số lần chống đẩy và xem lịch sử của mình.

### Các API

- **`/status`**: Lấy trạng thái hiện tại của hệ thống nhận diện chống đẩy.
- **`/save`**: Lưu số lần chống đẩy hiện tại vào cơ sở dữ liệu.
- **`/confirm`**: Xác nhận người dùng hiện tại.
- **`/change_user`**: Đổi người dùng hiện tại.
- **`/collect_face_data`**: Thu thập dữ liệu khuôn mặt cho người dùng mới.
- **`/train_model`**: Huấn luyện mô hình nhận diện khuôn mặt.
- **`/history`**: Lấy lịch sử chống đẩy của người dùng đã xác nhận.
- **`/achievements`**: Lấy thành tích của tất cả người dùng.
- **`/students`**: Lấy danh sách tất cả học sinh.

### Huấn Luyện Mô Hình

1. **Huấn luyện mô hình nhận diện chống đẩy:**

   - Mô hình được huấn luyện bằng script `Train_Pushup/train.py`.
   - Chỉnh sửa script nếu cần và chạy nó:

   ```sh
   python Train_Pushup/train.py
   ```

2. **Huấn luyện mô hình nhận diện khuôn mặt:**
   - Mô hình được huấn luyện bằng script `Train_FaceRecognition/train_model.py`.
   - Chỉnh sửa script nếu cần và chạy nó:
   ```sh
   python Train_FaceRecognition/train_model.py
   ```

### Thu Thập Dữ Liệu Khuôn Mặt

1. **Thu thập dữ liệu khuôn mặt cho người dùng mới:**
   - Sử dụng giao diện web để thu thập dữ liệu khuôn mặt.
   - Hoặc chạy script `Train_FaceRecognition/collect_face_data.py`:
   ```sh
   python Train_FaceRecognition/collect_face_data.py
   ```

### Xem Thành Tích và Lịch Sử

- Sử dụng giao diện web để xem thành tích và lịch sử của người dùng.
- Hoặc sử dụng các API để lấy dữ liệu dưới dạng JSON.

## Giới Thiệu Các Chức Năng

### 🎥 Giám Sát Thời Gian Thực

- Hiển thị luồng video thời gian thực từ camera.
- Nhận diện người dùng và đếm số lần chống đẩy.

### 🗂️ Quản Lý Dữ Liệu

- Lưu trữ thông tin người dùng và lịch sử chống đẩy vào cơ sở dữ liệu.
- Cung cấp API để truy xuất dữ liệu.

### 🤖 Huấn Luyện Mô Hình

- Huấn luyện mô hình nhận diện chống đẩy và khuôn mặt.
- Thu thập dữ liệu khuôn mặt cho người dùng mới.

### 📊 Xem Thành Tích và Lịch Sử

- Hiển thị thành tích và lịch sử chống đẩy của người dùng qua giao diện web bằng API.

## Poster

![Nhom8_AI IoT](https://github.com/user-attachments/assets/1795a590-381a-48f6-83eb-4aef2516d5c1)
