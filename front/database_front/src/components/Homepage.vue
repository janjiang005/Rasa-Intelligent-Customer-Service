<template>
    <div class="div1">
        <div class="navi">
            <div
                class="choose"
                name="first"
                @click="Allfunc"
                :class="{ choose1: isclick_func }"
            >
                <img v-if="isclick_func" src="../assets/img/function1.png" />
                <img v-if="!isclick_func" src="../assets/img/function.png" />
                <label>功能台</label>
            </div>
            <div
                class="choose"
                name="second"
                @click="Aboutus"
                :class="{ choose1: isclick_aboutus }"
            >
                <img v-if="isclick_aboutus" src="../assets/img/about1.png" />
                <img v-if="!isclick_aboutus" src="../assets/img/about.png" />
                <label>关于我们</label>
            </div>

        </div>
        <div class="content">
            <router-view @func="getMsgFromSon" />
        </div>
    </div>
</template>

<script>

export default {

    data() {
        return {
            isclick_func: false,
            isclick_aboutus: false,
            url: ["/"]
        };
    },
    methods: {
        getMsgFromSon: function(id) {
            if (id == 0) {
                this.isclick_func = false,
                this.isclick_aboutus = false;
            } else if (id == 1) {
                this.isclick_func = true;
                this.isclick_aboutus = false;
            }  else if (id == 2) {
                this.isclick_func = false;
                this.isclick_aboutus = true;
            } else {
                this.$message({
                    showClose: true,
                    message: "未定义界面！",
                    type: "error",
                    duration: 600
                });
            }
        },
        Allfunc: function() {
            this.$router.push("/Allfunc");
        },
        Aboutus: function() {
            this.$router.push("/Aboutus");
        }
    },
    created() {
        this.$router.push("/Allfunc");
    }
};

</script>



<style scoped>
@import url("../assets/css/Homepage.css");
</style>
