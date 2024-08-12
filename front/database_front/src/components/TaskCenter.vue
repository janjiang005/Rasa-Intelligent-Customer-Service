<template>
    <div class="taskcenter">
        <div class="content2">
            <div class="back2">
                <el-table
                    :data="Tasklist_display"
                    border
                    class="tabtop13"
                    align="center"
                >
                    <el-table-column
                        property="id"
                        label="任务ID"
                        width="65"
                        align="center"
                    >
                    </el-table-column>
                    <el-table-column
                        property="task_name"
                        label="任务类型"
                        width="180"
                        align="center"
                    >
                    </el-table-column>
                    <el-table-column
                        property="task_tag"
                        label="状态"
                        width="80"
                        align="center"
                    >
                    </el-table-column>
                    <el-table-column
                        property="start_time"
                        label="开始时间"
                        width="230"
                        align="center"
                    >
                    </el-table-column>
                    <el-table-column
                        property="end_time"
                        label="结束时间"
                        width="230"
                        align="center"
                    >
                    </el-table-column>
                    <el-table-column label="操作" align="center">
                        <template slot-scope="scope">
                            <el-button
                                type="primary"
                                size="mini"
                                @click="
                                    check_task(
                                        scope.row.id,
                                        scope.row.task_name
                                    )
                                "
                                >查看</el-button
                            >
                            <el-button
                                type="primary"
                                size="mini"
                                v-bind:disabled="scope.row.stu"
                                @click="
                                    download_taskres(
                                        scope.row.id,
                                        scope.row.task_name
                                    )
                                "
                                >下载处理结果</el-button
                            >
                            <el-button
                                type="danger"
                                size="mini"
                                @click="
                                    confirmdelete(
                                        scope.row.id,
                                        scope.row.task_name
                                    )
                                "
                                >删除任务</el-button
                            >
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div class="Pagination">
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[5, 10, 20, 50]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :page-size="page_size"
                    background
                    prev-text="上一页"
                    next-text="下一页"
                    :total="count"
                >
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            Tasklist: [],
            Tasklist_display: [],
            nowTime: "",
            dialogVisible: false,
            currentPage: 1,
            count: 0,
            page_size: 5,
            begin_index: 0,
            end_index: -1,
            task_type: {
                // 需要展示其任务类型中文名
                Question:'数据可视化',
                Upload:'知识库更新'
            }
        };
    },

    methods: {
        // 因当前页码变化更新展示数据的index
        handleCurrentChange(val) {
            this.currentPage = val;
            this.begin_index = (this.currentPage - 1) * this.page_size;
            this.end_index =
                this.currentPage * this.page_size - 1 > this.count - 1
                    ? this.count - 1
                    : this.currentPage * this.page_size - 1;

            this.update_display_tasklist();
        },
        // 因当前每页数据条数变化更新展示数据的index
        handleSizeChange(val) {
            this.page_size = val;
            this.begin_index = (this.currentPage - 1) * this.page_size;
            this.end_index =
                this.currentPage * this.page_size - 1 > this.count - 1
                    ? this.count - 1
                    : this.currentPage * this.page_size - 1;
            this.update_display_tasklist();
        },
        // 根据index信息将展示的数据放入 this.Tasklist_display用于展示
        update_display_tasklist() {
            this.Tasklist_display = [];
            for (let i = this.begin_index; i <= this.end_index; i++) {
                var task = {};

                if (this.Tasklist[i].task_tag == "True") {
                    task.task_tag = "处理中";
                    task.end_time = "尚未结束";
                    task.stu = true;
                } else {
                    task.task_tag = "结束";
                    task.stu = false;

                    task.end_time = this.Tasklist[i].end_time;
                }
                task.id = this.Tasklist[i].id;
                task.task_name = this.task_type[this.Tasklist[i].task_name];
                task.start_time = this.Tasklist[i].start_time;

                this.Tasklist_display.push(task);
            }
        },
        // 取消删除
        handleClose(done) {
            this.$confirm("取消删除？")
                .then(_ => {
                    done();
                })
                .catch(_ => {});
        },
        //  获取全部数据
        getTasklistall(mes) {
            this.Tasklist = [];
            this.$http({
                url: `${this.$backend_all}`,
                method: "get"
            })
                .then(backdata => {
                    var { data, status } = backdata;
                    if (status == 200) {
                        if (mes) {
                            this.$message({
                                message: "成功获取所有任务!",
                                type: "success",
                                duration: 600
                            });
                        }
                        this.Tasklist = data;
                        this.count = this.Tasklist.length;
                        // 更新任务展示的起始和结束下标
                        this.begin_index =
                            (this.currentPage - 1) * this.page_size;
                        this.end_index =
                            this.currentPage * this.page_size - 1 >
                            this.count - 1
                                ? this.count - 1
                                : this.currentPage * this.page_size - 1;
                        this.update_display_tasklist();
                    }
                })
                .catch(function(error) {
                    that.$message({
                        message: "数据获取失败，即将返回！",
                        type: "error",
                        duration: 900
                    });
                });
        },
        // 查看任务,根据任务id和任务类型查看对应任务处理结果
        check_task: function(id, taskname) {
            var task_item = this.get_taskitem(taskname);
            console.log(task_item);
            if (task_item == "Question") {
                this.$router.push("/QuestionList");
            } else if (task_item == "Upload") {
                this.$router.push("/TaskdetailFile/" + id);
            }
             else {
                this.$message({
                    message: "出错，任务类型不存在！",
                    type: "error",
                    duration: 600
                });
            }
        },

        getTask_url: function(taskname) {
            // 根据对应的任务类型选择对应的后端服务
            var task_item = this.get_taskitem(taskname);
            if (task_item == "Question") {
                return this.$backend_questionlist;
            } else if (task_item == "Upload") {
                return this.$backend_upload;
            }
            else {
                this.$message({
                    message: "出错，任务类型不存在！",
                    type: "error",
                    duration: 600
                });
                return null;
            }
        },
        // 下载任务处理结果
        download_taskres: function(id, taskname) {
            //获取转发地址
            console.log(taskname);
            let forward_adress = this.getTask_url(taskname);
            this.$http({
                url: `${forward_adress}/download_result/${id}`,
                method: "get",
                responseType: "blob"
            }).then(backdata => {
                var { status, data, headers } = backdata;
                if (status == 200) {
                    this.$message({
                        message: "成功下载识别结果！",
                        type: "success",
                        duration: 600
                    });

                    const blobUrl = window.URL.createObjectURL(data);
                    const a = document.createElement("a");
                    a.style.display = "none";
                    a.download = headers.file_name;
                    a.href = blobUrl;
                    a.click();
                } else {
                    this.$message({
                        message: "下载出错！",
                        type: "error",
                        duration: 600
                    });
                }
            });
        },
        //二次确认后根据id删除任务
        confirmdelete: function(id, taskname) {
            let forward_adress = this.getTask_url(taskname);
            this.$confirm("此操作将永久删除该任务, 是否继续?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning"
            })
                .then(() => {
                    this.$http({
                        url: `${forward_adress}/delete_task/${id}`,
                        method: "get"
                    }).then(backdata => {
                        var { status } = backdata;
                        if (status == 200) {
                            this.$message({
                                message: "删除成功",
                                type: "success",
                                duration: 600
                            });
                            if (
                                this.begin_index == this.end_index &&
                                this.begin_index > 0
                            ) {
                                this.handleCurrentChange(this.currentPage - 1);
                            }
                            this.getTasklistall(false);
                        }
                    });
                })
                .catch(() => {
                    this.$message({
                        type: "info",
                        message: "已取消删除",
                        duration: 600
                    });
                });
        },
        get_taskitem: function(taskvalue) {
            for (var item in this.task_type) {
                if (this.task_type[item] == taskvalue) return item;
            }
            return null;
        }
    },
    mounted() {
        this.$emit("func", 2);
        this.getTasklistall(true);
    }
};
</script>
<style scoped>
@import url("../assets/css/TaskCenter.css");
</style>

