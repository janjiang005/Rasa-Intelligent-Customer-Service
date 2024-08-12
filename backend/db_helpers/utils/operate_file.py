# 文件操作类
import os
import shutil
import zipfile

from db_helpers.config import db_config,config
from db_helpers.exts import *

app.config.from_object(db_config.FILE_DB)  # 加载配置文件
# db.init_app(app)  # 数据库ORM绑定app


# 删除文件，删除任务时调用
def delete_files(path):
    '''
    删除该目录下的所有文件,但保留该目录
    :param path: 输入要删除的目录路径，格式为xx/xx/
    :return:
    '''
    del_list = os.listdir(path)
    try:
        for f in del_list:
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree()
    except Exception:
        return -1
    return 0


def delete_dir(path):
    '''删除该目录及其下所有文件夹,不保留该目录传入格式为目录xx/xx'''
    try:
        shutil.rmtree(path)
    except Exception:
        return -1
    return 0


def mkdir(folder_name):
    """
    创建文件夹
    :param folder_name:文件夹的名称
    :return:创建成功则返回1，否则返回0
    """
    folder_name = folder_name.strip()
    folder_name = folder_name.rstrip("/")
    isExists = os.path.exists(folder_name)
    # 判断结果
    if not isExists:
        os.makedirs(folder_name)
        return 1
    else:
        return 0


