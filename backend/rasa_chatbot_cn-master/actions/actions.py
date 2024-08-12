import logging
import os
import re
import sqlite3
import numpy as np
from typing import Text, Dict, List, Any, Optional

import torch
from difflib import SequenceMatcher
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification, AutoModel
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import faiss


def initial_model():
    global bert_model, bert_model2, bert_tokenizer
    model_path = "/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/bert-base-chinese"
    bert_model = AutoModelForSequenceClassification.from_pretrained(model_path)  # 情感分析专用
    bert_model2 = AutoModel.from_pretrained(model_path, is_decoder=True)
    bert_tokenizer = AutoTokenizer.from_pretrained(model_path)


initial_model()


class ChatGLM(BaseModel):
    model_name_or_path: str
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path, trust_remote_code=True)
        self.model.to("cuda")

    def generate_response(self, prompt: str) -> str:
        # inputs = self.tokenizer(prompt, return_tensors='pt', truncation=True, padding=True)
        # inputs = {key: value.to("cuda") for key, value in inputs.items()}  # 将输入移动到 GPU

        # with torch.no_grad():
        #      outputs = self.model.generate(**inputs, max_length=150)
        #     print(f"Generated tokens: {outputs}")

        # response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = self.model.chat(self.tokenizer, prompt, history=None, temperature=0.7, top_p=0.9)
        return response


llm = ChatGLM(model_name_or_path="/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/chatglm3_6b")


# def generate_response(context: str, user_info: str, emotion: str, user_question: str) -> str:
#     prompt = (
#         "你是一位资深的物流客服。根据已知信息、用户物流信息和用户当前情绪状态，"
#         "遵循以下原则及示例，你可以通过在已知信息中查找相关内容并仿造示例进行输出。\n"
#         "原则：\n"
#         "1、必须根据已知信息和用户物流信息作答！！！\n"
#         "2、一定要观察用户情绪变化，当用户比较消极时，用最简便的方式解答用户问题；当用户比较积极时，添加适量聊天语解答用户问题，比如：今天天气真好、很荣幸见到小主等等；当用户比较平和时，正常作答。\n"
#         "以下为问答示例：\n"
#         "我的快递怎么还没到？\n"
#         "小主，很抱歉让您久等了，我刚给快递公司打电话询问了，您的快递已经到了您所在的城市，只是物流信息还未及时更新，估计您今天就可以收到了。\n"
#         "请回答下列问题：\n\n"
#         f"<已知信息>{context}</已知信息>\n"
#         f"<用户物流信息>{user_info}</用户物流信息>\n"
#         f"<用户当前情绪状态>{emotion}</用户当前情绪状态>\n"
#         f"<问题>{user_question}</问题>\n"
#     ).format(context=context, user_info=user_info, emotion=emotion, user_question=user_question)
#
#     response = llm.generate_response(prompt)
#     return response


class ActionProvideOrderStatus(Action):
    def name(self) -> str:
        return "action_provide_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot('order_id')
        order_id = order_id.upper()

        if not order_id:
            dispatcher.utter_message(text="小主，您还没有提供订单号呢，请提供一下哦！")
            return []

        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db')
        cursor = conn.cursor()

        cursor.execute('SELECT item_status FROM orders WHERE order_id=?', (order_id,))
        order = cursor.fetchone()

        if order:
            item_status = order[0]
            response = f"小主我来啦~您咨询的订单 {order_id} 的状态是：{item_status}。"
            dispatcher.utter_message(text=response)
            dispatcher.utter_message(text="请告诉喵喵小主是收件人还是寄件人？")
        else:
            response = f"小主抱歉呢，未找到该订单号对应的订单。"
            dispatcher.utter_message(text=response)
            dispatcher.utter_message(text="麻烦小主重新输入正确的订单号哦！")
            order_id = None

        conn.close()

        return [SlotSet("order_id", order_id)]


class ActionProvideUserType(Action):
    def name(self) -> Text:
        return "action_provide_user_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_type = tracker.get_slot('user_type')
        return [SlotSet("user_type", user_type)]


def get_top_questions(province: str, user_type: str, top_k: int = 5):
    conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/questionlist/user.db')
    cursor = conn.cursor()
    print("province:", province)
    print("user_type", user_type)

    query = f'''
        SELECT question
        FROM user
        WHERE province = ? and user_type = ?
        ORDER BY times DESC 
        LIMIT ?
    '''
    cursor.execute(query, (province, user_type, top_k))
    questions = cursor.fetchall()
    print("questions:", questions)

    conn.close()
    return [q[0] for q in questions]


