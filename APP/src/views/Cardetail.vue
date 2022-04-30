<template>
  <div class="bbc">
    <div class="nav">
      车 辆 详 情
    </div>
    <br>
    <!-- <div class="car">
          <div class="img"><router-link to="/user/detail1"><img src="@/assets/car1.png"/></router-link></div>
          <div class="img"><router-link to="/user/detail2"><img src="@/assets/car2.png"/></router-link></div>
          <div class="img"><router-link to="/user/detail3"><img src="@/assets/car3.png"/></router-link></div>
          <div class="img"><router-link to="/user/detail4"><img src="@/assets/more.png"/></router-link></div>
    </div>

  <div v-for="item in detail" :key="item.id">
    <div v-if="'detail'+item.id===$route.params.detail">
  <van-cell-group inset>
  <van-field
    v-model="item.type"
    label="车辆品牌"
  />
  <van-field
    v-model="item.num"
    label="车牌号"
  />
</van-cell-group>
  </div>
</div> -->

<div class="card" v-for="item in cars" :key="item.id">
          <van-icon name="logistics"  color="black" size="20px"/>
          <div>
            <p>车辆品牌: {{item.type}}</p>
            <p>车牌号: {{item.carNumber}}</p>
          </div>
          <van-icon name="cross" @click="Dialog(item.id)"/>

</div>
  <div>
    <br>
      <div style="margin: 0 10px">
        <van-button round type="primary" size="normal" color="#007BFF" block @click="add">新增车辆</van-button>
      </div>
      <!-- <br>
      <van-button round type="primary" size="normal" color="red" block @click="Dialog">删除</van-button> -->
  </div>

  </div>
</template>

<script>
import { reqDelCar } from '@/api'
import { Dialog, Toast } from 'vant'
import { mapState } from 'vuex'
export default {
  name: 'Cardetail',
  data () {
    return {
      reflash: true
    }
  },
  computed: {
    ...mapState(['cars'])
  },
  created () {
    this.$store.dispatch('getAllCar')
  },
  watch: {
  },
  methods: {

    add () {
      this.$router.push('/car/addcar')
    },
    Dialog (id) {
      Dialog.confirm({
        title: '确认删除？'
      })
        .then(() => {
          // on confirm
          reqDelCar([id])
          Toast('删除成功')
          setTimeout(() => {
            this.$store.dispatch('getAllCar')
          }, 1000)
          // this.$store.dispatch('getAllCar')
          // this.$router.push('/user')
        })
        .catch(() => {
          // on cancel
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
.card{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-radius: 10px;
      width: auto;
      height: 60px;
      padding: 10px 15px;
      margin-left: 10px;
      margin-right: 10px;
      margin-bottom: 10px;
      div{
         display: inline-block;
         margin-left: -50px;
         p{
           font-size: 14px;
           color: #323233;
         }
       }
       button{
          display: inline-block;
          height: 20px;
          width: 20px;
          border: 1px red solid;
          border-radius: 30%;
          background-color: red;
          color: #fff;
          font-size: 14px;
}
       background-color: #fff;
}

.button{
  display: block;
  width: 286px;
  height: 44px;
  text-align: center;
  margin: 0 auto;
  background-color: #007BFF;
  border: #007BFF;
  border-radius: 30px;
}
.bbc{
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: #f1f9ffb6;
}

</style>
