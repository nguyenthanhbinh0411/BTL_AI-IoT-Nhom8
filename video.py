import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import mysql.connector
import face_recognition
import pickle
from flask import Flask, render_template, Response, jsonify, request
from database import get_user_id, log_pushups
import os
import subprocess  
import json  
import pygame  # Import pygame for playing audio files
import time  # Import time for sleep
import threading  # Import threading for timers

app = Flask(__name__)

# Initialize pygame mixer
pygame.mixer.init()

# Cấu hình TensorFlow để dùng GPU nếu có
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Thanhbinh12",  # Thay bằng mật khẩu MySQL
    database="pushups_db"
)
cursor = db.cursor()

# Load mô hình nhận diện khuôn mặt
with open("face_model.pkl", "rb") as f:
    data = pickle.load(f)
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Load mô hình LSTM nhận diện chống đẩy
model = tf.keras.models.load_model("pushup_lstm_model.h5")

# Khởi tạo Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Biến toàn cục để lưu trạng thái
pushup_count = 0
prev_label = None
buffer_frames = []
current_user = "Unknown"  # Người tập hiện tại
confirmed_user = "Unknown"  # Người tập đã xác nhận
frame_count = 0  # Đếm frame để giảm tải nhận diện khuôn mặt
status_text = "Neutral"
result_text = "Fail"
stable_position_frames = 0  # Add this line to track stable position frames
counting_enabled = False  # Add this line to control counting
countdown_time = 0  # Add this line to track countdown time

# Khởi tạo camera
def initialize_camera():
    global cap  # Declare cap as global
    cap = cv2.VideoCapture(0)  # Sử dụng camera mặc định
    if not cap.isOpened():
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Thử mở camera khác
    if not cap.isOpened():
        raise RuntimeError("Không thể mở camera!")
    return cap

cap = initialize_camera()

def recognize_face(frame):
    """Nhận diện khuôn mặt và cập nhật tên người tập"""
    global current_user
    if confirmed_user == "Unknown":  # Chỉ nhận diện nếu chưa xác nhận người tập
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = "Unknown"

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                confidence = int((1 - face_distances[best_match_index]) * 100)

                if matches[best_match_index] and confidence >= 60:
                    name = known_face_names[best_match_index]

            current_user = name


def extract_keypoints(image):
    """Trích xuất keypoints từ Mediapipe Pose"""
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        keypoints = np.array([[lm.x, lm.y] for lm in results.pose_landmarks.landmark]).flatten()
        return keypoints, results
    return None, None


def generate_frames():
    """Luồng xử lý video cho Flask"""
    global pushup_count, prev_label, buffer_frames, frame_count, status_text, result_text, counting_enabled, countdown_time

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Lỗi: Không thể lấy khung hình từ camera!")
            break

        frame = cv2.flip(frame, 1)  # Lật ngang

        # Nhận diện khuôn mặt mỗi 30 frames
        if frame_count % 30 == 0:
            recognize_face(frame)
        
        frame_count += 1

        if current_user != "Unknown" and confirmed_user != "Unknown":
            keypoints, results = extract_keypoints(frame)
            if keypoints is not None:
                keypoints = keypoints.reshape(1, 1, -1)

                # Dự đoán bằng mô hình LSTM
                prediction = model.predict(keypoints)
                label = np.argmax(prediction)

                buffer_frames.append(label)
                if len(buffer_frames) > 5:
                    buffer_frames.pop(0)

                # Đếm chống đẩy nếu counting_enabled là True
                if counting_enabled and prev_label == 0 and label == 1 and buffer_frames.count(0) >= 3:
                    pushup_count += 1

                prev_label = label

                # Cập nhật trạng thái
                status_text = "Push-Up" if label == 1 else "Push-Down"
                result_text = "Pass" if pushup_count >= 10 else "Fail"

                # Vẽ khung xương Pose
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()  # Giải phóng camera khi Flask tắt

def countdown_timer():
    """Giảm thời gian đếm ngược mỗi giây"""
    global countdown_time
    while countdown_time > 0:
        time.sleep(1)
        countdown_time -= 1

@app.route('/status')
def status():
    """Gửi trạng thái pushup về giao diện"""
    if current_user != "Unknown":
        cursor.execute("SELECT msv, class FROM students WHERE name = %s", (current_user,))
        user_info = cursor.fetchone()
        msv = user_info[0] if user_info else "N/A"
        class_name = user_info[1] if user_info else "N/A"
    else:
        msv = "N/A"
        class_name = "N/A"
    
    return jsonify({
        "user": current_user,
        "msv": msv,
        "class": class_name,
        "status": status_text,
        "pushup_count": pushup_count,
        "result": result_text,
        "confirmed_user": confirmed_user  # Add this line
    })


