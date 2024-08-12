import logging as rel_log
import os
from datetime import timedelta
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import *
from flask_migrate import Migrate

# 导入apps中的各功能文件
from db_helpers.models.db_model import *
from db_helpers.config import config,db_config
from db_helpers.exts import db, app
from db_helpers.utils import operate_file,operate_database

app.config.from_object(db_config.FILE_DB)  # 加载配置文件
app.config.from_object(config)
db.init_app(app)  # 数据库ORM绑定app
migrate = Migrate(app, db)

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

app_for_ext = app


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Type, X-Requested-With,file_name'
    return response


def to_json(all_vendors):
    '''将表列表对象转换成json格式，配合类中的double_to_dict()使用,针对于多对象'''
    v = [ven.dobule_to_dict() for ven in all_vendors]
    v = jsonify(v)
    return v


def response_img(path):
    '''传入本地存储路径，将图片包装成响应文件并返回到网页,能够在网页直接展示图片'''
    img_path = path
    if not os.path.exists(img_path):
        return jsonify("文件出现未知错误，已损毁")
    with open(img_path, "rb") as f:
        image = f.read()
    return Response(image, mimetype='wav')


# def str_to_class(str):
#     '''
#     :param str: 传入的表名，string类型
#     :return: 返回相应的对象
#     '''
#     if str == "Object_Recognition":
#         return Object_Recognition
#     elif str == "Object_Detection":
#         return Object_Detection
#     elif str == "Receipt_Recognition":
#         return Receipt_Recognition
#     elif str == "Voice_Rec":
#         return Voice_Rec


def table_to_dir(table_name, t_id):
    '''

    :param table_name: 表名，字符串
    :param t_id: 主任务的id
    :return: 要删除的路径
    '''
    if table_name == "Object_Recognition":
        return app.config['OBJECT_REC_UPLOAD_FOLDER'] + "/task" + str(t_id)
    elif table_name == "Object_Detection":
        return app.config['OBJECT_DET_UPLOAD_FOLDER'] + "/task" + str(t_id)
    elif table_name == "Receipt_Recognition":
        return app.config['RECEIPT_REC_UPLOAD_FOLDER'] + "/task" + str(t_id)
    elif table_name == "Voice_Rec":
        return app.config['VOICE_REC_UPLOAD_FOLDER'] + "/task" + str(t_id)


# def imgs_to_base64(id):
#     '''查询某任务下的所有处理图片，并将其转化为base64字节流形式'''
#     print("diaoyonghanshu")
#     datas = Id_Card.query.filter(Id_Card.task_id == id).all()
#     imgs_base64 = []
#     for data in datas:
#         print(data.input_path)
#         with open(data.input_path) as f:
#             print("文件打开成功")
#             img_base64 = base64.b64encode(f.read())
#             imgs_base64.append(img_base64)
#     #此方法不行，再考虑
#     return jsonify(imgs_base64)

@app.route('/')
def hello_world():
    return 'Hello LGD'


# 所有的视图函数先写到app.py中，后期分别注册成蓝图,所有函数目前均不返回模板

# 页面1：功能台 Functional units
# 主要由前端直接展示图片和按钮，根据按钮跳转
@app.route("/func_units")
def func_units():
    """要由前端直接展示图片和按钮，根据按钮跳转到页面2"""
    pass


def save_tasks():
    '''保存未完成任务，目前暂定前端关闭程序后后端后台继续执行任务'''
    pass


def load_tasks():
    '''加载上次未完成任务'''
    pass


# 此部分最新代码已经迁移到apps.idcard_rec.py
# 页面2：功能页面--身份证识别
# 提交图片后，跳转至子任务界面
# 前端限制输入格式，传到后端，调用算法后将算法结果传到数据库，可在任务中心里通过数据库将结果返回前端
# @app.route('/idcard_recognize', methods=['GET', 'POST'])
# def upload_sfz():
#     if request.method == 'POST':
#         # 使用input的name来接收文件
#         # file = request.files['file']
#         files = request.files.getlist('file')
#
#         list = []
#
#         # 创建任务，传入task_name，task_tag为1代表任务进行中
#         # TODO：路径统一管理
#         # 服务器环境地址，在自己的电脑运行需替换成本机文件地址
#         id = create_task('Id_Card', 1)
#         # dir = os.path.join(app.config['IDCARD_UPLOAD_FOLDER'] + '/%s/' % (id))
#         dir = os.path.join('/Users/zhangkai/Documents/PycharmProjects/ocr' + '/%s/' % (id))
#         os.makedirs(dir)
#
#         for file in files:
#             if file and allowed_file(file.filename):
#                 # 使用时间戳保存文件名
#                 pic_name = imageName(file.filename)
#
#                 file_path = os.path.join(dir, pic_name)
#                 file.save(file_path)
#                 # 服务器环境，调用算法
#                 # dict = core.inference_idcard.start_idcard_inference(file_path, id)
#                 # 非服务器环境，调用模拟算法
#                 dict = core.test_inference_idcard.test_start_idcard_inference(file_path, id)
#                 # 将算法识别结果插入数据库
#                 insert_idcard_result(dict)
#                 list.append(dict)
#
#         # 算法识别结束，更新状态task_tag和end_time，tag为0代表任务结束
#         update_task_center(Task_Center, id, 0)
#         return jsonify(list)


