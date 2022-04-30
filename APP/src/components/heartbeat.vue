<template>
  <div>
    <div class="nav">
      心 跳
    </div>
  <van-tabs v-model="active">
    <van-tab title="日 ">
      <div class="calendar">
      <p @click="previousday">前一天</p>
      <p @click="show = true" class="date">{{this.nowdate}}</p>
      <p @click="nextday">后一天</p>
    </div>
    <van-calendar v-model="show"  @confirm="onConfirmday" color='#007bffd5' :min-date="minDate" :max-date="maxDate"/>
      <div id="main" :style="{width: '95%', height: '300px', margin: '0 0 0 5%' }"></div>
      <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));">
          <van-icon name="bar-chart-o" size="30px" color="#fff"/>
          <br>
          <div class="box">
            <div class="text">
              <p>本次最高：</p>
              <p style="float:right">{{maxnumber}} 次/分</p>
            </div>

            <br>
            <!-- <p style="float: right">{{minnumber}}%</p> -->
            <div class="text">
              <p>本次最低：</p>
              <p style="float:right">{{minnumber}} 次/分</p>
            </div>
          </div>
    </div>
    </van-tab>
    <van-tab title="周">
      <div class="calendar">
      <p @click="previousweek">上一周</p>
      <p @click="show = true" class="date">{{this.startday}}~{{this.endday}}</p>
      <p @click="nextweek">下一周</p>
    </div>

    <van-calendar v-model="show"  @confirm="onConfirmweek" color='#007bffd5' :min-date="minDate" :max-date="maxDate"/>
    <div id="week" :style="{width: '95%', height: '300px', margin: '0 0 0 5%' }"></div>
    <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));">
          <van-icon name="bar-chart-o" size="30px" color="#fff"/>
          <br>
          <div class="box">
            <div class="text">
              <p>本次最高：</p>
              <p style="float:right">{{maxnumber}} 次/分</p>
            </div>
            <br>
            <!-- <p style="float: right">{{minnumber}}%</p> -->
            <div class="text">
              <p>本次最低：</p>
              <p style="float:right">{{minnumber}} 次/分</p>
            </div>
          </div>
    </div>
    </van-tab>
    <van-tab title="月">
      <div class="calendar">
        <p @click="previousmonth">上一月</p>
        <p class="date">{{this.nowmonth}}</p>
        <p @click="nextmonth">下一月</p>
      </div>
    <div id="month" :style="{width: '95%', height: '300px', margin: '0 0 0 5%' }"></div>
    </van-tab>
  </van-tabs>

</div>
</template>

