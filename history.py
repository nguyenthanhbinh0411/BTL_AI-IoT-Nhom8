import mysql.connector
import json  # Import json module
import sys
from datetime import datetime

# Kết nối đến MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Thay bằng username MySQL của bạn
    password="Thanhbinh12",  # Thay bằng mật khẩu MySQL của bạn
    database="pushups_db"
)
cursor = db.cursor()

def get_history(confirmed_user):
    """Hiển thị lịch sử người tập đã xác nhận với tên, mã sinh viên, lớp và kết quả"""
    if confirmed_user == "Unknown":
        return json.dumps([])

    cursor.execute("""
        SELECT students.name, students.msv, students.class, pushup_logs.pushup_count, pushup_logs.timestamp,
            pushup_logs.result
        FROM pushup_logs
        JOIN students ON pushup_logs.user_id = students.id
        WHERE students.name = %s
    """, (confirmed_user,))
    
    logs = cursor.fetchall()
    
    history_data = []
    for log in logs:
        history_data.append({
            "user_name": log[0],      
            "msv": log[1],            
            "class": log[2],          
            "pushup_count": log[3],    
            "time": log[4].strftime("%Y-%m-%d %H:%M:%S"),  # Convert datetime to string
            "result": log[5]           
        })
    return json.dumps(history_data)

if __name__ == "__main__":
    confirmed_user = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    history = get_history(confirmed_user)
    print(history)