# 页面3：任务中心 Task Center
# 功能：1.点击查看，调转到任务详情界面
#     2.若任务完成，点击下载处理结果，前端判断task_center.task_tag==1时，则按钮可点击，具体下载功能暂未实现
#     3.删除任务，删除任务及相关结果
#
# 点击任务中心，直接返回所有task_center查询结果
@app.route("/TaskCenter")
def show_all_tasks():
    '''
    功能：task_center所有查询结果
    参数：无
    返回值：task_center表所有存储结果，包含id,task_name,task_tag,start_time，end_time
    '''
    print("you have get there")
    tasks_all = Task_Center.query.all()
    return to_json(tasks_all)


@app.route("/download_result/<int:t_id>")
def download_result(t_id):
    '''
    功能：查看子任务
    参数：t_id:任务id，由查看按钮绑定
    返回值：
    '''
    task = Task_Center.query.filter(Task_Center.id == t_id).first()
    subtask_name = str_to_class(task.task_name)  # 按照子任务名称返回子表对象
    # 调用打包接口-------------
    zip_file = zip_data(subtask_name, t_id)
    file = open(zip_file, "rb").read()
    response = make_response(file)
    response.headers.add_header('file_name', zip_file)
    print(type(response.data))
    print(response.headers)
    # 根据地址直接返回给浏览器，as_attachment = True表示返回文件名
    # 进行函数替换
    return response


# @app.route("/download_result_batch",methods=["GET","POST"])
# def download_result():
#     '''批量处理'''
#     pass

@app.route("/delete_task/<int:t_id>")
def delete_task(t_id):
    '''
    功能：删除任务
    参数（int）：
    返回值（json列表）：成功返回"True"，失败返回"False"
     '''
    task = Task_Center.query.filter(Task_Center.id == t_id).first()
    sub_task = str_to_class(task.task_name)
    sub_task_list = sub_task.query.filter(sub_task.task_id == t_id).all()
    task_name = task.task_name
    task_dir = table_to_dir(task_name, t_id)
    delete_dir(task_dir)  # 删除该任务对应的文件夹
    for sub_task_class in sub_task_list:
        db.session.delete(sub_task_class)
    db.session.delete(task)
    db.session.commit()

    # 这里可能涉及到多线程下的删除，暂不做判断，默认删除成功
    return f"已删除任务{t_id}"


# 页面4：子任务详情页面
@app.route("/task_details/<int:t_id>", methods=["GET", "POST"])
def task_details(t_id):
    '''
    功能：查看子任务，点击查看即跳到本页面
    参数：t_id：任务id，由查看按钮绑定
    返回值：[dict1,dict2,dict3....]，其中dict1存储了任务id，状态，开始结束时间等信息，ditc2之后存储的是身份证信息
    '''
    # #测试代码
    # task_id = Task_Center.query.filter(Task_Center.id==t_id).first()#
    # print(type(task_id)) # <class 'db_model.Task_Center'>
    # print(task_id) # <Task_Center 1>
    # print(type(task_id.idcards)) # <class 'sqlalchemy.orm.collections.InstrumentedList'>
    # print(task_id.idcards) # [<Id_Card 1>, <Id_Card 2>]
    # print(task_id.idcards[0].name,task_id.idcards[1].name) # 张三 李四
    # json_idcards = to_json(task_id.idcards)
    # print(json_idcards)
    # print(type(json_idcards))
    # #data_obj = task_id
    # return json_idcards #测试是否返回了json格式

    temp = []
    task = Task_Center.query.filter(Task_Center.id == t_id).first()
    task_dict = task.single_to_dict()  # 查询出来的是单对象，化成字典
    sub_task = str_to_class(task.task_name)
    sub_task_list = sub_task.query.filter(sub_task.task_id == t_id).all()
    temp.append(task_dict)  # 把主表相关信息放在第0个位置
    for sub_task_detail in sub_task_list:  # 把该任务相关的所有数据信息放入
        temp.append(sub_task_detail.single_to_dict())
    return jsonify(temp)


@app.route("/task_prim_details/<int:t_id>", methods=["GET", "POST"])
def task_prim_details(t_id):
    '''通过id返回主表信息'''
    return Task_Center.query.filter(Task_Center.id == t_id).first().single_to_dict()


@app.route("/task_sub_details/<int:t_id>", methods=["GET", "POST"])
def task_sub_details(t_id):
    '''通过id返回子表信息'''
    task = Task_Center.query.filter(Task_Center.id == t_id).first()
    sub_task = str_to_class(task.task_name)
    sub_task_list = sub_task.query.filter(sub_task.task_id == t_id).all()
    return to_json(sub_task_list)


if __name__ == '__main__':
    app.run(host='localhost', port=6020, debug=True, threaded=True)
