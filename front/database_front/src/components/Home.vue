<template>
    <div class="divcls">
        <h1>这里即将展示具体功能</h1>
    </div>
</template>
<style scoped>
.divcls {
    min-height: 800px;
    background-color: rgb(238, 237, 237);
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center;
}
</style>
<script>
export default {
    //import引入的组件需要注入到对象中才能使用

    components: {},
    data() {
        //数据

        return {};
    },
    methods: {},
    //生命周期 - 创建完成（可以访问当前this实例）

    created() {},
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        this.$emit("func", 0);
    },
    beforeCreate() {}, //生命周期 - 创建之前
    beforeMount() {}, //生命周期 - 挂载之前
    beforeUpdate() {}, //生命周期 - 更新之前
    updated() {}, //生命周期 - 更新之后
    beforeDestroy() {}, //生命周期 - 销毁之前
    destroyed() {}, //生命周期 - 销毁完成
    activated() {} //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
