# pojo类，用来映射数据库表结构的类
from db_helpers.exts import db

class Task_Center(db.Model):
    __tablename__ = "task_center"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_name = db.Column(db.String(100))
    task_tag = db.Column(db.Boolean)  # 1表示处理中 0表示已完成
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


    # 单个对象方法
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象方法
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result
