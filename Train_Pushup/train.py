import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Thư mục chứa ảnh đã chia nhãn
DATASET_PATH = "frame/"
LABELS = ["push-down", "push-up"]  # 0: Push-down, 1: Push-up

# Khởi tạo Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def extract_keypoints(image):
    """ Trích xuất keypoints từ ảnh sử dụng Mediapipe Pose """
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        keypoints = np.array([[lm.x, lm.y] for lm in results.pose_landmarks.landmark]).flatten()  # Chuyển thành vector 1D
        return keypoints
    return None

def load_data():
    """ Tải dữ liệu và trích xuất keypoints từ ảnh """
    X, y = [], []
    for label, label_name in enumerate(LABELS):  # 0: push-down, 1: push-up
        folder = os.path.join(DATASET_PATH, str(label))
        for file in os.listdir(folder):
            img_path = os.path.join(folder, file)
            image = cv2.imread(img_path)
            keypoints = extract_keypoints(image)
            if keypoints is not None:
                X.append(keypoints)
                y.append(label)

    X = np.array(X)
    y = np.array(y)
    return X, y

# Load dữ liệu
X, y = load_data()

# Kiểm tra dữ liệu
print(f"Số lượng mẫu: {len(X)}, Số keypoints mỗi mẫu: {X.shape[1]}")

# Chia dữ liệu thành train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Chuẩn hóa dữ liệu
X_train = X_train / np.max(X_train)
X_test = X_test / np.max(X_test)

# Chuyển nhãn thành dạng one-hot encoding
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

# Reshape dữ liệu cho LSTM (samples, timesteps, features)
X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

# Xây dựng mô hình LSTM
model = Sequential([
    LSTM(64, return_sequences=True, activation="relu", input_shape=(1, X_train.shape[2])),
    LSTM(32, return_sequences=False, activation="relu"),
    Dense(16, activation="relu"),
    Dense(2, activation="softmax")  # 2 lớp đầu ra (push-up, push-down)
])

# Compile mô hình
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train mô hình
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Lưu mô hình
model.save("pushup_lstm_model.h5")

# Kiểm tra độ chính xác trên tập test
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Độ chính xác trên tập test: {test_acc * 100:.2f}%")
