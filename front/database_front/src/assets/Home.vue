<template>
<div class="Home">
    <div class="block1">
            <img src="../assets/left.png" class="img">    
            <img src="../assets/right.png" class="img">   
    </div>
    <div class="block2" >   
        <el-tabs v-model="activeName" >
            <el-tab-pane label="功能台" name="first">
                <Function></Function>
            </el-tab-pane>
            <el-tab-pane label="任务中心" name="second">
                <TaskCenter></TaskCenter>
            </el-tab-pane>
            <el-tab-pane label="关于我们" name="third">
                <About></About>
            </el-tab-pane>
        </el-tabs>
    </div>   
</div>
</template>

<script>
import Function from '../components/Function'
import TaskCenter from '../components/TaskCenter'
import About from '../components/About'


export default {
    name:'Home',
    data() {
      return {
        activeName:'first'
      };
    },
    components:{
        Function,
        TaskCenter,
        About
    },
    
  };
</script>

<style>
.Home{
    width: 100%;
    height: 55px;
    background: #eeeff4;
}
.img{
    width: auto;
    height: 13px;
    border: 1.5px solid #DCDFE6;
    padding: 3px 8px 3px 8px;
    margin-left: 6px;
}
.block1{
    float: left;
    margin-left: 8px;
    margin-top: 15px;
}
.block2{
    float: left;
    margin-left: 20px;
}
.el-tab-pane{
    width: 100%;
    height: auto;
}
</style>