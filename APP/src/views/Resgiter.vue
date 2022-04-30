<template>
  <div>
    <div class="nav">
      注 册
    </div>
    <!-- <van-nav-bar
  title="注册"
  left-text="返回"
  left-arrow
  @click-left="onClickLeft"
/> -->
    <div class="login">
 <van-form @submit="onSubmit">
  <van-field
    v-model="username"
    name="id"
    label="手机号"
    placeholder="手机号"
    :rules="[{ required: true, message: '请输入手机号' }]"
  />
  <van-field
    v-model="password"
    type="password"
    name="password"
    label="密码"
    placeholder="密码"
    :rules="[{ required: true, message: '请输入密码' }]"
  />
  <van-field
    v-model="conpassword"
    type="password"
    name="conpassword"
    label="确认密码"
    placeholder="确认密码"
    :rules="[{ required: true, message: '请再次输入密码' }]"
  />
  <div style="margin: 16px;">
    <van-button round block type="info" native-type="submit">注册</van-button>
  </div> <div style="margin: 16px;">
  </div>
</van-form>
  </div>
  </div>
</template>

<script>
import { Toast } from 'vant'
import { reqRegister } from '@/api'
export default {
  name: 'Resgiter',
  data () {
    return {
      username: '',
      password: '',
      conpassword: ''
    }
  },
  methods: {
    onSubmit (values) {
      if (values.password !== values.conpassword) {
        Toast('密码不一致')
      } else {
        reqRegister({ tel: values.id, password: values.password })
        Toast('注册成功')
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style lang="less">
.login{
  margin-top: 100px;
}
.nav{
  height: 46px;
  background-color: #007bffd5;
  text-align: center;
  line-height: 46px;
  color: #fff;
}
</style>
