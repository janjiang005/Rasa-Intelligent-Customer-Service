<template>
  <div class="container">
    <div class="title">
      <img class="img" src="../assets/img/shouye.png" />
      <h2 style="font-size:30px;font-family:'MyCustomFont2'">喵喵客服：后台管理系统</h2>
      <h2 style="font-family: Poppins">Meow Meow Customer Service:<br/> Backend Management System</h2>
    </div>
    <div class="items">
      <div class="item" ref="cardRef1" @click="question_list()">
        <img src="../assets/img/data.png" class="item-img" />
        <div class="item-text">数据可视化</div>
      </div>
      <div class="item" ref="cardRef2" @click="upload_file()">
        <img src="../assets/img/kb.png" class="item-img" />
        <div class="item-text">知识库管理</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
   methods: {
        question_list: function() {
            this.$router.push("/QuestionList");
        },
        upload_file: function(){
            this.$router.push("/UploadFile")
        },

    },
  mounted() {
    // Function to handle the mouse enter event
    const handleMouseEnter = (event) => {
      const target = event.currentTarget;
      // Increase the size of the hovered item
      target.style.transform = 'scale(1.1)';

      // Decrease the size of other items
      this.$refs.items.forEach(item => {
        if (item !== target) {
          item.style.transform = 'scale(0.9)';
        }
      });
    };

    // Function to handle the mouse leave event
    const handleMouseLeave = (event) => {
      const target = event.currentTarget;
      // Reset the size of the hovered item
      target.style.transform = 'scale(1)';

      // Reset the size of other items
      this.$refs.items.forEach(item => {
        if (item !== target) {
          item.style.transform = 'scale(1)';
        }
      });
    };

    // Function to handle the click event and navigate to the URL
    const handleItemClick = (event) => {
      const target = event.currentTarget;
      const url = target.getAttribute('data-url');
      if (url) {
        // Use Vue Router for navigation (assuming you have Vue Router set up)
        this.$router.push(url);
      }
    };

    // Get the items and add event listeners
    const items = this.$refs.items = [this.$refs.cardRef1, this.$refs.cardRef2];

    items.forEach(item => {
      if (item) {
        item.addEventListener('mouseenter', handleMouseEnter);
        item.addEventListener('mouseleave', handleMouseLeave);
        item.addEventListener('click', handleItemClick);
      }
    });
  }
};
</script>

<style scoped lang="less">
  @font-face {
  font-family: 'MyCustomFont'; /* Give the font a name */
  src: url('../assets/font/Leefont蒙黑体.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
  @font-face {
  font-family: 'MyCustomFont2'; /* Give the font a name */
  src: url('../assets/font/荆南麦圆体.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}
.container {
    display: flex;
    align-items: flex-start; /* 垂直对齐顶部 */
    overflow: hidden;
    width: 100%;
    background-color: #ffdee9;
    background-image: -webkit-linear-gradient(0deg, #ffdee9 0%, #b5fffc 100%);
    background-image: -moz-linear-gradient(0deg, #ffdee9 0%, #b5fffc 100%);
    background-image: -o-linear-gradient(0deg, #ffdee9 0%, #b5fffc 100%);
    background-image: linear-gradient(0deg, #ffdee9 0%, #b5fffc 100%);
}

.title {
  text-align: center;
  font-family: sans-serif;
  font-size: 15px;
  margin-top: -25px;
}



.img {
  margin-top: 30px;
  margin-right: 90px;
  margin-left: 80px;
  overflow: hidden;
}

.items {
  margin-top: 80px;
  display: flex;
  flex-direction: column;
  gap: 60px; /* 调整两个div之间的间距 */
  margin-bottom: 20px;
  overflow: hidden;
}

.item {
  position: relative;
  width: 650px;
  height: 350px;
  background: #c4e1f6;
  opacity: 0.8;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
  filter: drop-shadow(2px 4px 8px #f1f1f2);
  border-radius: 30px;
  text-align: center;
  overflow: hidden;
}

.item-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.3s ease;
}

.item-text {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 24px;
  color: white;
  background: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-family: 'MyCustomFont';
}

.item:hover .item-img {
  filter: blur(5px);
}

.item:hover .item-text {
  opacity: 1;
}
</style>

