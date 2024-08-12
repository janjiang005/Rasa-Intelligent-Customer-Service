<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="card">
          <span class="card-title">选择省份/直辖市:</span><br/>
          <el-select v-model="selectedProvince" placeholder="请选择城市" @change="fetchQuestions" style="margin-top:20px">
            <el-option v-for="province in provinces" :key="province" :label="province" :value="province"></el-option>
          </el-select>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card">
          <span class="card-title">选择用户类型:</span><br/><br/>
          <el-radio-group v-model="userType" @change="fetchQuestions">
            <el-radio v-for="type in userTypes" :key="type" :label="type">{{type}}</el-radio>
          </el-radio-group>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="chart">
          <div class="com-chart" ref="seller_ref"></div>
        </div>
      </el-col>
      <el-col :span="16">
        <div id="main-map" class="map-container"></div>
      </el-col>
    </el-row>
    <el-table
      class="fixedtableHeight"
      v-loading="listLoading"
      :data="showList"
      :header-cell-style="{ background: '#9AC5E5', color: '#fff' }"
      stripe
      tooltip-effect="dark"
      style="width: 100%; margin-top: 5%; background: white;"
    >
      <el-table-column prop="order_id" label="订单编号" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.order_id }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="order_type" label="快递类型" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.order_type }}</span>
        </template>
      </el-table-column>
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
    </el-table>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import worldMap from '@/assets/map/china.json';

