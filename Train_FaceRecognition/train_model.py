import face_recognition
import os
import pickle

def train_model():
    data_dir = "face_data"
    known_face_encodings = []
    known_face_names = []

    # Duyệt qua từng thư mục con (tên người)
    for person_name in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        # Duyệt qua từng ảnh của người đó
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            
            # Tạo encoding cho khuôn mặt
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(person_name)
                
    # Lưu mô hình đã huấn luyện
    data = {"encodings": known_face_encodings, "names": known_face_names}
    with open("face_model.pkl", "wb") as f:
        pickle.dump(data, f)
    
    print("Huấn luyện mô hình hoàn tất!")

if __name__ == "__main__":
    train_model()