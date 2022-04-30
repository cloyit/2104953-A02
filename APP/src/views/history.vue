<template>
  <div>
    <div class="nav">
      驾 驶 记 录
    </div>
    <!-- <div class="test">
      暂无驾驶记录!
    </div> -->
    <br>
    <div class="calendar">
      <p @click="previousweek" >上一周</p>
      <p @click="show = true" class="date">{{this.startday}}~{{this.endday}}</p>
      <p @click="nextweek">下一周</p>
    </div>
    <br>
    <van-calendar v-model="show"  @confirm="onConfirm" color='#007bffd5' :min-date="minDate" :max-date="maxDate"/>
    <div class="showcard">
      <span>
        <p v-if="this.weekHistory.length"><span style="font-size: 1.3em">{{weekHistory.length}}</span> 天</p>
        <p class="min">本周驾驶天数</p>
      </span>
      <span>
        <p v-if="this.weekHistory.length"> <span style="font-size: 1.3em">{{this.drivingtime}}</span> 次</p>
        <p class="min">本周驾驶次数</p>
      </span>
    </div>
    <div class="warn">
      本周系统已保障您的安全 <span style="font-size: 1.3em">{{this.safetime}}</span> 分钟，期间您闭眼 <span style="font-size: 1.3em">{{this.eyesum}}</span> 次，
      您注意力不集中 <span style="font-size: 1.3em">{{this.attentionsum}}</span> 次,您打哈欠<span style="font-size: 1.3em">{{this.yawnsum}}</span>次。
    </div>
    <br>
    <div>
      <div id="main" :style="{width: '100%', height: '300px'}"></div>
    </div>
    <div style="margin: 10px">
      <span @click="prepage">上一页</span>
      <span @click="nextpage" style="float: right">下一页</span>
    </div>
     <router-link  :to="{name: 'historydetail',params: {id:weekHistory[nowpage][0].id,obj: weekHistory[nowpage][0]}}" v-if="weekHistory.length!=0">
       <div class="history">
      <p style="font-size:14px">{{weekHistory[nowpage][0].begin}}~{{weekHistory[nowpage][0].end}}</p>
      <van-divider />
      <div class="itembox">
        <div style="margin-top: 11px">
          <van-icon name="logistics" size="30px"/>
        </div>
        <div class="item">
          <p style="display: inline; margin-left: 10px">车辆</p>
          <p style="display: inline; margin-left: 10px">  {{carinfo(weekHistory[nowpage][0].carId)}}</p>
        </div>
      </div>
      <van-divider :style="{ padding: '0  0 0 30px'}"/>
      <div class="itembox">
        <div style="margin-top: 11px">
          <van-icon name="closed-eye" size="30px"/>
        </div>
        <div class="item">
          <p style="display: inline; margin-left: 10px">闭眼</p>
          <p style="display: inline; margin-left: 10px">  {{weekHistory[nowpage][0].closeEye}}次</p>
        </div>
      </div>
      <van-divider :style="{ padding: '0  0 0 30px'}"/>
      <div class="itembox">
        <div style="margin-top: 11px">
          <van-icon name="bulb-o" size="30px"/>
        </div>
        <div class="item">
          <p style="display: inline; margin-left: 10px">打哈欠</p>
          <p style="display: inline; margin-left: 10px">  {{weekHistory[nowpage][0].yawn}}次</p>
        </div>
      </div>
      <van-divider :style="{ padding: '0  0 0 30px'}"/>
      <div class="itembox">
        <div style="margin-top: 11px">
          <van-icon name="warning-o" size="30px"/>
        </div>
        <div class="item">
          <p style="display: inline; margin-left: 10px">注意力不集中</p>
          <p style="display: inline; margin-left: 10px">  {{weekHistory[nowpage][0].attention}}次</p>
        </div>
      </div>
      <br>
      <!-- <van-divider :style="{ padding: '0  0 0 30px'}"/> -->
    </div>
      </router-link>