class ActionProvideTopQuestions(Action):
    def name(self) -> str:
        return "action_provide_top_questions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_type = tracker.get_slot('user_type')
        order_id = tracker.get_slot('order_id')

        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db')
        cursor = conn.cursor()
        if user_type == '收件':
            cursor.execute('SELECT receiver_address FROM orders WHERE order_id=?', (order_id,))
        else:
            cursor.execute('SELECT sender_address FROM orders WHERE order_id=?', (order_id,))
        row = cursor.fetchone()
        conn.close()

        addr = row[0]
        pattern = re.compile(r"^(?P<province>[\u4e00-\u9fa5]+省)(?P<city>[\u4e00-\u9fa5]+市)$")
        match = pattern.match(addr)
        province = match.group('province')
        top_questions = get_top_questions(province, user_type)

        dispatcher.utter_message(text="小主可以选择以下问题，喵喵将为您解答~：")
        for q in top_questions:
            button = {"title": q.replace(" ", "<br>"), "payload": f'/select_question{{"selected_question":"{q}"}}'}
            dispatcher.utter_message(buttons=[button])
        return []


class ActionHandleSelection(Action):
    def name(self) -> str:
        return "action_handle_selection"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        selected_question = None

        for event in tracker.events:
            if event.get("name") == "selected_question":
                print(event)
                selected_question = event.get("value")
                break

        return [SlotSet("selected_question", selected_question)]


def get_embedding(text: str) -> np.ndarray:
    # 对输入文本进行分词和编码
    inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=120)
    inputs = {key: value.to('cuda') for key, value in inputs.items()}  # 将输入移动到 GPU
    bert_model2.to("cuda")
    with torch.no_grad():
        outputs = bert_model2(**inputs)

    cls_embedding = outputs.last_hidden_state[:, 0, :]
    return cls_embedding


# 连接到问题数据库
db_path = '/home/caiqing/ssd1/jan/rasa/backend/questionlist/user.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def levenshtein_distance(a: str, b: str) -> int:
    """
    计算莱文斯坦距离
    """
    return SequenceMatcher(None, a, b).ratio()


class ActionUpdateSelectedQuestion(Action):
    def __init__(self, user_type: str = "收件"):
        super().__init__()
        self.user_type = user_type

    def name(self) -> str:
        return "action_update_selected"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot('order_id')
        user_type = tracker.get_slot('user_type')

        # 数据库连接
        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db')
        cursor = conn.cursor()

        # 获取订单信息
        if user_type == '收件':
            cursor.execute('SELECT order_type, receiver_address FROM orders WHERE order_id = ?', (order_id,))
        else:
            cursor.execute('SELECT order_type, sender_address FROM orders WHERE order_id = ?', (order_id,))
        row = cursor.fetchone()

        order_type, addr = row

        # 提取省份和城市
        pattern = re.compile(r"^(?P<province>[\u4e00-\u9fa5]+省)(?P<city>[\u4e00-\u9fa5]+市)$")
        match = pattern.match(addr)
        province = match.group('province')
        city = match.group('city')

        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/questionlist/user.db')
        cursor = conn.cursor()

        if tracker.get_slot('selected_question') is not None or tracker.get_slot('selected_question') != "":
            question = tracker.get_slot('selected_question')

            cursor.execute('SELECT times FROM user WHERE question=?', (question,))
            row = cursor.fetchone()
            times = row[0]
            cursor.execute(
                'UPDATE user SET times = ? WHERE question = ?',
                (times + 1, question)
            )
            conn.commit()

        conn.close()
        return []


class ActionUpdateSelectedQuestion(Action):
    def __init__(self, user_type: str = "收件"):
        super().__init__()
        self.user_type = user_type

    def name(self) -> str:
        return "action_update_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        order_id = tracker.get_slot('order_id')
        user_type = tracker.get_slot('user_type')

        # 数据库连接
        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db')
        cursor = conn.cursor()

        # 获取订单信息
        if user_type == '收件':
            cursor.execute('SELECT order_type, receiver_address FROM orders WHERE order_id = ?', (order_id,))
        else:
            cursor.execute('SELECT order_type, sender_address FROM orders WHERE order_id = ?', (order_id,))
        row = cursor.fetchone()

        order_type, addr = row

        # 提取省份和城市
        pattern = re.compile(r"^(?P<province>[\u4e00-\u9fa5]+省)(?P<city>[\u4e00-\u9fa5]+市)$")
        match = pattern.match(addr)
        province = match.group('province')
        city = match.group('city')

        # question = tracker.get_slot('user_question')
        question = tracker.get_slot('user_question')

        conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/questionlist/user.db')
        cursor = conn.cursor()

        # 获取现有问题
        cursor.execute('SELECT question, times FROM user')
        rows = cursor.fetchall()

        existing_questions = [row[0] for row in rows]
        existing_times = [row[1] for row in rows]

        similarities = [levenshtein_distance(question, existing_question) for existing_question in existing_questions]
        flag = 0
        for i in range(len(similarities)):
            if similarities[i] >= 0.90:
                cursor.execute(
                    'UPDATE user SET times = ? WHERE question = ?',
                    (existing_times[i] + 1, existing_questions[i])
                )
                flag = 1
                break
        if flag == 0:
            cursor.execute(
                'INSERT INTO user (user_type, order_id, order_type, province, city, question, times) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (self.user_type, order_id, order_type, province, city, question, 1)
            )

        conn.commit()

        conn.close()
        return []


