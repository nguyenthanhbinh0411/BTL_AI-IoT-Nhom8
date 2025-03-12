import mysql.connector
import json

# Kết nối đến MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Thay bằng username MySQL của bạn
    password="Thanhbinh12",  # Thay bằng mật khẩu MySQL của bạn
    database="pushups_db"
)
cursor = db.cursor()

def get_students():
    """Hiển thị danh sách học sinh"""
    cursor.execute("SELECT id, name, msv, class FROM students")
    students = cursor.fetchall()
    
    students_data = []
    for student in students:
        students_data.append({
            "id": student[0],
            "name": student[1],
            "msv": student[2],
            "class": student[3]
        })
    
    return json.dumps(students_data)

if __name__ == "__main__":
    students = get_students()
    print(students)
