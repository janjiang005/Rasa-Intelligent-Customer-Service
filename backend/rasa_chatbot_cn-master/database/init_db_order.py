import sqlite3
import os

def init_db():
    db_path = 'order.db'  # 使用完整路径
    db_dir = 'database/' + db_path
    os.makedirs(os.path.dirname(db_dir), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 修改表名为 orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT NOT NULL,
            order_type TEXT NOT NULL,
            item_status TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            sender_address TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_address TEXT NOT NULL
        )
    ''')

    # Records to be inserted
    records = [
        ('SF12345', '书籍', '东莞市-成都市运输中', '张三', '广东省东莞市','李四','四川省成都市'),
        ('SF78900', '文件', '派送中', '王五', '北京市','六六','江苏省南京市'),
        ('SF34512', '文件', '等待揽收中', '李红', '上海市','王伟','四川宜宾市'),
        ('SF77776', '食品', '已签收', '赵明', '上海市','张云','青海省西宁市'),
        ('SF89754', '日用品', '成都市-北京市运输中', '谢佳', '四川省成都市','江流','北京市')
    ]

    for record in records:
        cursor.execute('''
            INSERT INTO orders (order_id, order_type, item_status, sender_name, sender_address, receiver_name, receiver_address) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', record)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