# 加载FAISS索引
index = faiss.read_index("/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/faiss_index.bin")
conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/logistics_qa.db')
cursor = conn.cursor()


def get_db_connection():
    conn = sqlite3.connect('/home/caiqing/ssd1/jan/rasa/backend/upload_kb/database/logistics_qa.db')
    return conn


# def get_embedding(text: str) -> np.ndarray:
#     """
#     获取问题的嵌入向量
#     """
#     inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=120)
#
#     with torch.no_grad():
#         outputs = bert_model2(**inputs)
#
#     cls_embedding = outputs.last_hidden_state[:, 0, :]
#     return cls_embedding.numpy()
#
#
# def fetch_all_embeddings_from_db() -> List[np.ndarray]:
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT embed FROM logistics_qa')
#     embeddings = [np.frombuffer(row[0], dtype=np.float32) for row in cursor.fetchall()]
#     conn.close()
#     return embeddings

# def levenshtein_distance(a: str, b: str) -> int:
#     """
#     计算莱文斯坦距离
#     """
#     return SequenceMatcher(None, a, b).ratio()


def fetch_top_k_similar_questions(question: str, k: int = 5) -> List[str]:
    """
    找到 top k 个与给定问题最相似的结果
    """
    # 从数据库获取所有结果
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT result FROM logistics_qa')
    results = cursor.fetchall()

    # 计算莱文斯坦距离
    distances = [levenshtein_distance(question, result) for result in results]

    # 获取 top k 的索引
    top_k_indices = np.argsort(distances)[-k:]

    # 获取 top k 问题的结果
    top_k_results = [results[idx] for idx in top_k_indices]

    return top_k_results


class ActionAnalyzeEmotion(Action):
    def __init__(self):
        model_path = '/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/model/bert-base-chinese'

    def name(self) -> str:
        return "action_analyze_emotion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        # Get user message
        conn = sqlite3.connect("/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db")
        cursor = conn.cursor()
        user_type = tracker.get_slot("user_type")
        order_id = tracker.get_slot("order_id")
        if user_type == "收件":
            cursor.execute('SELECT order_type, receiver_address FROM orders WHERE order_id = ?', (order_id,))
        else:
            cursor.execute('SELECT order_type, sender_address FROM orders WHERE order_id = ?',
                           (order_id,))
        row = cursor.fetchone()
        order_type,addr = row
        db_path = '/home/caiqing/ssd1/jan/rasa/backend/questionlist/user.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("11111")
        user_question = tracker.latest_message.get('text')
        # user_message = tracker.latest_message.get('text')
        print("message:", user_question)
        inputs = bert_tokenizer(user_question, return_tensors='pt')
        outputs = bert_model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        predicted_class_id = logits.argmax().item()

        emotions = {0: '消极', 1: '平和', 2: '积极'}
        confidence = probabilities[0][predicted_class_id].item()
        emotion = emotions[predicted_class_id]
        print(emotion)
        print(confidence)
        pattern = re.compile(r"^(?P<province>[\u4e00-\u9fa5]+省)(?P<city>[\u4e00-\u9fa5]+市)$")
        match = pattern.match(addr)
        province = match.group('province')
        city = match.group('city')

        # Check existing emotion and confidence
        cursor.execute('SELECT emotion, confidence FROM user WHERE user_type = ? AND order_id = ? AND question = ?',
                       (user_type, order_id, user_question))
        row = cursor.fetchone()

        if row is None:
            # Insert new emotion if not present
            cursor.execute(
                'INSERT INTO user (user_type,order_id,order_type,province,city,emotion,confidence,question,times) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)',
                (user_type,order_id,order_type,province,city,emotion,confidence,user_question,1)
            )

        else:
            # existing_emotion, existing_confidence = row
            existing_emotion, existing_confidence = row

            # Compare confidence levels and update if the new confidence is higher
            if confidence > existing_confidence:
                cursor.execute(
                    'UPDATE user SET emotion = ?, confidence = ? WHERE user_type = ? AND order_id = ? AND question = ?',
                    (emotion, confidence, user_type, order_id,user_question)
                )

        conn.commit()
        conn.close()

        return [SlotSet("emotion", emotion)]


