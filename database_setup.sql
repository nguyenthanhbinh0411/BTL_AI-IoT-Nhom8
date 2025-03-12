-- Tạo database pushups_db
CREATE DATABASE IF NOT EXISTS pushups_db;

-- Sử dụng database pushups_db
USE pushups_db;

-- Tạo bảng students để lưu thông tin học sinh
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    msv VARCHAR(50) UNIQUE NOT NULL,
    class VARCHAR(100) NOT NULL
);

-- Tạo bảng pushup_logs để lưu thông tin log chống đẩy
CREATE TABLE IF NOT EXISTS pushup_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    pushup_count INT,
    result VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES students(id)
);

-- Thêm cột result vào bảng pushup_logs nếu chưa có
ALTER TABLE pushup_logs ADD COLUMN IF NOT EXISTS result VARCHAR(10);
