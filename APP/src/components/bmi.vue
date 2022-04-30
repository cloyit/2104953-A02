<template>
  <div>
    <div class="nav">
      体 重
    </div>
  <div id="main" :style="{width: '100%', height: '300px'}"></div>

  <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));">
          <van-icon name="bar-chart-o" size="30px" color="#fff"/>
          <br>
          <div>
            <p>最高：</p> <p style="float: right">{{max}}Kg</p>
            <br>
            <p>最低：</p> <p style="float: right">{{min}}Kg</p>
            <br>
            <p>身体指数：</p> <p style="float: right">{{bmip}}</p>
            <br>
            <p>建议体重：</p> <p style="float: right">{{recommand}}Kg</p>
          </div>
  </div>
  <br>
  <div style="float: right" @click="showPopup"><van-button icon="plus" type="primary" round color="rgb(244, 177, 131)"/></div>
  <van-popup v-model="show" round>
    <div class="popup">
      <p>新增体重信息</p>
        <br>
        <van-field v-model="value" placeholder="请输入体重" />
        <br>
      <van-button round block type="info" native-type="submit" @click="onSubmit">提交</van-button>
    </div>
  </van-popup>
  <div style="height: 50px"></div>
</div>
</template>

<script>
import * as echarts from 'echarts'
import { mapState } from 'vuex'
import { Toast } from 'vant'
import { requploadBmi } from '@/api'
export default {
  name: 'bmi',
  created () {
    this.$store.dispatch('getAllBmi')
  },
  mounted () {
    this.$nextTick(() => {
      this.drawLine()
    })
  },
  data () {
    return {
      show: false,
      value: '',
      chart: {},
      max: 0,
      min: 1e9,
      bmip: 0,
      recommand: 0
    }
  },
  computed: {
    ...mapState(['bmi'])
  },
  methods: {
    showPopup () {
      this.show = true
    },
    drawLine () {
      var chartDom = document.getElementById('main')
      this.chart = echarts.init(chartDom)
      var option

      var date = ['2022-01-17', '2022-01-18', '2022-01-21', '2022-01-23', '2022-01-25', '2022-01-30', '2022-02-02']
      var data = [80.0, 80.2, 79.8, 79.5, 79.0, 79.1, 78.9]
      option = {
        title: {
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: date,
          axisPointer: {
            show: true,
            label: {
              show: true
            }
          }
        },
        yAxis: {
          name: 'Kg',
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '体重',
            type: 'line',
            symbol: 'none',
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
            data: data
          }
        ]
      }

      option && this.chart.setOption(option)
    },
    onSubmit () {
      var date = new Date()
      var nowmonth = Number(date.getMonth()) + 1
      if (nowmonth < 10) {
        nowmonth = '0' + nowmonth
      }
      var nowday = Number(date.getDate())
      if (nowday < 10) {
        nowday = '0' + nowday
      }
      var nowdate = date.getFullYear() + '-' + nowmonth + '-' + nowday + 'T00:00:00'
      if (!isNaN(this.value)) {
        requploadBmi({ weight: this.value, time: nowdate, height: 182 })
        Toast('提交成功')
      } else {
        Toast('请输入正确的体重信息')
      }
      this.show = false
      this.value = ''
      setTimeout(() => {
        this.$store.dispatch('getAllBmi')
      }, 1000)
    }
  },
  watch: {
    bmi () {
      var date = []
      var data = []
      this.bmi.forEach(item => {
        date.push(item.time)
        data.push(item.weight)
        this.max = Math.max(this.max, item.weight)
        this.min = Math.min(this.min, item.weight)
      })
      this.bmip = (this.bmi[this.bmi.length - 1].weight / this.bmi[this.bmi.length - 1].height / this.bmi[this.bmi.length - 1].height * 10000).toFixed(2)
      this.recommand = (this.bmi[this.bmi.length - 1].height * this.bmi[this.bmi.length - 1].height * 23 / 10000).toFixed(2)
      this.chart.setOption({
        xAxis: {

          data: date
        },
        series: [
          {
            name: '体重',
            data: data
          }
        ]
      })
    }
  }
}
</script>
<style lang="less" scoped>
.popup{
  width: 200px;
  height: 200px;
  margin: 10px 20px;
  padding: 10px;
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