<script>
import * as echarts from 'echarts'
import { mapState, mapGetters } from 'vuex'
export default {
  name: 'heartbeat',
  created () {
    this.$nextTick(function () {
      this.drawLine()
      this.maxnum()
    })
    var now = new Date(2022, 0, 21)
    this.getCurrenDay(now)
    this.$store.dispatch('getDayHealth', { beginTimeS: this.nowdate + ' 00:00:00', endTimeS: this.nowdate + ' 23:59:59' })
  },
  data () {
    return {
      maxnumber: 0,
      minnumber: 1e9,
      active: 0,
      show: false,
      minDate: new Date(2021, 0, 1),
      maxDate: new Date(),
      nowdate: '',
      startday: '',
      endday: '',
      chart: '',
      nowmonth: ''
    }
  },
  computed: {
    ...mapGetters(['heartbeat']),
    ...mapState(['lastHistory', 'dayHealth', 'weekHealth', 'monthHealth'])
  },
  methods: {
    drawLine () {
      if (this.chart !== null && this.chart !== '' && this.chart !== undefined) this.chart.dispose()
      var chartDom = document.getElementById('main')
      this.chart = echarts.init(chartDom)
      var option

      var date = []
      var data = []
      option = {
        grid: {
          left: '1%',
          containLabel: true
        },
        title: {
          // text: this.lastHistory.drivingInformation.end.substring(0, 10)
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
          name: '下/分',
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '心跳',
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
            data: data
          }
        ]
      }

      option && this.chart.setOption(option)
    },
    weekdrawLine () {
      if (this.chart !== null && this.chart !== '' && this.chart !== undefined) this.chart.dispose()
      var weekchartDom = document.getElementById('week')
      this.chart = echarts.init(weekchartDom)
      var option

      var date = []
      var data = []
      option = {
        grid: {
          left: '1%',
          containLabel: true
        },
        legend: {
          icon: 'rect'
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
          name: '下/分',
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '平均值',
            type: 'line',
            symbol: 'none',
            // areaStyle: {
            //   color: 'rgb(255, 188, 194)'
            // },
            lineStyle: {
              color: 'rgb(255, 188, 194)'
            },
            itemStyle: {
              normal: {
                label: { show: true },
                color: 'rgb(255, 188, 194)'
              }
            },
            axisTick: {
              show: true,
              interval: 0,
              lineStyle: {

              }
            },
            data: data
          },
          {
            name: '最大值',
            type: 'line',
            symbol: 'none',
            // areaStyle: {
            //   color: 'rgb(255, 188, 194)'
            // },
            lineStyle: {
              color: 'rgb(244, 177, 131)'
            },
            itemStyle: {
              normal: {
                label: { show: true },
                color: 'rgb(244, 177, 131)'
              }
            },
            axisTick: {
              show: true,
              interval: 0,
              lineStyle: {

              }
            },
            data: data
          },
          {
            name: '最小值',
            type: 'line',
            symbol: 'none',
            // areaStyle: {
            //   color: 'rgb(255, 188, 194)'
            // },
            lineStyle: {
              color: '#38dfc8'
            },
            itemStyle: {
              normal: {
                label: { show: true },
                color: '#38dfc8'
              }
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
    monthdrawLine () {
      if (this.chart !== null && this.chart !== '' && this.chart !== undefined) this.chart.dispose()
      var monthchartDom = document.getElementById('month')
      this.chart = echarts.init(monthchartDom)
      var option

      var date = []
      var data = []
      option = {
        grid: {
          left: '1%',
          containLabel: true
        },
        title: {
          // text: this.lastHistory.drivingInformation.end.substring(0, 10)
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
          name: '下/分',
          boundaryGap: [0, '50%'],
          type: 'value',
          scale: true
        },
        series: [
          {
            name: '心跳',
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
            data: data
          }
        ]
      }

      option && this.chart.setOption(option)
    },
    maxnum () {
      this.heartbeat.forEach(item => {
        this.maxnumber = Math.max(this.maxnumber, item)
        this.minnumber = Math.min(this.minnumber, item)
      })
    },
    nextday () {
      var nextday = new Date(this.nowdate)
      nextday = nextday.setDate(nextday.getDate() + 1)
      nextday = new Date(nextday)
      this.getCurrenDay(nextday)
    },
    previousday () {
      var nextday = new Date(this.nowdate)
      nextday = nextday.setDate(nextday.getDate() - 1)
      nextday = new Date(nextday)
      this.getCurrenDay(nextday)
    },
    getCurrenDay (date) {
      var nowmonth = Number(date.getMonth()) + 1
      if (nowmonth < 10) {
        nowmonth = '0' + nowmonth
      }
      var nowday = Number(date.getDate())
      if (nowday < 10) {
        nowday = '0' + nowday
      }
      this.nowdate = date.getFullYear() + '-' + nowmonth + '-' + nowday
    },
    getCurrenMonth (date) {
      var nowmon = Number(date.getMonth()) + 1
      if (nowmon < 10) {
        nowmon = '0' + nowmon
      }
      this.nowmonth = date.getFullYear() + '-' + nowmon
    },
    onConfirmday (date) {
      this.show = false
      this.getCurrenDay(date)
    },
    onConfirmweek (date) {
      this.show = false
      this.getCurrentWeekLastDay(date)
      this.getCurrentWeekFirstDay(date)
    },
    getCurrentWeekFirstDay (date) {
      const weekFirstDay = new Date(date - (date.getDay() - 1) * 86400000)
      let firstMonth = Number(weekFirstDay.getMonth()) + 1
      if (firstMonth < 10) {
        firstMonth = '0' + firstMonth
      }
      let weekFirstDays = weekFirstDay.getDate()
      if (weekFirstDays < 10) {
        weekFirstDays = '0' + weekFirstDays
      }
      this.startday = weekFirstDay.getFullYear() + '-' + firstMonth + '-' + weekFirstDays
    },
    getCurrentWeekLastDay (date) {
      const weekFirstDay = new Date(date - (date.getDay() - 1) * 86400000)
      const weekLastDay = new Date((weekFirstDay / 1000 + 6 * 86400) * 1000)
      let lastMonth = Number(weekLastDay.getMonth()) + 1
      if (lastMonth < 10) {
        lastMonth = '0' + lastMonth
      }
      let weekLastDays = weekLastDay.getDate()
      if (weekLastDays < 10) {
        weekLastDays = '0' + weekLastDays
      }
      this.endday = weekFirstDay.getFullYear() + '-' + lastMonth + '-' + weekLastDays
    },
    nextweek () {
      var nextweek = new Date(this.startday)
      nextweek = nextweek.setDate(nextweek.getDate() + 7)
      nextweek = new Date(nextweek)
      this.getCurrentWeekFirstDay(nextweek)
      this.getCurrentWeekLastDay(nextweek)
    },
    previousweek () {
      var nextweek = new Date(this.startday)
      nextweek = nextweek.setDate(nextweek.getDate() - 7)
      nextweek = new Date(nextweek)
      this.getCurrentWeekFirstDay(nextweek)
      this.getCurrentWeekLastDay(nextweek)
    },
    nextmonth () {
      var arr = this.nowmonth.split('-')
      if (Number(arr[1]) < 9) {
        arr[1] = Number(arr[1]) + 1
        arr[1] = '0' + arr[1] + ''
      } else if (arr[1] === '12' || arr[1] === 12) {
        arr[1] = '01'
        arr[0] = Number(arr[0]) + 1
      } else {
        arr[1] = Number(arr[1]) + 1
      }
      this.nowmonth = arr.join('-')
    },
    previousmonth () {
      var arr = this.nowmonth.split('-')
      if (arr[1] === '01') {
        arr[1] = '12'
        arr[0] = Number(arr[0]) - 1
      } else if (Number(arr[1]) < 11) {
        arr[1] = Number(arr[1]) - 1
        arr[1] = '0' + arr[1] + ''
      } else {
        arr[1] = Number(arr[1]) - 1
      }
      this.nowmonth = arr.join('-')
    }
  },
  watch: {
    dayHealth () {
      var date = []
      var data = []
      if (this.dayHealth[0]) {
        this.dayHealth[0].forEach((item) => {
          date.push(item.time)
          data.push(item.heartbeat)
        })
      }
      this.chart.setOption({
        xAxis: {
          data: date
        },
        series: [
          { data: data }
        ]
      })
    },
    nowdate () {
      if (this.nowdate !== '') {
        this.$store.dispatch('getDayHealth', { beginTimeS: this.nowdate + ' 00:00:00', endTimeS: this.nowdate + ' 23:59:59' })
      }
    },
    active (val) {
      if (val === 1) {
        if (this.startday !== '') {
          this.$store.dispatch('getWeekHealth', { beginTimeS: this.startday + ' 00:00:00', endTimeS: this.endday + ' 23:59:59' })
        }
        this.$nextTick(function () {
          this.weekdrawLine()
          this.maxnum()
          var now = new Date(2022, 0, 21)
          this.getCurrentWeekFirstDay(now)
          this.getCurrentWeekLastDay(now)
        })
      } else if (val === 0) {
        this.$store.dispatch('getDayHealth', { beginTimeS: this.nowdate + ' 00:00:00', endTimeS: this.nowdate + ' 23:59:59' })
        this.$nextTick(function () {
          this.drawLine()
          this.maxnum()
        })
      } else if (val === 2) {
        this.getCurrenMonth(new Date(2022, 0))
        this.$nextTick(function () {
          this.monthdrawLine()
        })
      }
    },
    startday () {
      if (this.startday !== '') {
        this.$store.dispatch('getWeekHealth', { beginTimeS: this.startday + ' 00:00:00', endTimeS: this.endday + ' 23:59:59' })
      }
    },
    nowmonth () {
      if (this.nowmonth !== '') {
        this.$store.dispatch('getMonthHealth', { beginTimeS: this.nowmonth + '-01 00:00:00', endTimeS: this.nowmonth + '-31 23:59:59' })
      }
    },
    weekHealth () {
      var date = []
      var avgdata = []
      var maxdata = []
      var mindata = []
      this.weekHealth.forEach((p) => {
        date.push(p.time)
        avgdata.push(p.avgheartbeat)
        maxdata.push(p.maxheartbeat)
        mindata.push(p.minheartbeat)
      })
      this.chart.setOption({
        xAxis: {
          data: date
        },
        series: [
          {
            nmae: 'avg',
            data: avgdata
          },
          {
            nmae: 'max',
            data: maxdata
          },
          {
            nmae: 'min',
            data: mindata
          }
        ]
      })
    },
    monthHealth () {
      var date = []
      var data = []
      this.monthHealth.forEach((p) => {
        date.push(p.time)
        data.push(p.avgheartbeat)
      })
      this.chart.setOption({
        xAxis: {
          data: date
        },
        series: [
          { data: data }
        ]
      })
    }
  }
}
</script>

<style lang="less" scoped>
.title{
  text-align: center;
  height: 40px;
  line-height: 40px;
  background-image: linear-gradient(rgb(32, 184, 239), rgb(99, 196, 238));
  border-radius: 10px;
  margin: 0 10px;
  padding: 0 10px;
  color: #fff;
}
.box{
  width: 100%;
}
.text{
    div p{
      display: inline-block;
    }
  }
.card{
       border-radius: 10px;
       height: 120px;
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
.calendar{
  display: flex;
  justify-content: space-between;
  margin: 0 10px;
  .date{
    font-size: 15px;
  }
}
</style>