@app.route('/save', methods=['POST'])
def save():
    """Lưu kết quả chống đẩy vào database và reset kết quả"""
    global pushup_count, status_text, result_text
    if current_user != "Unknown":
        log_pushups(current_user, pushup_count, result_text)  # Include result_text as status
        response_result = result_text  # Capture the result before resetting
        pushup_count = 0
        status_text = "Neutral"
        result_text = "Fail"
        
        # Play completion audio first
        pygame.mixer.music.load("hoanthanh.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        # Play audio based on result
        if response_result == "Pass":
            pygame.mixer.music.load("ketquadat.mp3")
        else:
            pygame.mixer.music.load("ketquakhongdat.mp3")
        pygame.mixer.music.play()
        
        return jsonify({"message": "Lưu kết quả thành công!", "result": response_result})
    return jsonify({"message": "Không thể lưu kết quả. Người tập chưa được xác định."})

@app.route('/confirm', methods=['POST'])
def confirm():
    """Xác nhận người tập hiện tại"""
    global confirmed_user, current_user, counting_enabled, countdown_time
    if current_user != "Unknown":
        confirmed_user = current_user
        user_id = get_user_id(confirmed_user)
        print(f"Confirmed user: {confirmed_user}")
        
        # Play chuanbi.mp3
        pygame.mixer.music.load("chuanbi.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        # Wait for 5 seconds before playing batdau.mp3
        time.sleep(5)
        
        # Play batdau.mp3
        pygame.mixer.music.load("batdau.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        # Enable counting and set countdown time
        counting_enabled = True
        countdown_time = 30
        
        # Start countdown timer in a separate thread
        threading.Thread(target=countdown_timer).start()
        threading.Timer(30, stop_counting).start()
        
        return jsonify({"message": f"Người tập hiện tại: {confirmed_user} ,hãy vào vị trí để thực hành bài thi"})
    return jsonify({"message": "Không thể xác nhận. Người tập chưa được xác định."})

def stop_counting():
    """Dừng đếm và phát âm thanh hết giờ"""
    global counting_enabled
    counting_enabled = False
    pygame.mixer.music.load("hetgio.mp3")
    pygame.mixer.music.play()

@app.route('/countdown')
def countdown():
    """API để gửi thời gian đếm ngược về giao diện"""
    global countdown_time
    return jsonify({"countdown": countdown_time})

@app.route('/change_user', methods=['POST'])
def change_user():
    """Đổi người tập"""
    global current_user, confirmed_user, pushup_count, status_text, result_text
    current_user = "Unknown"
    confirmed_user = "Unknown"
    pushup_count = 0
    status_text = "Neutral"
    result_text = "Fail"
    return jsonify({"message": "Đã đổi người tập."})

@app.route('/')
def index():
    """Trang chính hiển thị video"""
    return render_template('index.html')


@app.route('/video')
def video():
    """Luồng video"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')

def collect_face_data(name):
    """Thu thập dữ liệu khuôn mặt cho người tập mới"""
    global cap  # Declare cap as global
    data_dir = "face_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    person_dir = os.path.join(data_dir, name)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    count = 0
    print("Nhìn vào camera và chờ...")

    while count < 100:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            file_name = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(file_name, face_img)
            count += 1
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Collected: {count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Collecting Faces", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Đã thu thập xong {count} ảnh cho {name}")

    # Reinitialize the camera after collecting face data
    cap = initialize_camera()

def train_model():
    """Huấn luyện mô hình nhận diện khuôn mặt"""
    global cap  # Declare cap as global
    data_dir = r"C:\BTL_AI_IOT\9\face_data"
    model_file = "face_model.pkl"
    
    # Release the camera before training
    if cap.isOpened():
        cap.release()
    
    known_face_encodings = []
    known_face_names = []
    total_images = sum([len(files) for r, d, files in os.listdir(data_dir)])
    processed_images = 0

    for person_name in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(person_name)
            
            processed_images += 1
            progress = (processed_images / total_images) * 100
            print(f"Progress: {progress:.2f}%")
                
    data = {"encodings": known_face_encodings, "names": known_face_names}
    with open(model_file, "wb") as f:
        pickle.dump(data, f)
    
    print("Huấn luyện mô hình hoàn tất!")
    
    # Reinitialize the camera after training
    cap = initialize_camera()

@app.route('/collect_face_data', methods=['POST'])
def collect_face_data_route():
    """API để thu thập dữ liệu khuôn mặt"""
    name = request.form.get('name')
    msv = request.form.get('msv')
    class_name = request.form.get('class_name')
    if name and msv and class_name:
        collect_face_data(name)
        get_user_id(name, msv, class_name)
        return jsonify({"message": f"Đã thu thập dữ liệu khuôn mặt cho {name}"}), 200
    return jsonify({"message": "Tên, MSV và lớp không được để trống"}), 400

@app.route('/train_model', methods=['POST'])
def train_model_route():
    """API để huấn luyện mô hình nhận diện khuôn mặt"""
    try:
        # Call the external train_model.py script
        result = subprocess.run(["python", "train_model.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Huấn luyện mô hình hoàn tất!"}), 200
        else:
            return jsonify({"error": f"Lỗi khi huấn luyện mô hình: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi khi huấn luyện mô hình: {str(e)}"}), 500

@app.route('/history', methods=['POST'])
def history_route():
    """API để hiển thị lịch sử người tập"""
    try:
        # Pass the confirmed user to the history.py script
        result = subprocess.run(["python", "history.py", confirmed_user], capture_output=True, text=True)
        if result.returncode == 0:
            history_data = result.stdout
            return jsonify(json.loads(history_data)), 200
        else:
            return jsonify({"error": f"Lỗi khi hiển thị lịch sử: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi khi hiển thị lịch sử: {str(e)}"}), 500

@app.route('/achievements', methods=['GET'])
def achievements_route():
    """API để hiển thị thành tích cao nhất của từng người tập"""
    try:
        # Call the external achievements.py script
        result = subprocess.run(["python", "achievements.py"], capture_output=True, text=True)
        if result.returncode == 0:
            achievements_data = result.stdout
            return jsonify(json.loads(achievements_data)), 200
        else:
            return jsonify({"error": f"Lỗi khi hiển thị thành tích: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi khi hiển thị thành tích: {str(e)}"}), 500

@app.route('/students', methods=['GET'])
def students_route():
    """API để hiển thị danh sách học sinh"""
    try:
        # Call the external students.py script
        result = subprocess.run(["python", "students.py"], capture_output=True, text=True)
        if result.returncode == 0:
            students_data = result.stdout
            return jsonify(json.loads(students_data)), 200
        else:
            return jsonify({"error": f"Lỗi khi hiển thị danh sách học sinh: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": f"Lỗi khi hiển thị danh sách học sinh: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
