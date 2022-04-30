<template>
  <div>
    <div class="nav">
      新 增 车 辆
    </div>
    <br>
    <van-cell-group inset>
      <van-field
        v-model="type"
        label="车辆品牌"
        placeholder="请输入车辆品牌"
      />
      <van-field
        v-model="carNumber"
        label="车牌号"
        placeholder="请输入车牌号"
      />
    </van-cell-group>
    <br>
    <div style="margin: 0 10px"><van-button round type="primary" size="normal" color="#007BFF" block @click="onSave">保存</van-button></div>

</div>
</template>

<script>
import { Toast } from 'vant'
import { reqaddCar } from '@/api'
export default {
  data () {
    return {
      type: '',
      carNumber: ''
    }
  },
  methods: {
    onSave () {
      reqaddCar({ type: this.type, carNumber: this.carNumber })
      setTimeout(() => {
        this.$store.dispatch('getAllCar')
        this.$router.replace('/car/cardetail')
      }, 1000)
      Toast('保存成功')
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
</style>
