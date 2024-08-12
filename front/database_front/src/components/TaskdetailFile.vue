<template>
    <div class="audiodetail">
        <div class="content">
            <h3>知识库管理</h3>
            <div class="task_detail">
                <div class="span_group1">
                    <span class="span1">当前状态:{{ state }}</span>
                    <br />
                    <span class="span1">开始时间:{{ start_time }}</span>
                </div>
                <div class="span_group2">
                    <span class="span2">任务ID:{{ task_id }}</span>
                    <br />
                    <span class="span2">结束时间:{{ end_time }}</span>
                </div>
            </div>
            <br />
            <br />

            <div class="fenge"></div>
            <div class="progress">
                <h3>处理进度</h3>
                <br />
                <el-steps :active="active" finish-status="success">
                    <el-step title="创建任务"></el-step>
                    <el-step title="处理中"></el-step>
                    <el-step title="结束"></el-step>
                </el-steps>
            </div>

            <div class="result">
                <h3>处理结果</h3>
                <table class="table1">
                    <tr>
                        <th class="th1">知 识 库 ID</th>
                        <th class="th2">文 件 名</th>
                        <th class="th3">划 分 结 果</th>

                    </tr>
                    <tr v-for="content in displaydata" :key="content.id">
                        <td class="main_content">
                            {{ content.id }}
                        </td>
                        <td class="main_content">
                            {{ content.filename }}
                        </td>
                        <td class="main_content">
                            {{ content.chunk }}
                        </td>

                    </tr>
                </table>
            </div>
        </div>
    </div>
</template>
<script scoped>
export default {
    name: "audiodetail",
    data() {
        return {
            task: {},
            task_display: {},
            state: "结束",
            task_id: "1",
            start_time: "2022年3月20日16:00",
            end_time: "2022年3月20日16:30",
            start_time: "",
            end_time: "",
            active: 2,
            stu: true,
            sta: "",
            timer: "",
            displaydata: []
        };
    },
    methods: {
        getTimeFormat: function(date) {
            let year = date.getFullYear(); //获取年
            let month = date.getMonth() + 1; //获取月
            let day = date.getDate(); //获取日
            let Hours = date.getHours(); //获取时
            let minutes = date.getMinutes(); //获取分
            let Seconds = date.getSeconds(); //获取秒
            return `${year}年${month}月${day}日 ${Hours}:${minutes}:${Seconds}`;
        },
        //async getVoiceToText(url) {
        //    let { data } = await this.$http({
        //        url: `${this.$backend_voiceidf}/voice_rec`,
        //        method: "get"
        //    });
        //    return data[0];
        //},
        // 获取任务信息
        async getTaskInfo() { //"original_noise","result_noise","result_time":{"end","start"},"result_text","task_id"
            let {data , status}  = await this.$http({
                url: `${this.$backend_upload}/upload_file`,
                method: "get"
            });

            // return;

            for(let i = 0;i < data.length;i++){
                if (status == 200) {

                    this.$message({
                        message: "任务" + data[i]["task_id"]+ "数据信息获取成功！",
                        type: "success",
                        duration: 900
                    });
                } else {
                    this.$message({
                        message: "任务" + data[i]["task_id"]+ "数据信息获取失败！",
                        type: "error",
                        duration: 900
                    });
                    return;
                }
            }

            let task_info = data;
            this.sta = task_info.task_tag;
            this.task_id = data[0]["task_id"]

            this.start_time = this.getTimeFormat(
                new Date()
            );
            if (this.sta == 1) {
                this.active = 2;
                this.state = "处理中";
                this.stu = true;
                this.end_time = " 暂未结束";
            } else {
                this.active = 3;
                this.stu = false;
                this.state = "结束";
                clearTimeout(this.timer);
                this.end_time = this.getTimeFormat(
                    new Date()
                );
            }
            for(let i = 0;i < data.length;i++){
                let dataone = {};
                dataone.id = data[i]["task_id"];
                dataone.filename = data[i]["filename"]
                dataone.chunk = data[i]["chunk"]
                this.displaydata.push(dataone);
            }




        },


    },
    mounted() {
        this.task_id = this.$route.params.id;
        this.getTaskInfo();
        // 轮询机制；每过十秒请求一次，直至任务状态为结束
        this.timer = window.setInterval(() => {
            setTimeout(() => {
                this.getTaskInfo();
            }, 0);
        }, 10000);
    },
    beforeDestroy() {
        clearTimeout(this.timer);
    }
};
</script>

<style scoped>
.audiodetail {
    width: 100%;
    height: 100%;
    padding-top: 20px;
    background-color: #e6edf2;
    overflow: scroll;
    font-family: sans-serif;
}
.content {
    width: 85%;
    height: auto;
    background-color: white;
    margin: 20px auto;
    padding-bottom: 30px;
    /* min-height: 700px; */
}
.content h3 {
    padding-top: 20px;
    padding-left: 5%;
}
.span1 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8px;
    color: #585a5b;
}
.span2 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8px;
    color: #585a5b;
}

.task_detail {
    display: flex;
}
.span_group1 {
    margin-left: 5%;
}
.span_group2 {
    margin-left: 15%;
}
.label1 {
    border-radius: 3px;

    color: white;
    padding: 6px 5px;
    margin-left: 5%;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
}
.label2 {
    border-radius: 3px;
    background-color: #d51623;
    color: white;
    padding: 6px 6px;
    margin-left: 35px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
}
.fenge {
    width: 95%;
    border-top: 1px solid #979b9b;
    margin: auto;
    margin-top: 20px;
    margin-bottom: 20px;
}
.progress {
    width: 90%;
    margin: auto;
}
.progress h3 {
    padding-left: 0%;
}
.result {
    width: 95%;
    margin: auto;
    padding-bottom: 5%;
}
.result h3 {
    margin-top: 40px;
    margin-bottom: 20px;
    padding-left: 2%;
}
.table1 {
    width: 95%;
    padding-bottom: 10px;
    margin: auto;
    text-align: center;
}

.main_content {
    background-color: #eaeef0;
    text-align: center;
    padding: 10px 3px 3px 10px;
}
audio {
    width: 100%;
}
.th1 {
    width: 4%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th2 {
    width: 20%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th3 {
    width: 20%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th4 {
    width: 20%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th5 {
    width: 20%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th6 {
    width: 20%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th7{
    width: 8%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
.th8 {
    width: 8%;
    background-color: #84C9EF;
    color: white;
    font-size: 15px;
    padding: 10px 5px 5px 10px;
}
</style>

