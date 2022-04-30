<template>
  <div class="bbc">
    <div class="nav">
      可 穿 戴 设 备 详 情
    </div>
    <br>
    <div class="card">
          <van-icon name="service-o"  color="black" size="20px" />
          <div>
            <p>设备品牌: 安徒生手环</p>
            <p>设备ID: {{id}}</p>
          </div>
          <van-icon name="cross"/>

</div>
  <div>
    <br>
      <div style="margin: 0 10px">
        <van-button round type="primary" size="normal" color="#007BFF" block @click="showpo">更换设备</van-button>
      </div>
  </div>
  <van-popup v-model="show" round>
    <div class="popup">
      <p>更换绑定手环</p>
        <br>
        <van-field v-model="value" placeholder="请输入id" />
        <br>
      <van-button round block type="info" native-type="submit" @click="onSubmit">提交</van-button>
    </div>
  </van-popup>
  </div>
</template>

<script>
import { reqgetBracelet, reqbindBracelet } from '@/api'
export default {
  data () {
    return {
      id: '',
      show: false,
      value: ''
    }
  },
  created () {
    var res = reqgetBracelet()
    res.then((item) => {
      if (item.status === 200) { this.id = item.obj }
    }).catch()
  },
  methods: {
    showpo () {
      this.show = true
    },
    onSubmit () {
      this.show = false
      reqbindBracelet(this.value)
      this.value = ''
      setTimeout(() => {
        var res = reqgetBracelet()
        res.then((item) => {
          if (item.status === 200) { this.id = item.obj }
        }).catch()
      }, 1000)
    }
  }
}
</script>

<style lang='less' scoped>
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
.popup{
  width: 200px;
  height: 200px;
  margin: 10px 20px;
  padding: 10px;
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
