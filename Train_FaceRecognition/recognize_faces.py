import cv2
import face_recognition
import pickle
import numpy as np

def recognize_faces():
    # Tải mô hình đã huấn luyện
    try:
        with open("face_model.pkl", "rb") as f:
            data = pickle.load(f)
        known_face_encodings = data["encodings"]
        known_face_names = data["names"]
    except FileNotFoundError:
        print("Chưa tìm thấy mô hình huấn luyện. Vui lòng chạy train_model.py trước!")
        return

    # Khởi động webcam
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    
    # Ngưỡng nhận diện
    tolerance = 0.5  # Điều chỉnh độ khắt khe của face_recognition
    confidence_threshold = 60  # Ngưỡng % để xác định "Unknown"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển đổi sang RGB vì face_recognition dùng RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Tìm vị trí khuôn mặt và tạo encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Nhận diện từng khuôn mặt
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # So sánh với các khuôn mặt đã biết
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
            name = "Unknown"
            confidence = 0

            # Tính khoảng cách khuôn mặt
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                min_distance = face_distances[best_match_index]
                confidence = int((1 - min_distance) * 100)  # Độ tin cậy (%)

                # Chỉ gán tên nếu khớp và độ tin cậy >= 60%
                if matches[best_match_index] and confidence >= confidence_threshold:
                    name = known_face_names[best_match_index]

            # Vẽ khung và tên
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            label = f"{name} ({confidence}%)" if name != "Unknown" else "Unknown"
            cv2.putText(frame, label, (left, top-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # In thông tin debug lên console
            print(f"Detected: {name}, Distance: {min_distance:.2f}, Confidence: {confidence}%")

        cv2.imshow("Face Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()