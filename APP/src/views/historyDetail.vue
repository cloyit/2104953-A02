<template>
  <div>
    <div class="nav">
      驾 驶 记 录 详 情
    </div>

    <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));">
      <van-icon name="underway" size="30px" color="#fff"/>
      <br>
      <div>
        <p>驾驶时长：</p> <p style="float: right"> {{this.drivingtime}}分钟</p>
        <van-divider/>
        <br>
        <p>眨眼次数：</p> <p style="float: right">{{this.$route.params.obj.closeEye}}次</p>
        <br>
        <p style="float: right">{{this.$route.params.obj.attention}}次</p>
        <p>注意力不集中次数：</p>
        <br>
        <p style="float: right">{{this.$route.params.obj.yawn}}次</p>
        <p>打哈欠次数：</p>
        <br>
        <p style="float: right">{{this.$route.params.obj.startLatitude}}44 N {{this.$route.params.obj.startLongitude}}30 E</p>
        <p>起始位置：</p>
        <br>
        <p style="float: right">{{this.$route.params.obj.endLatitude}}51 N {{this.$route.params.obj.endLongitude}}58 E</p>
        <p>结束位置：</p>
      </div>
    </div>

    <div id="main" :style="{width: 'auto', height: '300px'}" ></div>
    <div id="bloodOxygen" :style="{width: '95%', height: '300px', margin: '0 0 0 5%'}"></div>
    <div id="heartbeat" :style="{width: '95%', height: '300px', margin: '0 0 0 5%'}"></div>
    <div id="temperature" :style="{width: '95%', height: '300px', margin: '0 0 0 5%'}"></div>
    <p class="bottomtext">数据来源：可穿戴设备1,编号：7VAX84AC513</p>
    <div style="height: 50px"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { mapState } from 'vuex'
export default {
  name: 'historydetail',
  data () {
    return {
      drivingtime: 0,
      bloodchart: {},
      heartbeatchart: {},
      temperaturechart: {}
    }
  },
  computed: {
    ...mapState(['dayHealth'])
  },
  created () {
    this.$store.dispatch('getDayHealth', { beginTimeS: this.$route.params.obj.begin, endTimeS: this.$route.params.obj.end })
    this.$nextTick(function () {
      this.drawLine()
      this.blooddrawLine()
      this.heartbeatdrawLine()
      this.temperaturedrawLine()
    })
    var begin = new Date(this.$route.params.obj.begin)
    var end = new Date(this.$route.params.obj.end)
    this.drivingtime = (end - begin) / 1000 / 60
  },
  methods: {
    drawLine () {
      var chartDom = document.getElementById('main')
      var myChart = echarts.init(chartDom)
      var option

      option = {
        legend: {
          orient: 'vertical',
          x: 'left',
          data: ['眨眼', '注意力分散', '打哈欠']
        },
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center',
              emphasis: {
                show: true
              },
              normal: {
                show: true,
                formatter: '{d}%',
                position: 'inner'
              }
            },
            labelLine: {
              show: false
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '30',
                fontWeight: 'bold'
              }
            },
            data: [
              {
                value: this.$route.params.obj.closeEye,
                name: '眨眼'
              },
              {
                value: this.$route.params.obj.attention,
                name: '注意力分散'
              },
              {
                value: this.$route.params.obj.yawn,
                name: '打哈欠'
              }
            ]
          }
        ]
      }

      option && myChart.setOption(option)
    },
    blooddrawLine () {
      var chartDom = document.getElementById('bloodOxygen')
      this.bloodchart = echarts.init(chartDom)
      var option

      option = {
        title: {
          text: '血氧'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [],
          axisPointer: {
            show: true,
            label: {
              show: true
            }
          }
        },
        yAxis: {
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '血氧',
            type: 'line',
            symbol: 'none',
            areaStyle: {
              color: 'rgb(255, 188, 194)'
            },
            lineStyle: {
              color: 'rgb(255, 188, 194)'
            },
            itemStyle: {
              normal: { label: { show: true } }
            },
            axisTick: {
              show: true,
              interval: 0,
              lineStyle: {

              }
            },
            // label: {
            //   show: true,
            //   position: 'bottom',
            //   textStyle: {
            //     fontSize: 1
            //   }
            // },
            data: []
          }
        ]
      }

      option && this.bloodchart.setOption(option)
    },
    heartbeatdrawLine () {
      var chartDom = document.getElementById('heartbeat')
      this.heartbeatchart = echarts.init(chartDom)
      var option

      option = {
        title: {
          text: '心率'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [],
          axisPointer: {
            show: true,
            label: {
              show: true
            }
          }
        },
        yAxis: {
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '心率',
            type: 'line',
            symbol: 'none',
            areaStyle: {
              color: 'rgb(244, 177, 131)'
            },
            lineStyle: {
              color: 'rgb(244, 177, 131)'
            },
            itemStyle: {
              normal: { label: { show: true } }
            },
            axisTick: {
              show: true,
              interval: 0,
              lineStyle: {

              }
            },
            // label: {
            //   show: true,
            //   position: 'bottom',
            //   textStyle: {
            //     fontSize: 1
            //   }
            // },
            data: []
          }
        ]
      }

      option && this.heartbeatchart.setOption(option)
    },
    temperaturedrawLine () {
      var chartDom = document.getElementById('temperature')
      this.temperaturechart = echarts.init(chartDom)
      var option

      option = {
        title: {
          text: '体温'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [],
          axisPointer: {
            show: true,
            label: {
              show: true
            }
          }
        },
        yAxis: {
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '体温',
            type: 'line',
            symbol: 'none',
            areaStyle: {
              color: 'rgb(115, 192, 222)'
            },
            lineStyle: {
              color: 'rgb(115, 192, 222)'
            },
            itemStyle: {
              normal: { label: { show: true } }
            },
            axisTick: {
              show: true,
              interval: 0,
              lineStyle: {

              }
            },
            // label: {
            //   show: true,
            //   position: 'bottom',
            //   textStyle: {
            //     fontSize: 1
            //   }
            // },
            data: []
          }
        ]
      }

      option && this.temperaturechart.setOption(option)
    }
  },
  watch: {
    dayHealth () {
      var date = []
      var data1 = []
      var data2 = []
      var data3 = []
      if (this.dayHealth[0]) {
        this.dayHealth[0].forEach((item) => {
          date.push(item.time)
          data1.push(item.bloodOxygen)
          data2.push(item.temperature)
          data3.push(item.heartbeat)
        })
      }
      this.bloodchart.setOption({
        xAxis: {
          data: date
        },
        series: [
          { data: data1 }
        ]
      })
      this.temperaturechart.setOption({
        xAxis: {
          data: date
        },
        series: [
          { data: data2 }
        ]
      })
      this.heartbeatchart.setOption({
        xAxis: {
          data: date
        },
        series: [
          { data: data3 }
        ]
      })
    }
  }

}
</script>

<style lang="less" scoped>
.nav{
  height: 46px;
  background-color: #007bffd5;
  text-align: center;
  line-height: 46px;
  color: #fff;
}
.bottomtext{
  float: right;
  font-size: 13px;
  color: rgb(224,224,224);
}
.card{
       border-radius: 10px;
       padding: 10px;
       margin: 10px;
       img{
         display: inline-block;
         width: 60px;
       }
       div{
         display: inline-block;
         width: 100%;
         p{
           display: inline-block;
           font-size: 15px;
           color: #fff;
         }
       }
}
</style>
