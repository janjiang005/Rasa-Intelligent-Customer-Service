import sqlite3
import os


def init_db():
    db_path = './user.db'
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            order_id TEXT NOT NULL,
            order_type TEXT NOT NULL,
            province TEXT,
            city TEXT NOT NULL,
            emotion TEXT,
            confidence REAL,
            question TEXT ,
            times INTEGER 
        )
    ''')

    # Records to be inserted
    records = [
        ('收件','SF12345', '书籍', '四川省', '成都市', '平和','0.883','我的快递到哪了？',2),
        ('寄件','SF78900', '文件', '江苏省', '南京市', '消极','0.676','丢件了怎么办？',1),
        ('收件','SF34512', '文件', '四川省', '宜宾市', '消极','0.774','怎么还不配送过来？',1),
        ('收件','SF77776', '食品', '青海省', '西宁市', '积极','0.641','我要拒收快递',1),
        ('寄件','SF89754', '日用品', '', '北京市', '积极','0.669','我想更换地址',1),
        ('收件','SF55555','文件','四川省','南充市','消极','0.790','为什么你们一直不联系我？',1),
        ('寄件','SF66666', '食品', '四川省', '简阳市', '积极','0.589','快递损坏怎么办', 1)
    ]

    for record in records:
        cursor.execute('''
            INSERT INTO user (user_type,order_id, order_type, province, city,emotion,confidence, question,times) 
            VALUES (?,?, ?, ?, ?, ?,?,?,?)
        ''', record)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
