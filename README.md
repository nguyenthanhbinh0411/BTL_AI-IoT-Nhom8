# Hệ Thống Nhận Diện Chống Đẩy

Dự án này là một hệ thống nhận diện chống đẩy sử dụng thị giác máy tính và học máy để đếm số lần chống đẩy và nhận diện người dùng. Hệ thống bao gồm giao diện web để giám sát thời gian thực và cơ sở dữ liệu để lưu trữ thông tin người dùng và nhật ký chống đẩy.

## Mục Lục
- [Cài Đặt](#cài-đặt)
- [Thiết Lập Cơ Sở Dữ Liệu](#thiết-lập-cơ-sở-dữ-liệu)
- [Chạy Ứng Dụng](#chạy-ứng-dụng)
- [Sử Dụng](#sử-dụng)
- [Các API](#các-api)
- [Huấn Luyện Mô Hình](#huấn-luyện-mô-hình)
- [Thu Thập Dữ Liệu Khuôn Mặt](#thu-thập-dữ-liệu-khuôn-mặt)
- [Xem Thành Tích và Lịch Sử](#xem-thành-tích-và-lịch-sử)

## Cài Đặt

1. **Clone repository:**
    ```sh
    git clone https://github.com/yourusername/PushUpRecognition.git
    cd PushUpRecognition
    ```

2. **Cài đặt các gói Python cần thiết:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Cài đặt MySQL:**
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
