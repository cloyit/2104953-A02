<template>
  <div class="bbc">
    <div class="nav">
      健 康 数 据
    </div>
    <div class="box" @click="goBlood">
      <!-- <p>血氧</p> -->
      <div class="img"><img src="http://47.102.99.215/group1/M00/00/02/rBgbJ2JVGOOAdeGrAAAkvKorQLY.45.jpg" alt=''/></div>
      <div class="img" v-if="bloodOxygen.length !== 0">
        <p>血氧 ： <span style="font-size: 1.3em">{{a_bloodOxygen}}</span> %</p>
        <p style="font-size:13px;color:rgb(107, 110, 112);">时间:{{health[0][0].time}}</p>
      </div>
      <div class="button">
        <van-button  hairline round  type="danger" size="mini"  v-if="a_bloodOxygen<70">较低</van-button>
        <van-button  hairline round  type="warning" size="mini" v-if="a_bloodOxygen<90&&a_bloodOxygen>=70">偏低</van-button>
        <van-button  hairline round  type="primary" size="mini" v-if="a_bloodOxygen<=99&&a_bloodOxygen>=90">正常</van-button>
      </div>
    </div>
    <div class="box" @click="goTemperature">
      <div class="img"><img src="http://47.102.99.215/group1/M00/00/02/rBgbJ2JVGMKAO5XLAAAx-ENN3PE.43.jpg" alt=''/></div>
      <div class="img" v-if="bloodOxygen.length !== 0">
        <p>体温 ： <span style="font-size: 1.3em">{{a_temperature}}</span>℃</p>
        <p style="font-size:13px;color:rgb(107, 110, 112);">时间:{{health[0][0].time}}</p>
      </div>
      <div class="button">
        <van-button  hairline round  type="danger" size="mini"  v-if="a_temperature>37.5">较高</van-button>
        <van-button  hairline round  type="warning" size="mini" v-if="a_temperature<35.7">较低</van-button>
        <van-button  hairline round  type="primary" size="mini" v-if="a_temperature<=37.5&&a_temperature>=35.7">正常</van-button>
      </div>
      </div>
    <div class="box" @click="goHeartbeat">
      <div class="img" ><img src="http://47.102.99.215/group1/M00/00/02/rBgbJ2JVGPCARMncAAAin8vy-jY.46.jpg" alt=''/></div>
      <div class="img" v-if="bloodOxygen.length !== 0">
        <p>心率 ： <span style="font-size: 1.3em">{{a_heartbeat}}</span> 次/分</p>
        <p style="font-size:13px;color:rgb(107, 110, 112);">时间:{{health[0][0].time}}</p>
      </div>
      <div class="button">
        <van-button  hairline round  type="danger" size="mini"  v-if="a_heartbeat>100">较高</van-button>
        <van-button  hairline round  type="warning" size="mini" v-if="a_heartbeat<60">较低</van-button>
        <van-button  hairline round  type="primary" size="mini" v-if="a_heartbeat<=100&&a_heartbeat>=60">正常</van-button>
      </div>
      </div>
    <div class="box" @click="goBmi">
      <div class="img"><img src="http://47.102.99.215/group1/M00/00/02/rBgbJ2JVGNaAP8bgAAAfc9X61Xk.44.jpg" alt=''/></div>
      <div class="img" v-if="bloodOxygen.length !== 0">
        <p>体重 ： <span style="font-size: 1.3em">80.3</span> Kg</p>
        <p style="font-size:13px;color:rgb(107, 110, 112);">时间:{{health[0][0].time}}</p>
      </div>
      <div class="button">
        <van-button  hairline round  type="danger" size="mini" v-if="0">危险</van-button>
        <van-button  hairline round  type="primary" size="mini" v-if="1">正常</van-button>
      </div>
    </div>
    <div class="report" @click="goreport">点击生成健康报表</div>
    </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
export default {
  name: 'Home',
  computed: {
    ...mapState(['health', 'token']),
    ...mapGetters(['heartbeat', 'temperature', 'bloodOxygen'])
  },
  data () {
    return {
      selected: 1,
      a_heartbeat: 0,
      a_temperature: 0,
      a_bloodOxygen: 0
    }
  },
  mounted () {
    this.heartbeat.forEach(item => {
      this.a_heartbeat += Number(item)
    })
    this.temperature.forEach(item => {
      this.a_temperature += Number(item)
    })
    this.bloodOxygen.forEach(item => {
      this.a_bloodOxygen += Number(item)
    })
    this.a_heartbeat = Number((this.a_heartbeat / this.bloodOxygen.length).toFixed(0))
    this.a_temperature = Number((this.a_temperature / this.bloodOxygen.length).toFixed(1))
    this.a_bloodOxygen = Number((this.a_bloodOxygen / this.bloodOxygen.length).toFixed(2))
  },
  methods: {
    goreport () {
      this.$router.push('/health/healthReport')
    },
    goBmi () {
      this.$router.push('/health/bmi')
    },
    goBlood () {
      this.$router.push('/health/bloodoxygen')
    },
    goHeartbeat () {
      this.$router.push('/health/heartbeat')
    },
    goTemperature () {
      this.$router.push('/health/temperature')
    }
  }
}
</script>

<style lang="less" scoped>
img{
  height: 100px;
  width: 320px;
}
.report{
  margin: 10px 60px;
  padding: 10px 30px;
  border-radius: 10px;
  text-align: center;
  background-color: rgb(244, 177, 131);
  color: #fff;
}
.nav{
  height: 46px;
  background-color: #007bffd5;
  text-align: center;
  line-height: 46px;
  color: #fff;
}
.chart{
  display: flex;
  height: 30px;
  justify-content: space-around;
}
.box{
  height: 90px;
  background-color: #fff;
  border: 1px   #fff solid;
  border-radius: 20px;
  margin: 10px;
  van-button{
    float: right;
  }
  .button{
    float: right;
    margin-top: 33px;
    margin-right: 5px;
  }
  .img{
    display: inline-block;
    margin-left: 5px;
  img{
    width: 40px;
    height: 40px;
    margin-right: 30px;
  }
  }
}
.bbc{
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: #f1f9ffb6;
}

</style>
