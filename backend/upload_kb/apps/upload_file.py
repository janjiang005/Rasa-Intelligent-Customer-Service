import re
from typing import List, Optional, Any
import logging
import os
import json
import sqlite3
from flask import Flask, render_template, request, jsonify, Response,Blueprint
import PyPDF2
import docx2txt
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 自定义分词器
from core.upload_processor import split_text, save_chunks_to_db

import faiss

from core.upload_processor import save_embeddings_to_faiss

upload = Blueprint('upload',__name__)

result = []
id = 1
@upload.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    global result, id
    id = 0
    if request.method == 'POST':

        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            if file:
                file_content = None
                if file.filename.endswith('.json'):
                    file_content = json.dumps(json.load(file), ensure_ascii=False)
                elif file.filename.endswith('.pdf'):
                    pdf_reader = PyPDF2.PdfFileReader(file)
                    file_content = ''
                    for page_num in range(pdf_reader.numPages):
                        page = pdf_reader.getPage(page_num)
                        file_content += page.extract_text()
                elif file.filename.endswith('.docx'):
                    file_content = docx2txt.process(file)
                else:
                    return jsonify({"error": "Unsupported file format"}), 400


                chunks = split_text(file_content)

                db_chunks = json.dumps(chunks,ensure_ascii=False)
                save_chunks_to_db(file,db_chunks)
                save_embeddings_to_faiss(chunks)

                # 获取更新后的向量库数据并返回给前端
                result.append({
                    'task_id': id,
                    'filename':file.filename,
                    'chunk':chunks
                    }
                )
                id += 1
        return Response(json.dumps(result),mimetype='application/json')
    elif request.method == 'GET':
        return jsonify(result)