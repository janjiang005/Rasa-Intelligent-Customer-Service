import sqlite3

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

from flask_cors import CORS
#CORS(app)  # 允许所有的 CORS 请求，也可以根据需要配置特定的允许源

app = Flask(__name__)
CORS(app)  # 允许所有的 CORS 请求，也可以根据需要配置特定的允许源

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Type, X-Requested-With,file_name'
    return response


# 假设你已经配置好数据库连接
engine = create_engine('sqlite:///user.db')

@app.route('/initialData', methods=['GET'])
def get_initial_data():
    with engine.connect() as conn:
        province_result = conn.execute(text("SELECT DISTINCT province, city FROM user"))
        provinces_set = set()
        for row in province_result:
            province = row[0] if row[0] else row[1]
            provinces_set.add(province)
        provinces = list(provinces_set)

        user_types_result = conn.execute(text("SELECT DISTINCT user_type FROM user"))
        user_types = [row[0] for row in user_types_result]
        print(user_types)
    return jsonify({
        'provinces': provinces,
        'userTypes': user_types,
    })

@app.route('/questions', methods=['GET'])
def get_questions():
    province = request.args.get('province')
    user_type = request.args.get('userType')

    if not province or not user_type:
        return jsonify({'error': 'Missing parameters'}), 400

    query = text("""
        SELECT order_id, order_type, question, times
        FROM user
        WHERE province = :province AND user_type = :user_type
        ORDER BY question DESC
        LIMIT 5
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {'province': province, 'user_type': user_type})
        questions = [{'order_id': row[0], 'order_type': row[1], 'question': row[2], 'times':row[3]} for row in result]

    return jsonify({'questions': questions})

@app.route('/mapData', methods=['GET'])
def map_data():
    try:

        conn = sqlite3.connect('user.db')

        cursor = conn.cursor()
        cursor.execute('''
            SELECT province, COUNT(*) as count 
            FROM user 
            GROUP BY province
        ''')
        rows = cursor.fetchall()
        result = [{'province': row[0], 'count': row[1]} for row in rows]
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching map data: {e}")
        return jsonify([]), 500
    finally:
        conn.close()

#
# @app.route('/provinceData', methods=['GET'])
# def city_data():
#     try:
#         conn = sqlite3.connect('user.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             SELECT province, COUNT(*) as count
#             FROM user
#             GROUP BY province
#         ''')
#         rows = cursor.fetchall()
#
#         total_count = sum(row[1] for row in rows)
#         result = [{'name': row[0], 'count': row[1], 'percentage': (row[1] / total_count) * 100} for row in rows]
#
#         return jsonify(result)
#     except Exception as e:
#         print(f"Error fetching city data: {e}")
#         return jsonify([]), 500
#     finally:
#         conn.close()

@app.route('/provinceData', methods=['GET'])
def province_data():
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT province, city,user_type, COUNT(*) as count 
            FROM user 
            GROUP BY province, user_type
        ''')
        rows = cursor.fetchall()

        province_data = {}
        for row in rows:
            province, city,user_type, count = row
            if province == "":
                province = city
            if province not in province_data:
                province_data[province] = {'received': 0, 'sent': 0}
            if user_type == '收件':
                province_data[province]['received'] += count
            elif user_type == '寄件':
                province_data[province]['sent'] += count

        result = []
        for province, data in province_data.items():
            result.append({'name': province, 'received': data['received'], 'sent': data['sent']})

        return jsonify(result)
    except Exception as e:
        print(f"Error fetching province data: {e}")
        return jsonify([]), 500
    finally:
        conn.close()

@app.route('/provinceDetails', methods=['GET'])
def get_province_details():
    province = request.args.get('province')
    if not province:
        return jsonify({"error": "Province is required"}), 400

    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        # 获取问题列表，按出现次数降序排列，并限制为前5个
        cursor.execute('''
            SELECT question, SUM(times),emotion,confidence as total_times 
            FROM user 
            WHERE province = ? 
            GROUP BY question 
            ORDER BY total_times DESC 
            LIMIT 5
        ''', (province,))
        questions = cursor.fetchall()

        question_list = [{"question": row[0], "times": row[1],"emotion":row[2],"confidence":row[3]} for row in questions]

        # 获取情绪分布
        cursor.execute('''
            SELECT emotion, COUNT(*) as count 
            FROM user 
            WHERE province = ? 
            GROUP BY emotion
        ''', (province,))
        emotions = cursor.fetchall()

        emotion_data = [{"name": row[0], "value": row[1]} for row in emotions]

        return jsonify({"questions": question_list, "emotions": emotion_data})

    except Exception as e:
        print(f"Error fetching province details: {e}")
        return jsonify({"error": "Error fetching province details"}), 500

    finally:
        conn.close()



if __name__ == '__main__':
    app.run(host='localhost',port=6030,debug=True,threaded=True)
