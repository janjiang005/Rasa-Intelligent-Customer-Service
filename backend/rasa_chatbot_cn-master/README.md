# Rasa Core and Rasa NLU
## rasa对话系统系列文章
- [rasa对话系统踩坑记（一）](https://www.jianshu.com/p/5d9aa2a444a3)
- [rasa对话系统踩坑记（二）](https://www.jianshu.com/p/4ecd09be4419)
- [rasa对话系统踩坑记（三）](https://www.jianshu.com/p/ae028903d748)
- [rasa对话系统踩坑记（四）](https://www.jianshu.com/p/9393d319e698)
- [rasa对话系统踩坑记（五）](https://www.jianshu.com/p/eec63e56db07)
- [rasa对话系统踩坑记（六）](https://www.jianshu.com/p/21808ac8d409)
- [rasa对话系统踩坑记（七）](https://www.jianshu.com/p/405c087c2f7f)
- [rasa对话系统踩坑记（八）](https://www.jianshu.com/p/6a93209c48a4)
- [rasa对话系统踩坑记（九）](https://www.jianshu.com/p/1a4abe93635e)
- [rasa对话系统踩坑记（十）](https://www.jianshu.com/p/debcf0041fcb)
- [rasa-nlu的究极形态](https://www.jianshu.com/p/553e37ffbac0)
- [闲聊模型的实践并应用到rasa](https://www.jianshu.com/p/bccf2321bd50)

## Introduction
rasa版本已经更新到了2.0版本，改动比较大，等2.0版本稳定后再跟进了。现在这里的代码还是去年上半年的版本，后面rasa做了很多改动，component已经支持bert，对中文的支持也更好。所以这个之前基于1.1.x的版本就转到1.1.x分支，目前master分支的话就分享最新的基于1.10.18的一套支持中文的pipeline
> 欢迎加入**rasa微信闲聊群**，微信请加：coffee199029

## Running by command
### install packages
 - python >= 3.6
```
pip install -r requirements.txt
```
下载依赖package

### train model
```
make train
```

### run model
```
make run
```

### test in cmdline
```
make shell
```
可以在命令行中测试

### test by http server
`http://localhost:5005/webhooks/rest/webhook` post请求，请求参数例如：
```
{
    "sender": "0001",
    "message": "你好"
}
```
可以使用postman去请求调用

### use rasa x
```
make run-x
```
