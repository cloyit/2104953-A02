<template>

  <div>
    <div class="nav">
      登 录
    </div>
    <div class="login">
 <van-form @submit="onSubmit">
  <van-field
    v-model="username"
    name="手机号"
    label="手机号"
    placeholder="手机号"
    :rules="[{ required: true, message: '请填写手机号' }]"
  />
  <van-field
    v-model="password"
    type="password"
    name="密码"
    label="密码"
    placeholder="密码"
    :rules="[{ required: true, message: '请填写密码' }]"
  />
  <div style="margin: 16px;">
    <van-button round block type="info" native-type="submit">登录</van-button>
  </div> <div style="margin: 16px;">
    <router-link to="/resgiter">
    <van-button round block type="info" >注册</van-button>
    </router-link>
  </div>
</van-form>
  </div>
  <div style="text-align:center">
    <p>测试账号密码</p>
    <p>手机号：18222155748</p>
    <p>密码：123</p>
  </div>
  </div>
</template>

<script>
import { reqToken } from '@/api'
import { Toast } from 'vant'
export default {

  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async onSubmit (values) {
      const result = await reqToken(this.username, this.password)
      if (result.status === 200) {
        this.$store.commit('ADDToken', result.obj)
        setTimeout(() => {
          this.$store.dispatch('GetUser')
          this.$router.replace('/user')
        }, 1000)
      } else {
        this.password = ''
        Toast('密码或手机号错误')
      }
    }
  }
}
</script>

<style lang="less">
.lookback{
  margin-top: 20px;
  text-align: center;
}
.nav{
  height: 46px;
  background-color: #007bffd5;
  text-align: center;
  line-height: 46px;
  color: #fff;
}
</style>
