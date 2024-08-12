// 引入axios
import Axios from "axios";

// 创建axios对象，设置请求的基准地址

// 封装成插件 一个对象
var myplugin_axios = {};
myplugin_axios.install = function(Vue) {
    var axios_obj = Axios.create({
        baseURL: "http://localhost:5001"
        // baseURL: "http://127.0.0.1:81/back_end"
    });

    // 使用axios对象的拦截器，进行请求的判断及处理
    // 此处主要为了接收token或者设置token进行用户验证
    // 暂不使用
    axios_obj.interceptors.request.use(function(conf) {
        // 任何时候都需要返回
        return conf;
    });

    // 将处理好的axios对象重新赋值给vue的原型对象

    Vue.prototype.$http = axios_obj;
    //访问图像视频的ip：端口号
    Vue.prototype.$url = "http://localhost:5001/";

    //后台工作人员上传文件
    Vue.prototype.$backend_upload = "upload"
    //数据可视化
    Vue.prototype.$backend_data = "questionlist"

};
// 将插件导出
export default myplugin_axios;
