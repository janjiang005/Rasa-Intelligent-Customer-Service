<template>
    <div class="Test_upload">
        <div class="content3">
            <h2>知识库管理</h2>
            <el-form :model="form">


                <div class="pic">
                    <el-form-item class="el_form_item">
                        <h3>选择文件上传(至多可添加{{ limitNum }}条)</h3>

                        <el-upload
                            :multiple="multiple"
                            ref="upload"
                            action=""
                            :limit="limitNum"
                            accept=".json,.pdf,.docx"
                            :auto-upload="false"
                            :file-list="Audio_list"
                            :on-exceed="handleExceed"
                            :on-change="handleChange"
                            :before-upload="handleBeforeUpload"
                            :on-remove="handleRemove"
                            :on-progress="uploadAudioProgress"
                        >

                            <el-button
                                slot="trigger"
                                size="small"
                                type="success"
                                >文件选取</el-button
                            >
                            <el-button
                                style="margin-left: 10px;"
                                size="small"
                                type="primary"
                                @click="uploadFile()"
                                >文件上传</el-button
                            >
                            <el-button size="small" @click="back()"
                                >取消上传</el-button
                            >
                            <div slot="tip" class="el-upload__tip">
                                只能上传json,pdf,docx文件，且不超过300Mb
                            </div>
                        </el-upload>
                    </el-form-item>
                </div>
            </el-form>
            <el-dialog
                title="文件上传"
                :visible.sync="dialog_UPprogress"
                width="40%"
                top="13%"
                :show-close="false"
            >
                <div class="Up_progress_icon">
                    <img
                        v-if="loading"
                        src="../assets/img/loading.gif"
                        alt=""
                    />
                    <img
                        v-if="!loading"
                        src="../assets/img/up_ending.jpeg"
                        alt=""
                    />
                </div>
                <div v-if="loading" class="Up_progress_word">
                    数据上传中...
                </div>
                <div v-if="!loading" class="Up_progress_word">
                    数据上传成功，{{ return_CountDown }}秒后进入知识库管理界面！
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
export default {
    name: "UploadImage",
    data() {
        return {
            // 上传进度提示
            dialog_UPprogress: false,
            // 返回倒计时
            return_CountDown: 3,
            limitNum: 3,
            form: {},
            Audio_list: [],
            //用于上传视频
            multiple: true,
            loading: true,
            timer: "",
            Audiourl_list: [],
            //展示视频列表
            show_tooltip: false,
            //  是否展示提示信息："选取视频文件进行预览！"
        };
    },
    methods: {
        // 上传文件之前的钩子
        handleBeforeUpload(file) {
            //这个钩子函数用于文件自动上传
        },
        uploadAudioProgress(event, file, fileList) {
            this.AudioUploadPercent = file.percentage.toFixed(0) * 1;
        },
        //超出个数限制时
        handleExceed(files, img_list) {
            this.$message.error(`一次最多上传${this.limitNum}个文件!`);
        },
        // 移除
        handleRemove(file, Audio_list) {
            this.Audio_list = Audio_list;
            //移除的时候同样将预览的视频url删除
            this.Audiourl_list = this.Audiourl_list.filter(
                item => item.name != file.name
            );
            this.show_tooltip = this.Audiourl_list.length == 0 ? true : false;
        },
          getFileType(name) {
            let startIndex = name.lastIndexOf('.')
            if (startIndex !== -1) {
                return name.slice(startIndex + 1).toLowerCase()
            } else {
                return ''
            }
        },


    handleChange(file, fileList) {
    let allowedTypes = ['json', 'pdf', 'docx'];
    let filetype = this.getFileType(file.name); // 获取文件后缀名或类型
    if (!allowedTypes.includes(filetype)) {
        this.$notify.warning({
            title: "警告",
            message: "请上传 JSON、PDF 或者 DOCX 文件！"
        });
        // 将不符合要求的文件从文件列表中移除
        fileList.pop();
    }


            let existFile = fileList
                .slice(0, fileList.length - 1)
                .find(f => f.name === file.name);
            if (existFile) {
                this.$message.error("当前文件已经存在!");
                fileList.pop();
            }
            this.fileList = fileList;
        },

    uploadFile() {
            if (this.fileList.length == 0) {
                this.$message({
                    showClose: true,
                    message: "每项任务至少包含一条数据，请重新进行选择！",
                    type: "error",
                    duration: 800
                });
                return;
            }

            this.dialog_UPprogress = true;
            let upload_data = new FormData();

            for (var item of this.fileList) {
                if (!item.raw && item.url.indexOf("blob") === -1) {
                } else {
                    upload_data.append("file", item.raw);
                }
            }


            this.$http({
                url: `${this.$backend_upload}/upload_file`,
                method: "post",
                data: upload_data
            })
                .then(backdata => {
                    var { status, data } = backdata;
                    if (status == 200) {
                        this.loading = false;
                        this.timer = window.setInterval(() => {
                            this.return_CountDown--;
                            if (this.return_CountDown == 0) {
                                clearTimeout(this.timer);
                                var id = data.task_id;
                                this.$router.push("/TaskdetailFile/" + id);
                            }
                        }, 1000);
                    }
                })
                .catch(err => {
                    this.$message({
                        message: "数据上传失败，请重新进行提交！",
                        type: "error",
                        duration: 900
                    });
                });
        },
        back() {
            this.$router.push("/Allfunc");
        }
    },
    beforeDestroy() {
        clearTimeout(this.timer);
    }
};


</script>

<style scoped>
@import url("../assets/css/Upload.css");
</style>

