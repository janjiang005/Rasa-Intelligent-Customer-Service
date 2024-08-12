import re
from typing import List, Optional, Any
import logging
import os
import json
import sqlite3

from flask_migrate import Migrate
import PyPDF2
import docx2txt

from apps.upload_file import upload
import sys
import os

# 获取当前文件所在目录的父目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 将父目录添加到 sys.path 中
sys.path.append(parent_dir)


from db_helpers.config import config,db_config
from db_helpers.exts import db,app

app.register_blueprint(upload)

app.config.from_object(db_config.FILE_DB)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app,db)

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST,GET'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Type, X-Requested-With,file_name'
    return response


logger = logging.getLogger(__name__)







if __name__ == '__main__':
    app.run(host='localhost',port=6040,debug=True,threaded=True)