class ActionCustomerServiceResponse(Action):
    def name(self) -> str:
        return "action_handle_select_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('selected_question') is not None or tracker.get_slot('selected_question') != "":
            query = tracker.get_slot('selected_question')
        # elif tracker.get_slot("user_question") is not None or tracker.get_slot("user_question") != "":
        #     query = tracker.get_slot("user_question")
        context = fetch_top_k_similar_questions(query, k=5)
        # context = tracker.get_slot("context")
        print("context", context)
        order_id = tracker.get_slot("order_id")
        print("order_id", order_id)
        user_info = get_user_info(order_id, tracker)
        print("user_info", user_info)
        emotion = tracker.get_slot("emotion")
        print("emotion", emotion)
        user_question = tracker.get_slot("selected_question")
        #   print("selected_question:")
        # print(user_question)

        prompt = (
            "你是一位资深的物流客服。根据已知信息、用户物流信息和用户当前情绪状态，"
            "遵循以下原则及示例，你可以通过在已知信息中查找相关内容进行输出。\n"
            "原则：\n"
            "1、必须根据已知信息和用户物流信息作答！！！\n"
            "2、一定要观察用户情绪变化，当用户比较消极时，用最简便的方式解答用户问题；当用户比较积极时，添加适量聊天语解答用户问题，比如：今天天气真好、很荣幸见到小主等等；当用户比较平和时，正常作答。\n"
            "3、用户物流信息里包含了订单号、订单类型及订单状态！！！\n"
            "请根据已知信息、用户物流信息及用户当前情绪状态回答问题：\n\n"
            f"<已知信息>{context}</已知信息>\n"
            f"<用户物流信息>{user_info}</用户物流信息>\n"
            f"<订单号>{order_id}</订单号>"
            f"<用户当前情绪状态>{emotion}</用户当前情绪状态>\n"
            f"<问题>{user_question}</问题>\n"
        )
        response = llm.generate_response(prompt)
        pattern = r"^\('([^']+)',"
        match = re.search(pattern, str(response))
        main_content = match.group(1)
        dispatcher.utter_message(text=main_content)
        return [SlotSet("user_question", None)]


def get_user_info(order_id: str, tracker: Tracker) -> str:
    conn = sqlite3.connect("/home/caiqing/ssd1/jan/rasa/backend/rasa_chatbot_cn-master/database/order.db")
    cursor = conn.cursor()
    user_type = tracker.get_slot('user_type')

    cursor.execute('SELECT order_type,item_status FROM orders WHERE order_id = ?', (order_id,))
    row = cursor.fetchone()

    conn.close()
    if row:
        order_type, item_status = row
        print(f"订单号为{order_id},订单类型为{order_type},订单状态为{item_status}")
        return f"订单号为{order_id},订单类型为{order_type},订单状态为{item_status}"

    else:
        return "未找到相关的订单信息。"


class ActionProvideQuestionAnswer(Action):
    def name(self) -> str:
        return "action_handle_user_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.get_slot("user_question")
        print("query:", query)
        context = fetch_top_k_similar_questions(query, k=5)
        # context = tracker.get_slot('context')
        order_id = tracker.get_slot('order_id')
        user_info = get_user_info(order_id, tracker)
        emotion = tracker.get_slot('emotion')

        prompt = (
            "你是一位资深的物流客服。根据已知信息、用户物流信息和用户当前情绪状态，"
            "遵循以下原则及示例，你可以通过在已知信息中查找相关内容进行输出。\n"
            "原则：\n"
            "1、必须根据已知信息和用户物流信息作答！！！\n"
            "2、一定要观察用户情绪变化，当用户比较消极时，用最简便的方式解答用户问题；当用户比较积极时，添加适量聊天语解答用户问题，比如：今天天气真好、很荣幸见到小主等等；当用户比较平和时，正常作答。\n"
            "3、用户物流信息里包含了订单号、订单类型及订单状态！！！\n"
            "请根据已知信息、用户物流信息及用户当前情绪状态回答问题：\n\n"
            f"<已知信息>{context}</已知信息>\n"
            f"<用户物流信息>{user_info}</用户物流信息>\n"
            f"<订单号>{order_id}</订单号>"
            f"<用户当前情绪状态>{emotion}</用户当前情绪状态>\n"
            f"<问题>{query}</问题>\n"
        )
        response = llm.generate_response(prompt)
        print("response:", response)
        pattern = r"^\('([^']+)',"
        match = re.search(pattern, str(response))
        main_content = match.group(1)
        dispatcher.utter_message(text=main_content)
        return [SlotSet("context", query)]
