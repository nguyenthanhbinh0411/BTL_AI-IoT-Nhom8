import cv2
import os

def collect_face_data():
    # Tạo thư mục để lưu dữ liệu nếu chưa có
    data_dir = "face_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Nhập tên người cần thu thập dữ liệu
    name = input("Nhập tên người: ")
    person_dir = os.path.join(data_dir, name)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)

    # Khởi động webcam
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    count = 0
    print("Nhìn vào camera và chờ...")

    while count < 100:  # Thu thập 100 ảnh
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển sang ảnh xám để phát hiện khuôn mặt
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Cắt khuôn mặt
            face_img = frame[y:y+h, x:x+w]
            # Lưu ảnh
            file_name = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(file_name, face_img)
            count += 1
            
            # Vẽ khung quanh khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Collected: {count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Collecting Faces", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Đã thu thập xong {count} ảnh cho {name}")

if __name__ == "__main__":
    collect_face_data()