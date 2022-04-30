<template>
  <div>
    <div class="nav">个 人 信 息</div>
    <van-cell-group inset>
      <van-divider @click="show = true">
        <img
          :src="userinfo.headPortrait"
          alt=""
          class="avatar"
          v-if="userinfo !== {}"
        />
      </van-divider>

      <input type="file" id="test" />
      <van-action-sheet v-model="show" :actions="actions" @select="onSelect">
        <div class="content"></div>
      </van-action-sheet>

      <van-field v-model="userinfo.name" label="姓名" />
      <van-field v-model="userinfo.tel" label="手机号" />
      <van-field v-model="userinfo.gender" label="性别" />
      <van-field v-model="userinfo.nickname" label="用户名" />
      <!-- 允许输入正整数，调起纯数字键盘 -->
      <van-field v-model="userinfo.year" type="digit" label="年龄" />
      <!-- 允许输入数字，调起带符号的纯数字键盘 -->
      <van-field v-model="bmi[bmi.length-1].height" type="number" label="身高" readonly/>
      <van-field v-model="bmi[bmi.length-1].weight" type="number" label="体重" readonly/>
      <van-field
        v-model="userinfo.emergencyNumber"
        type="number"
        label="紧急联系人"
      />
      <van-button
        round
        type="primary"
        size="normal"
        color="#007BFF"
        block
        @click="onSave"
        style="margin-top: 5px"
        >保存</van-button
      >
    </van-cell-group>
  </div>
</template>

<script>
import { Toast } from 'vant'
import { mapState } from 'vuex'
import { perfectInformation, reqUploadPortrait } from '@/api'
export default {
  data () {
    return {
      show: false,
      actions: [{ name: '上传头像' }]
    }
  },
  computed: {
    ...mapState(['userinfo', 'bmi'])
  },
  methods: {
    comReqImg () {
      var input = document.getElementById('test')
      if (input.files[0]) {
        var formdata = new FormData()
        formdata.append('file', input.files[0])
        reqUploadPortrait(formdata)
        this.userinfo.headPortrait = this.getObjectURL(input.files[0])
      }
    },
    getObjectURL (file) {
      var url = null
      // 下面函数执行的效果是一样的，只是需要针对不同的浏览器执行不同的 js 函数而已
      if (window.createObjectURL !== undefined) { // basic
        url = window.createObjectURL(file)
      } else if (window.URL !== undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file)
      } else if (window.webkitURL !== undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file)
      }
      return url
    },
    inputImg () {
      var input = document.getElementById('test')
      input.click()
    },
    onSave () {
      perfectInformation(this.userinfo)
      this.comReqImg()
      Toast('保存成功')
    },
    onSelect (item) {
      // 默认情况下点击选项时不会自动收起
      // 可以通过 close-on-click-action 属性开启自动收起
      this.show = false
      if (item.name === '上传头像') {
        this.inputImg()
      }
      Toast(item.name)
    }
  }
}
</script>

<style lang="less" scoped>
#test {
  visibility: hidden;
}
.nav {
  height: 46px;
  background-color: #007bffd5;
  text-align: center;
  line-height: 46px;
  color: #fff;
}
.avatar {
  width: 60px;
  height: 60px;
  background-color: #fff;
  border-radius: 50%;
  margin-right: 10px;
}
.content {
  text-align: center;
}
</style>
