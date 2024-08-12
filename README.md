## 一、智能客服模块
### 1、前端
(1)进入front/rasa_bot_front-main<br/>
(2)执行命令
> npm start
### 2、后端
(1)进入backend/rasa_chatbot_cn-master<br/>
(2)根据nlu.yml训练rasa框架
> rasa train

(3)运行action
> rasa run actions

(4)启动Rasa对话系统
>rasa run -m models --enable-api --cors "*"

## 二、后台管理系统
### 1、前端
(1)进入front/database_front<br/>
(2)执行命令
> npm run dev

### 2、后端
(1)进入questionlist启动数据可视化页面
> python app.py

(2)进入upload_kb启动知识库管理页面
> python app.py

