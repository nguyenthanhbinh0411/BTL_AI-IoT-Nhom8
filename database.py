import mysql.connector

# Kết nối đến MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Thay bằng username MySQL của bạn
    password="Thanhbinh12",  # Thay bằng mật khẩu MySQL của bạn
    database="pushups_db"
)
cursor = db.cursor()

def get_user_id(name, msv="default_msv", class_name="default_class"):
    """Lấy ID của người tập từ database. Nếu chưa có thì thêm mới."""
    cursor.execute("SELECT id FROM students WHERE name = %s", (name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Thêm user mới nếu chưa tồn tại
    cursor.execute("INSERT INTO students (name, msv, class) VALUES (%s, %s, %s)", (name, msv, class_name))
    db.commit()
    return cursor.lastrowid

def log_pushups(name, count, result):
    """Lưu số lần chống đẩy vào database với trạng thái Pass/Fail"""
    user_id = get_user_id(name)
    
    cursor.execute("INSERT INTO pushup_logs (user_id, pushup_count, result) VALUES (%s, %s, %s)", 
                   (user_id, count, result))
    db.commit()
