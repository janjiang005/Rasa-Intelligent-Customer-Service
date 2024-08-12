import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="/data")
db = SQLAlchemy()  # 数据库ORM
# 初始化线程池，用以对各个算法处理时管理后台任务
executor_main = ThreadPoolExecutor(os.cpu_count())
