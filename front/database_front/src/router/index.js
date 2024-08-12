import Vue from "vue";
import Router from "vue-router";
import Homepage from "@/components/Homepage";
import Home from "@/components/Home";
import Allfunc from "@/components/Allfunc";
import ProvinceDetails from "@/components/ProvinceDetails"
//知识库管理（上传文件）
import UploadFile from "@/components/UploadFile"
import TaskdetailFile from "@/components/TaskdetailFile";
//数据可视化
import QuestionList from "@/components/QuestionList"

import Aboutus from "@/components/Aboutus"


Vue.use(Router);
const originalPush = Router.prototype.push;
Router.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err);
};

export default new Router({
    mode: "history",
    routes: [
        {
            path: "/",
            component: Homepage,
            children:[
                {path:"/",name:"Home",component: Home},
                {path:"/Allfunc",name:"Allfunc",component: Allfunc},
                {path: "/UploadFile", name: "UploadFile", component: UploadFile}, //功能台
                {path: "/QuestionList", name: "QuestionList", component: QuestionList}, //数据可视化
                {path:"/TaskdetailFile/:id",name:'TaskdetailFile',component: TaskdetailFile},
                {
                  path: '/province-details/:province',
                  name: 'ProvinceDetails',
                  component: ProvinceDetails,
                  props: true,
                },
                {path:"/Aboutus",name:'Aboutus',component: Aboutus}
            ]
        }


    ]
})