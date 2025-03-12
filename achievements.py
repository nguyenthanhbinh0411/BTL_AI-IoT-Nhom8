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

def get_achievements():
    """Hiển thị thành tích cao nhất của từng người tập"""
    cursor.execute("""
        SELECT students.name, students.msv, students.class, MAX(pushup_logs.pushup_count) AS max_pushup_count, pushup_logs.result
        FROM pushup_logs
        JOIN students ON pushup_logs.user_id = students.id
        GROUP BY students.id, students.name, students.msv, students.class, pushup_logs.result
        ORDER BY max_pushup_count DESC
    """)
    achievements = cursor.fetchall()
    
    achievements_data = []
    seen_users = set()
    for achievement in achievements:
        if achievement[0] not in seen_users:
            achievements_data.append({
                "name": achievement[0],
                "msv": achievement[1],
                "class": achievement[2],
                "max_pushup_count": achievement[3],
                "result": achievement[4]
            })
            seen_users.add(achievement[0])
    
    return json.dumps(achievements_data)

if __name__ == "__main__":
    achievements = get_achievements()
    print(achievements)