def move_data(data_path, des_path):
    """
    将数据复制到新建的文件夹下
    :param data_path:数据初始所在的位置
    :param des_path:数据要复制到哪个文件夹下面
    :return:若复制成功，返回1，否则返回0
    """
    try:
        path, data_name = os.path.split(data_path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == data_name:
                    old_file_path = os.path.join(root, file)
                    # print(old_file_path)
                    new_path = des_path
                    if not os.path.exists(new_path):  # 创建新文件夹
                        os.makedirs(new_path)
                    new_file_path = new_path + '/' + file
                    shutil.copyfile(old_file_path, new_file_path)  # 复制文件
        return 1
    except:
        return 0


def turn_result_in_txt(table, result_data, path, id):
    """
    将从数据库中取出的处理结果存到txt文件里，txt文件命名为任务id.txt，放在图像数据所在的文件夹下
    :param result_data:算法处理数据，dict格式
    :param id:任务的id，用来创建txt文件
    :return:若成功，返回1，否则返回0
    """
    with app.app_context():
        try:
            if table.__tablename__ == "id_card":
                with open(path + '/task' + str(id) + '.txt', 'a') as f:
                    f.write('任务:' + str(result_data['id']) + '\n')
                    if result_data['name'] == "null":
                        f.write('姓名:识别失败' + '\n')
                    else:
                        f.write('姓名:' + str(result_data['name']) + '\n')
                    if result_data['sex'] == 1:
                        f.write('性别:男' + '\n')
                    elif result_data['sex'] == 0:
                        f.write('性别:女' + '\n')
                    else:
                        f.write('识别失败' + '\n')
                    if result_data['year'] == -1:
                        f.write('出生年：识别失败' + '\n')
                    else:
                        f.write('出生年:' + str(result_data['year']) + '\n')
                    if result_data['month'] == -1:
                        f.write('出生月：识别失败' + '\n')
                    else:
                        f.write('出生月:' + str(result_data['month']) + '\n')
                    if result_data['day'] == -1:
                        f.write('出生日：识别失败' + '\n')
                    else:
                        f.write('出生日:' + str(result_data['day']) + '\n')
                    if result_data['nation'] == "null":
                        f.write('民族:识别失败' + '\n')
                    else:
                        f.write('民族:' + str(result_data['nation']) + '\n')
                    if result_data['address'] == "null":
                        f.write('地址:识别失败' + '\n')
                    else:
                        f.write('地址:' + str(result_data['address']) + '\n')
                    if result_data['id_number'] == "null":
                        f.write('身份证号:识别失败' + '\n')
                    else:
                        f.write('身份证号:' + str(result_data['id_number']) + '\n')
                    f.write('---------------------------------------------------------\n')
                    f.write('---------------------------------------------------------\n')
                return 1
            elif table.__tablename__ == "object_recognition":
                print(path + '/task' + str(id) + '.txt')
                with open(path + '/task' + str(id) + '.txt', 'a') as f:
                    f.write('任务:' + str(result_data['id']) + "\n")
                    if (len(result_data['image_info']) == 0):
                        f.write('识别结果:' + "未识别到目标" + "\n")
                    else:
                        f.write('识别结果:' + str(result_data['image_info']) + "\n")
                    f.write('---------------------------------------------------------\n')
                    f.write('---------------------------------------------------------\n')
                return 1
            elif table.__tablename__ == "object_detection":
                with open(path + '/task' + str(id) + '.txt', 'a') as f:
                    f.write('任务:' + str(result_data['id']) + '\n')
                    f.write('识别结果:' + str(result_data['image_info']) + '\n')
                    f.write('---------------------------------------------------------\n')
                    f.write('---------------------------------------------------------\n')
                return 1
            elif table.__tablename__ == "receipt_recognition":
                with open(path + '/task' + str(id) + '.txt', 'a') as f:
                    f.write('发票代码:' + str(result_data['r_code']) + '\n')
                    f.write('发票号码:' + str(result_data['r_number']) + '\n')
                    f.write('开票日期:' + str(result_data['r_data']) + '\n')
                    f.write('机器编号:' + str(result_data['machine_number']) + '\n')
                    f.write('税控码:' + str(result_data['fiscal_code']) + '\n')
                    f.write('购买方名称及身份证号码:' + str(result_data['buyer']) + '\n')
                    f.write('组织机构代码:' + str(result_data['organ_code']) + '\n')
                    f.write('纳税人识别号:' + str(result_data['person_code']) + '\n')
                    f.write('车辆类型:' + str(result_data['car_class']) + '\n')
                    f.write('厂牌型号:' + str(result_data['factory']) + '\n')
                    f.write('产地:' + str(result_data['place']) + '\n')
                    f.write('合格证号:' + str(result_data['certificate']) + '\n')
                    f.write('进口证明书号:' + str(result_data['import_number']) + '\n')
                    f.write('商检单号:' + str(result_data['sell_check_number']) + '\n')
                    f.write('发动机号码:' + str(result_data['engine_number']) + '\n')
                    f.write('车辆识别号代号:' + str(result_data['car_number']) + '\n')
                    f.write('价税合计:' + str(result_data['tax_all']) + '\n')
                    f.write('小写:' + str(result_data['tax_all_small']) + '\n')
                    f.write('销货单位名称:' + str(result_data['seller']) + '\n')
                    f.write('电话:' + str(result_data['phone_number']) + '\n')
                    f.write('纳税人识别号:' + str(result_data['person_id']) + '\n')
                    f.write('账号:' + str(result_data['account']) + '\n')
                    f.write('地址:' + str(result_data['address']) + '\n')
                    f.write('开户银行:' + str(result_data['bank']) + '\n')
                    f.write('增值税税率:' + str(result_data['rate']) + '\n')
                    f.write('增值税税额:' + str(result_data['amount']) + '\n')
                    f.write('主管税务机关及代码:' + str(result_data['agency']) + '\n')
                    f.write('不含税价:' + str(result_data['without_tax']) + '\n')
                    f.write('完税凭证号码:' + str(result_data['tax_check_number']) + '\n')
                    f.write('吨位:' + str(result_data['weight']) + '\n')
                    f.write('限乘人数:' + str(result_data['limit']) + '\n')
                    f.write('开票人:' + str(result_data['check_people']) + '\n')
                    f.write('---------------------------------------------------------\n')
                    f.write('---------------------------------------------------------\n')
                return 1
            elif table.__tablename__ == "vid_object_recognition":
                pass
        except:
            return 0


def zip_dir(dirpath, zip_name):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 压缩成功返回1，否则返回0
    """
    try:
        zip = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')
            for filename in filenames:
                if filename.endswith('zip'):
                    pass
                else:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
        return 1
    except:
        return 0


def zip_data(table, id):
    """
    将数据和算法处理结果取出来，放进同一个文件夹中并压缩成zip文件
    :param table:哪一个子任务表
    :param id:子任务表中，任务的id
    :return:返回一个包括原始数据和算法处理结果的zip文件。
    """
    with app.app_context():
        data = [tips.__dict__ for tips in table.query.filter(table.task_id == id).all()]
        path = config.UPLOAD_FOLDER + '/task' + str(id)
        print(path)
        zippath = config.UPLOAD_FOLDER + '/task' + str(id) + '/task' + str(id)
        for i in data:
            move_data(i['input_path'], path)
            turn_result_in_txt(table, i, path, id)
        zip_dir(path, zippath + '.zip')
        return zippath + '.zip'
