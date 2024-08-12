<template>
    <div id="app" class="div_id">
       <router-view></router-view>
    </div>
</template>

<script>
export default {
    name: "App"
};
</script>

<style>
.div_id {
    height: 100%;
    width:100%;
    background: url("assets/img/back.jpg");
    position: relative;
    /* margin-top: -0.4%;
    margin-left: -0.4%; */
    /* background-repeat: no-repeat;

    background-size: 100% 100%;

    background-attachment: fixed; */
}
</style>
