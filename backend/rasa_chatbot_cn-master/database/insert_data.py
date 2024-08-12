import sqlite3

conn = sqlite3.connect('logistics.db')

# 插入物流订单数据
conn.execute('''
INSERT INTO logistics_orders (order_id, receiver_name, sender_name, address, item_type)
VALUES
    ('12345', '张三', '李四', '四川省,成都市,武侯区', '电子产品','派送中'),
    ('12346', '王五', '赵六', '广东省,广州市,天河区', '衣物','揽收中'),
    ('12347', '孙七', '周八', '江苏省,南京市,玄武区', '书籍','暂无物流状态')
''')

# 插入一些测试收件请求数据
conn.execute('''
INSERT INTO receive_requests (username, province, city, district, question)
VALUES
    ('用户1', '四川省', '成都市', '成华区', '我的快递到哪了？'),
    ('用户2', '广东省', '广州市', '天河区', '我的快递还有多久才到？')
''')

# 插入一些测试寄件请求数据
conn.execute('''
INSERT INTO send_requests (username, province, city, district, question)
VALUES
    ('用户3', '江苏省', '南京市', '宣武区', '丢件了怎么办？'),
    ('用户4', '四川省', '成都市', '武侯区', '什么时候上门取件？')
''')

# 提交更改并关闭连接
conn.commit()
conn.close()
