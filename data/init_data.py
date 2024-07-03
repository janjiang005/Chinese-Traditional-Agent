import sqlite3
import os


def init_db():
    db_path = 'user.db'
    #os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #times:出现次数
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient(
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT NOT NULL,
            question TEXT NOT NULL,
            times INTEGER NOT NULL
        )
    ''')

    # Records to be inserted
    records = [
        ('儿科','儿童食欲不振怎么办？',2),
        ('儿科','儿童经常感冒怎么办？',5),
        ('儿科','儿童腹泻怎么办?',7),
        ('神经科','我最近记忆力下降是怎么回事?',1),
        ('神经科','我的头痛可能是由什么引起的?',4),
        ('眼科','我的视力是否需要矫正？',8),
        ('眼科','我的白内障需要手术治疗吗？',3),
        ('耳鼻喉科','我的打鼾如何治疗？',7),
        ('耳鼻喉科','我喉咙痛怎么回事？',9),
        ('皮肤科','我的皮肤过敏可能是什么引起的?',10),
        ('皮肤科','我的湿疹如何治疗?',2),
    ]

    for record in records:
        cursor.execute('''
            INSERT INTO patient (department,question,times) 
            VALUES ( ?, ?, ?)
        ''', record)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