</div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import * as echarts from 'echarts'
export default {
  name: 'history',
  computed: {
    ...mapState(['weekHistory', 'monthHistory', 'token', 'cars']),
    ...mapGetters(['closeEye', 'attention', 'yawn'])
  },
  data () {
    return {
      startday: '',
      endday: '',
      show: false,
      minDate: new Date(2021, 0, 1),
      maxDate: new Date(),
      safetime: 0,
      eyesum: 0,
      yawnsum: 0,
      attentionsum: 0,
      drivingtime: 0,
      myChart: {},
      nowpage: 0
    }
  },
  created () {
    this.$nextTick(function () {
      this.drawLine()
    })
    var now = new Date(2022, 0, 21)
    this.getCurrentWeekFirstDay(now)
    this.getCurrentWeekLastDay(now)
  },
  methods: {
    drawLine () {
      var chartDom = document.getElementById('main')
      this.myChart = echarts.init(chartDom)
      var option

      option = {
        legend: {
          data: ['闭眼', '打哈欠', '注意力分散'],
          icon: 'rect'
        },
        xAxis: {
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {},
        series: [
          {
            name: '闭眼',
            type: 'bar',
            data: this.closeEye,
            itemStyle: {
              color: 'rgb(100, 204, 245)'
            }
          },
          {
            name: '打哈欠',
            type: 'bar',
            data: this.yawn,
            itemStyle: {
              color: 'rgb(244, 177, 131)'
            }
          },
          {
            name: '注意力分散',
            type: 'bar',
            data: this.attention,
            itemStyle: {
              color: '#38dfc8'
            }
          }
        ]
      }

      option && this.myChart.setOption(option)
    },
    onConfirm (date) {
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
    carinfo (id) {
      for (let i = 0; i < this.cars.length; i++) {
        if (this.cars[i].id === id) {
          return this.cars[i].type + ' ' + this.cars[i].carNumber
        }
      }
    },
    nextpage () {
      if (this.nowpage < this.weekHistory.length - 1) {
        this.nowpage++
      }
    },
    prepage () {
      if (this.nowpage > 0) {
        this.nowpage--
      }
    }
  },
  mounted () {
    if (this.token.length === 0) {
      this.$router.push('/login')
    }
  },
  watch: {
    startday () {
      this.$store.dispatch('getDrivingInformationByTime', { beginTimeS: this.startday + ' 00:00:00', endTimeS: this.endday + ' 00:00:00' })
    },
    closeEye () {
      this.$nextTick(function () {
        this.myChart.setOption({
          series: [
            {
              name: '闭眼',
              type: 'bar',
              data: this.closeEye,
              itemStyle: {
                color: 'rgb(100, 204, 245,0.8)'
              }
            },
            {
              name: '打哈欠',
              type: 'bar',
              data: this.yawn,
              itemStyle: {
                color: 'rgb(244, 177, 131,0.8)'
              }
            },
            {
              name: '注意力分散',
              type: 'bar',
              data: this.attention,
              itemStyle: {
                color: 'rgba(125, 255, 201, 0.8)'
              }
            }
          ]
        })
      })
    },
    attention () {
      this.safetime = 0
      this.eyesum = 0
      this.attentionsum = 0
      this.drivingtime = 0
      this.yawnsum = 0
      this.weekHistory.forEach((p) => {
        p.forEach((item) => {
          this.safetime += (new Date(item.end) - new Date(item.begin)) / 1000 / 60
          this.eyesum += item.closeEye
          this.attentionsum += item.attention
          this.yawnsum += item.yawn
          this.drivingtime++
        })
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
.calendar{
  display: flex;
  justify-content: space-between;
  margin: 0 10px;
  padding: 0 10px;
  background-color: rgb(237, 237, 237);
  border-radius: 20px;
  .date{
    line-height: 21px;
    font-size: 15px;
  }
}
.itembox{
  display: flex;
  height: 32px;
}
.history{
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));
}
.item{
  display: flex;
  width: 100%;
  justify-content: space-between;
}
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
.warn{
  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));
}
.showcard{
  display: flex;
  // background-color: rgb(32, 184, 239);
  background-image: linear-gradient(rgb(32, 184, 239), rgb(99, 196, 238));
  border-radius: 10px;
  font-size: 17px;
  margin: 0 10px;
  color: #fff;
  span{
    width: 50%;
    text-align: center;
  }
  .min{
    font-size: 13px;
  }
}
</style>
