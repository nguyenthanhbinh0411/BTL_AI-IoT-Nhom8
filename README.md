# BTL AI & IoT - Nhóm 8

## Giới thiệu
Dự án này bao gồm các chức năng nhận diện khuôn mặt và đếm số lần chống đẩy sử dụng AI và IoT. Dự án được xây dựng bằng Python và sử dụng các thư viện như OpenCV, Mediapipe, TensorFlow, Flask, và MySQL.

## Cài đặt
1. **Clone repository:**
    ```bash
    git clone <repository-url>
    cd BTL_AI_IOT/BTL_AI&IoT-Nhom8
    ```

2. **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Cấu hình MySQL:**
    - Tạo database `pushups_db`.
    - Chạy các script SQL để tạo các bảng cần thiết.

4. **Cấu hình TensorFlow để sử dụng GPU (nếu có):**
    ```python
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    ```

## Sử dụng
### 1. Thu thập dữ liệu khuôn mặt
Chạy script `collect_face_data.py` để thu thập dữ liệu khuôn mặt:
```bash
python collect_face_data.py
```
Nhập tên người cần thu thập dữ liệu khi được yêu cầu.

### 2. Huấn luyện mô hình nhận diện khuôn mặt
Chạy script `train_model.py` để huấn luyện mô hình nhận diện khuôn mặt:
```bash
python train_model.py
```

### 3. Xử lý video chống đẩy
Chạy script `frames.py` để xử lý video và trích xuất các frame:
```bash
python frames.py
```

### 4. Huấn luyện mô hình nhận diện chống đẩy
Chạy script `train.py` để huấn luyện mô hình nhận diện chống đẩy:
```bash
python train.py
```

### 5. Chạy ứng dụng Flask
Chạy script `video.py` để khởi động ứng dụng Flask:
```bash
python video.py
```
Mở trình duyệt và truy cập `http://localhost:5000` để sử dụng ứng dụng.

## API
### 1. Thu thập dữ liệu khuôn mặt
- **Endpoint:** `/collect_face_data`
- **Method:** `POST`
- **Parameters:** `name`, `msv`, `class_name`

### 2. Huấn luyện mô hình nhận diện khuôn mặt
- **Endpoint:** `/train_model`
- **Method:** `POST`

### 3. Xác nhận người tập
- **Endpoint:** `/confirm`
- **Method:** `POST`

### 4. Lưu kết quả chống đẩy
- **Endpoint:** `/save`
- **Method:** `POST`

### 5. Hiển thị lịch sử người tập
- **Endpoint:** `/history`
- **Method:** `POST`

### 6. Hiển thị thành tích cao nhất
- **Endpoint:** `/achievements`
- **Method:** `GET`

### 7. Hiển thị danh sách học sinh
- **Endpoint:** `/students`
- **Method:** `GET`

## Đóng góp
Nếu bạn muốn đóng góp cho dự án, vui lòng tạo pull request hoặc mở issue mới.

## Liên hệ
Nếu có bất kỳ câu hỏi nào, vui lòng liên hệ với chúng tôi qua email: [email@example.com]
