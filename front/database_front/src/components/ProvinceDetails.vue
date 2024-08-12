<template>
  <div class="province-details">
    <h2>{{ province }}情感分析结果</h2>
    <div class="content-container">
      <div class="left-side">
        <div class="emotion-image" v-if="emotionImage">
          <img :src="emotionImage" alt="Emotion Image" />
        </div>
      </div>
      <div class="right-side">
        <div class="chart">
          <div class="com-chart" ref="chart_ref"></div>
        </div>
        <el-table
          class="fixedtableHeight"
          v-loading="listLoading"
          :data="showList"
          stripe
          tooltip-effect="dark"
          style="width: 90%; margin-top:40px; background: white; margin-left:100px;"
        >

                <el-table-column prop="question" label="问题" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.question }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="times" label="出现次数" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.times }}</span>
            </template>
          </el-table-column>
           <el-table-column prop="question" label="情绪" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.emotion }}</span>
            </template>
          </el-table-column>
           <el-table-column prop="question" label="置信度" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.confidence }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import positiveImage from '@/assets/img/positive.png';
import negativeImage from '@/assets/img/negative.png';
import neutralImage from '@/assets/img/neutral.png';

export default {
  props: ['province'],
  data() {
    return {
      listLoading: false,
      showList: [],
      chartInstance: null,
      emotionImage: '',
    };
  },
  created() {
    this.fetchProvinceDetails();
  },
  mounted() {
    this.initChart();
    window.addEventListener("resize", this.screenAdapter);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.screenAdapter);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    async fetchProvinceDetails() {
      this.listLoading = true;
      try {
        const response = await fetch(`http://localhost:5001/questionlist/provinceDetails?province=${this.province}`);
        const data = await response.json();
        if (data && data.questions) {
          this.showList = data.questions;
          this.updateChart(data.emotions);
        }
      } catch (error) {
        console.error('Error fetching province details:', error);
      } finally {
        this.listLoading = false;
      }
    },
    initChart() {
      this.chartInstance = echarts.init(this.$refs.chart_ref);
      const initOption = {
        title: {
          text: "情绪分布",
          left: 20,
          top: 20,
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [
          {
            name: '情绪',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            itemStyle: {
              color: function (params) {
                const colorList = ['#FF7F50', '#87CEEB', '#DA70D6','#d05667'];
                return colorList[params.dataIndex];
              }
            }
          }
        ]
      };
      this.chartInstance.setOption(initOption);
    },
    updateChart(emotions) {
      const options = this.chartInstance.getOption();
      options.series[0].data = emotions;
      this.chartInstance.setOption(options);

      // Determine the emotion with the highest percentage
      let maxEmotion = '';
      let maxPercentage = 0;
      emotions.forEach(emotion => {
        if (emotion.value > maxPercentage) {
          maxPercentage = emotion.value;
          maxEmotion = emotion.name;
        }
      });

      // Set the emotion image based on the max emotion
      if (maxEmotion === '积极') {
        this.emotionImage = positiveImage;
      } else if (maxEmotion === '消极') {
        this.emotionImage = negativeImage;
      } else if (maxEmotion === '平和') {
        this.emotionImage = neutralImage;
      } else {
        this.emotionImage = '';
      }
    },
    screenAdapter() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    }
  }
};
</script>

<style scoped>
@font-face {
  font-family: 'MyCustomFont2';
  src: url('../assets/font/HarmonyOS_Sans_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.province-details {
  font-family: 'MyCustomFont2';
  padding: 20px;
  background: #f0f2f5;
}
.content-container {
  display: flex;
}
.left-side {
  flex: 1;
  padding-right: 20px;
}
.right-side {
  flex: 2;
}
.chart {
  height: 400px;
  width: 90%;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 15px;
  margin-left:100px;
}
.com-chart {
  height: 100%;
  width: 100%;
}
.fixedtableHeight {
  margin-top: 25px;
  max-height: 500px;
  overflow: auto;
  width:90%;
  margin-left:100px;
}
.emotion-image {
  margin-top: 15px;
  text-align: center;
}
.emotion-image img {

    width:115%;
    height:115%;
    /*margin-right:100px;*/
    border-radius: 4px;
}
/*img {*/
/*    width:150%;*/
/*    height:150%;*/
/*    margin-top:25px;*/
/*    margin-left:20px;*/
/*    margin-right:50px;*/
/*  }*/
</style>