export default {
  data() {
    return {
      listLoading: false,
      showList: [],
      provinces: [],
      selectedProvince: '',
      userType: '',
      userTypes: [],
      provinceData: [],
      mapData: [],
      chartInstance: null,
      allData: null,
      currentPage: 1,
      totalPage: 0,
      timerId: null,
    };
  },

  watch: {
    theme() {
      if (this.chartInstance) {
        this.chartInstance.dispose();
        this.initChart();
        this.screenAdapter();
        this.updateChart();
      }
    }
  },
  created() {
    this.fetchInitialData();
  },
  mounted() {
    this.initMap();
    this.fetchMapData();
    this.fetchProvinceData();
    this.initChart();
    window.addEventListener("resize", this.screenAdapter);
  },
  beforeDestroy() {
    clearInterval(this.timerId);
    window.removeEventListener('resize', this.screenAdapter);
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
  },
  methods: {
    async fetchInitialData() {
      this.listLoading = true;
      try {
        const response = await fetch('http://localhost:5001/questionlist/initialData');
        const data = await response.json();
        if (data && data.provinces && data.userTypes) {
          this.provinces = data.provinces;
          this.userTypes = data.userTypes;
        }
      } catch (error) {
        console.error('Error fetching initial data:', error);
      } finally {
        this.listLoading = false;
      }
    },
    async fetchQuestions() {
      if (this.selectedProvince && this.userType) {
        this.listLoading = true;
        try {
          const response = await fetch(`http://localhost:5001/questionlist/questions?province=${this.selectedProvince}&userType=${this.userType}`);
          const data = await response.json();
          if (data && data.questions) {
            this.showList = data.questions;
          }
        } catch (error) {
          console.error('Error fetching questions:', error);
        } finally {
          this.listLoading = false;
        }
      }
    },
    async fetchMapData() {
      try {
        const response = await fetch('http://localhost:5001/questionlist/mapData');
        const data = await response.json();
        if (data && Array.isArray(data)) {
          this.mapData = data.map(item => ({ name: item.province, value: item.count }));
          this.updateMap();
        }
      } catch (error) {
        console.error('Error fetching map data:', error);
      }
    },
    async fetchProvinceData() {
      try {
        const response = await fetch('http://localhost:5001/questionlist/provinceData');
        const data = await response.json();
        if (data && Array.isArray(data)) {
          this.provinceData = data;
          this.allData = this.provinceData;

          this.totalPage = Math.ceil(this.allData.length / 10); // 每页显示10行
          this.updateChart();
          this.startInterval();
        }
      } catch (error) {
        console.error('Error fetching province data:', error);
      }
    },
    // initMap() {
    //   echarts.registerMap('world', worldMap);
    //   this.map = echarts.init(document.getElementById('main-map'));
    //   this.map.setOption({
    //     tooltip: {
    //       trigger: 'item',
    //       formatter: '{b}: {c}',
    //     },
    //     visualMap: {
    //       min: 0,
    //       max: 5000,
    //       left: 'left',
    //       top: 'bottom',
    //       text: ['高', '低'],
    //       inRange: {
    //         color: ['#B0D6F5', '#65C2F5', '#0463CA'],
    //       },
    //       calculable: true,
    //     },
    //     series: [
    //       {
    //         name: '数据',
    //         type: 'map',
    //         mapType: 'world',
    //         roam: true,
    //         itemStyle: {
    //           emphasis: { label: { show: true } },
    //         },
    //         data: this.mapData,
    //       },
    //     ],
    //   });
    // },
    initMap() {
  echarts.registerMap('world', worldMap);
  this.map = echarts.init(document.getElementById('main-map'));
  this.map.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}',
    },
    visualMap: {
      min: 0,
      max: 5000,
      left: 'left',
      top: 'bottom',
      text: ['高', '低'],
      inRange: {
        color: ['#B0D6F5', '#65C2F5', '#0463CA'],
      },
      calculable: true,
    },
    series: [
      {
        name: '数据',
        type: 'map',
        mapType: 'world',
        roam: true,
        itemStyle: {
          emphasis: { label: { show: true } },
        },
        data: this.mapData,
      },
    ],
  });

  this.map.on('click', (params) => {
    if (params.data && params.data.value > 0) {
      this.$router.push({ name: 'ProvinceDetails', params: { province: params.name } });
    }
  });
},
    updateMap() {
      const option = this.map.getOption();
      option.series[0].data = this.mapData;
      this.map.setOption(option);
    },
    initChart() {
      this.chartInstance = echarts.init(this.$refs.seller_ref, this.theme);
      const initOption = {
        title: {
          text: "▎省份收件/寄件问题统计",
          left: 20,
          top: 20,
        },
        grid: {
          top: '20%',
          left: '3%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'line',
            z: 0,
            lineStyle: {
              color: "#2D3443"
            }
          }
        },
        legend: {
          data: ['收件', '寄件'],
          top: 40
        },
        series: [
          {
            name: '收件',
            type: 'bar',
            label: {
              show: true,
              position: 'right',
              textStyle: {
                color: '#fff'
              }
            },
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#62be9d' },
                { offset: 1, color: '#a4e2cb' }
              ])
            }
          },
          {
            name: '寄件',
            type: 'bar',
            label: {
              show: true,
              position: 'right',
              textStyle: {
                color: '#fff'
              }
            },
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#f0c800' },
                { offset: 1, color: '#e3e276' }
              ])
            }
          }
        ]
      };
      this.chartInstance.setOption(initOption);
      this.chartInstance.on('mouseover', () => clearInterval(this.timerId));
      this.chartInstance.on("mouseout", this.startInterval);
    },
    updateChart() {
      const start = (this.currentPage - 1) * 10;
      const end = this.currentPage * 10;
      const data = this.allData.slice(start, end);
      const names = data.map(item => item.name);
      const receivedData = data.map(item => item.received);
      const sentData = data.map(item => item.sent);

      const options = this.chartInstance.getOption();
      options.yAxis[0].data = names;
      options.series[0].data = receivedData;
      options.series[1].data = sentData;
      this.chartInstance.setOption(options);
    },
    screenAdapter() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },
    startInterval() {
      this.timerId = setInterval(() => {
        this.currentPage++;
        if (this.currentPage > this.totalPage) {
          this.currentPage = 1;
        }
        this.updateChart();
      }, 3000);
    },
  },
};
</script>

<style scoped>

  @font-face {
  font-family: 'MyCustomFont2';
  src: url('../assets/font/HarmonyOS_Sans_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}


.dashboard-container {
  font-family: 'MyCustomFont2';
  font-size: 18px;
  font-weight: bold;
  background: #f0f2f5;
  padding: 20px;
}
.card {
  padding: 10px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height:100px;
}
.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
.map-container {
  height: 400px;
  width: 100%;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top:20px;
}
.chart {
  height: 400px;
  width: 100%;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.com-chart {
  height: 100%;
  width: 100%;
  margin-top:20px;
}
.fixedtableHeight {
  margin-top:20px;
  max-height: 500px;
  overflow: auto;
}
</style>
