import datetime

from db_helpers.config import config,db_config
from db_helpers.exts import *
from db_helpers.models.db_model import Task_Center

app.config.from_object(config)  # 加载配置文件
app.config.from_object(db_config.FILE_DB)  # 加载配置文件
# db.init_app(app)  # 数据库ORM绑定app


def create_task(task_name, task_tag):
    '''
    生成任务,每个功能页面的算法执行之前都调用本方法
    :param task_name:
    :param task_tag:
    :param start_time:
    :param end_time:
    :return:
    '''
    with app.app_context():
        try:
            new_task = Task_Center(task_name=task_name, task_tag=task_tag, start_time
            =datetime.datetime.now())
            db.session.add(new_task)
            db.session.flush()
            id = new_task.id
            db.session.commit()
        except Exception:
            return -1
        return id


def delete_task_center(id):
    '''
    用于算法执行失败后删除刚创建的主表id
    :param id: 要删除的主表id
    :return:
    '''
    with app.app_context():
        try:
            # task = Task_Center.query.filter(Task_Center.id == id).frist()
            db.session.query(Task_Center).filter(Task_Center.id == id).delete()
            # print('这里的task', task)
            # db.session.delete(task)
            db.session.commit()
        except Exception:
            return -1
        return 0


def update_task_center(table, id, task_tag_value, result_path):
    '''
    用于任务执行完成后，更新Task_Center表中状态与完成时间的值,以及保存文件结果的路径
    :param table: 要修改的表对象
    :param id: 要修改的数据的id
    :param task_tag_value: 当任务完成，更新tag为0
    :return: 判断是否更新成功
    '''
    with app.app_context():
        try:
            Task_Center.query.filter(table.id == id).update({"task_tag": task_tag_value})
            Task_Center.query.filter(table.id == id).update({"end_time": datetime.datetime.now()})
            Task_Center.query.filter(table.id == id).update({"save_path": result_path})
            db.session.commit()
        except Exception:
            return -1
        return 0


if __name__ == '__main__':
    # 测试用例

    dict = {"task_id": 3,
            "image_info": {'person-01': ['228×425', 0.932], 'person-02': ['234×416', 0.926],
                           'person-03': ['264×430', 0.896],
                           'car-04': ['129×90', 0.894], 'person-05': ['231×476', 0.857], 'car-06': ['118×80', 0.845],
                           'person-07': ['40×98', 0.825], 'person-08': ['37×111', 0.814],
                           'handbag-09': ['68×136', 0.767],
                           'handbag-10': ['122×109', 0.669], 'car-11': ['27×19', 0.665], 'car-12': ['72×71', 0.664],
                           'car-13': ['77×65', 0.654], 'car-14': ['37×36', 0.641], 'car-15': ['34×47', 0.616],
                           'handbag-16': ['73×122', 0.508], 'car-17': ['25×17', 0.417], 'car-18': ['26×17', 0.404]},
            "input_path": '/data/lgd/idcard_recognize/24/test.txt',
            "output_path": '/data/lgd/idcard_recognize/24/test.txt'}
    import json

    dict['image_info'] = json.dumps(dict['image_info'])
    # print(dict['image_info'])
    # print(insert_idcard_result(dict))
    # update_task_center(Task_Center, 4, 0)
