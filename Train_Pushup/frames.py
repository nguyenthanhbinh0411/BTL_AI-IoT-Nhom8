import cv2
import os
import numpy as np
import mediapipe as mp

# Khởi tạo Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Thư mục chứa video đầu vào
video_folder = "videos/"
output_folder_pushup = "fram/1/"
output_folder_pushdown = "fram/0/"

os.makedirs(output_folder_pushup, exist_ok=True)
os.makedirs(output_folder_pushdown, exist_ok=True)

def extract_keypoints(image):
    """ Trích xuất keypoints từ frame bằng Mediapipe Pose """
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        keypoints = np.array([[lm.x, lm.y] for lm in results.pose_landmarks.landmark])  # Lấy tọa độ X, Y
        return keypoints
    return None

def calculate_angle(a, b, c):
    """ Tính góc giữa ba điểm a-b-c """
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def classify_pushup(keypoints):
    """
    Xác định tư thế push-up dựa trên vị trí keypoints.
    - Khi push-up (1): Thân người cao hơn, khuỷu tay gần thẳng
    - Khi push-down (0): Người hạ xuống, khuỷu tay gập nhiều
    """
    if keypoints is None:
        return None  # Không xác định được keypoints

    # Lấy các điểm quan trọng: Cả bên trái & bên phải
    left_shoulder, left_elbow, left_hip = keypoints[11], keypoints[13], keypoints[23]
    right_shoulder, right_elbow, right_hip = keypoints[12], keypoints[14], keypoints[24]

    # Tính góc
    left_angle = calculate_angle(left_shoulder, left_elbow, left_hip)
    right_angle = calculate_angle(right_shoulder, right_elbow, right_hip)

    # Chọn góc lớn nhất (tránh lỗi góc đối diện)
    best_angle = max(left_angle, right_angle)

    # Điều chỉnh ngưỡng phân loại
    if best_angle > 160:  # Đẩy lên cao hơn
        return 1  # Push-up
    elif best_angle < 90:  # Hạ thấp xuống
        return 0  # Push-down
    return None  # Không rõ tư thế

def draw_keypoints(image, keypoints):
    """ Vẽ keypoints lên ảnh để kiểm tra """
    for (x, y) in keypoints:
        x, y = int(x * image.shape[1]), int(y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    return image

def process_videos():
    """ Xử lý từng video trong thư mục videos/ """
    for filename in os.listdir(video_folder):
        if filename.endswith((".mp4", ".avi", ".mov")):
            cap = cv2.VideoCapture(os.path.join(video_folder, filename))
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1

                if frame_count % 5 == 0:  # Chỉ lấy mỗi 5 frame để tránh trùng lặp nhiều
                    keypoints = extract_keypoints(frame)
                    label = classify_pushup(keypoints)

                    if keypoints is not None:
                        frame = draw_keypoints(frame, keypoints)  # Vẽ keypoints lên ảnh

                    if label is not None:
                        output_path = os.path.join(
                            output_folder_pushup if label == 1 else output_folder_pushdown,
                            f"{filename}_frame{frame_count}.jpg"
                        )
                        cv2.imwrite(output_path, frame)

            cap.release()

    print("Xử lý video hoàn tất!")

# Chạy chương trình
process_videos()
