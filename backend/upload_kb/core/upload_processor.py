import os
import json
import sqlite3
from typing import Optional, Any, List
import numpy as np

import torch
from PyPDF2 import PdfFileReader
import docx2txt
from sentence_transformers import SentenceTransformer
from core.chinese_recursive_text_splitter import ChineseRecursiveTextSplitter
import faiss

# 初始化模型
from transformers import BertModel, BertTokenizer

model = SentenceTransformer('/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/bge-large-zh-v1.5')


# 连接数据库
def get_db_connection():
    conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/logistics_qa.db')
    return conn


# 处理上传的文件
def process_uploaded_file(file):
    try:
        content = None
        if file.filename.endswith('.json'):
            content = json.load(file)
        elif file.filename.endswith('.pdf'):
            pdf_reader = PdfFileReader(file)
            content = ''.join([pdf_reader.getPage(i).extract_text() for i in range(pdf_reader.numPages)])
        elif file.filename.endswith('.docx'):
            content = docx2txt.process(file)
        else:
            return False

        chunks = split_text(content)
        save_chunks_to_db(chunks)
        save_embeddings_to_faiss(chunks)
        return True
    except Exception as e:
        print(f"Error processing file: {e}")
        return False


# 使用自定义分词器分词
def split_text(content):
    text_splitter = ChineseRecursiveTextSplitter(
        keep_separator=True,
        is_separator_regex=True,
        chunk_size=250,
        chunk_overlap=0
    )
    chunks = text_splitter.split_text(content)
    return chunks


def get_db_connection():
    conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/logistics_qa.db')
    return conn


bert_model = BertModel.from_pretrained(
    '/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/bert-base-chinese')
bert_tokenizer = BertTokenizer.from_pretrained(
    '/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/bert-base-chinese')


def get_embedding(text: str) -> np.ndarray:
    inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].numpy()
    return cls_embedding


# 保存分词后的文本向量到数据库
def save_chunks_to_db(file, chunks):
    conn = get_db_connection()
    cursor = conn.cursor()

    accumulated_text = ""
    index = 1
    for chunk in chunks:
        chunk = chunk.strip()
       # print(chunk)
        if chunk != '\\' and chunk != "":
            accumulated_text += chunk

       #     print(accumulated_text)
        else:
            if accumulated_text:  # 检查累积的文本是否为空
                accumulated_text.strip()
                print("index:",index)
                print("result:",accumulated_text)
                embedding = get_embedding(accumulated_text).flatten()
                embedding_bytes = embedding.tobytes()  # 将嵌入向量转换为字节
                cursor.execute("INSERT INTO logistics_qa (filename, result,embed) VALUES (?,?, ?)",
                               (file.filename, accumulated_text,embedding_bytes))
                accumulated_text = ""  # 重置累积文本
                index += 1

    conn.commit()
    conn.close()


# 保存嵌入向量到FAISS
def save_embeddings_to_faiss(chunks):
    index_file = "/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/faiss_index.bin"
    embeddings = model.encode(chunks)

    # 创建或加载 FAISS 索引
    index_dir = os.path.dirname(index_file)
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        print(f"Created directory for Faiss index at {index_dir}")

    if not os.path.exists(index_file):
        # 创建一个新的 Faiss 索引，假设向量维度为模型的输出维度
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        print(f"Created new Faiss index at {index_file}")
    else:
        # 如果文件已存在，则加载现有的索引
        index = faiss.read_index(index_file)
        print(f"Loaded existing Faiss index from {index_file}")

    # 将新向量 embeddings 添加到索引中
    index.add(embeddings)

    # 将更新后的索引保存回文件
    faiss.write_index(index, index_file)
    print(f"Saved embeddings to Faiss index in {index_file}")
