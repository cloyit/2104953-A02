<template>
     <div class="user-container">
       <div class="user-card">
         <van-cell>
           <template #icon>
                <img :src="userinfo.headPortrait" alt="" class="avatar" v-if="userinfo!=={}"/>
           </template>
           <template #title>
             <span class="username" v-if="!userinfo.nickname">用户名</span>
             <span class="username" v-if="userinfo.nickname">{{userinfo.nickname}}</span>
           </template>
           <template #label>
             <router-link to="/login" v-if="!islogin"><van-tag color="#fff" text-color="#007bff">登录/注册</van-tag></router-link>
           </template>
         </van-cell>
       </div>
        <br>
        <div class="card-contain">
        <router-link to='/userdetail'>
          <div class="card" style="background-image: linear-gradient(to bottom right, #38dfc8, #38dfc8af);">
          <van-icon name="contact" size="30px" color="#fff"/>
          <br>
          <div><p>个人信息</p>
          <p v-if="userinfo.name && bmi.length !== 0">{{userinfo.gender}} {{bmi[bmi.length-1].height}}厘米</p>
          </div>
        </div>
        </router-link>
        <router-link to='/car/cardetail'>
          <div class="card" style=" background-image: linear-gradient(to bottom right, #199fff, #1dafffaf);">
          <van-icon name="logistics" size="30px" color="#fff" />
          <br>
          <div>
            <p>车辆信息</p>
          <p v-if="cars.length!=0">{{cars[0].type}} {{cars[0].carNumber}}</p>
          </div>
        </div>
        </router-link>
        <router-link to="/cardev">
          <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(230, 104, 104), rgba(230, 104, 104,0.7));">
          <van-icon name="desktop-o" size="30px" color="#fff"/>
          <br>
          <div><p>车载设备</p>
          <p v-if="userinfo.name">ZN-812</p>
          </div>
        </div>
        </router-link>

        <router-link to="/movdev">
          <div class="card" style="background-image: linear-gradient(to bottom right,  rgb(244, 177, 131), rgba(244, 177, 131,0.7));">
          <van-icon name="service-o" size="30px" color="#fff"/>
          <br>
          <div><p>可穿戴设备</p>
          <p v-if="userinfo.name">安徒生手环</p>
          </div>
        </div>
        </router-link>

       </div>
       <br>
       <van-cell-group class="action-card">
         <van-cell icon="phone-o" title="联系客服" @click="show = true" is-link />
         <van-cell icon="share-o" title="退出登录" is-link  @click="Dialog()" />
       </van-cell-group>
       <van-popup v-model="show" round>
    <div class="popup">
      <p>联系客服</p>
      <van-cell icon="phone-o" title="13036997541 热线1" />
      <van-cell icon="phone-o" title="18222155748 热线2" />
        <br>
    </div>
  </van-popup>
     </div>
</template>

<script>
import { mapState } from 'vuex'
import { Dialog, Toast } from 'vant'
export default {
  name: 'User',
  data () {
    return {
      islogin: false,
      show: false
    }
  },
  methods: {
    Dialog () {
      Dialog.confirm({
        title: '确认退出登录？'
      })
        .then(() => {
          // on confirm
          this.$store.commit('reset')
          Toast('退出成功')
          this.$router.replace('/login')
        })
        .catch(() => {
          // on cancel
        })
    }
  },
  computed: {
    ...mapState(['token', 'cars', 'userinfo', 'bmi'])
  },
  mounted () {
    if (this.token.length !== 0) {
      this.$store.dispatch('getLastUserHealth')
      this.$store.dispatch('GetUser')
      this.$store.dispatch('getAllCar')
      this.$store.dispatch('getAllBmi')
      this.islogin = true
      if (this.userinfo.nickname === '') {
        this.$router.push('/userdetail')
      }
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
   .user-container {
     .user-card {
       background-color: #007bff;
       color: white;
       padding-top: 20px;
       .van-cell {
         background: #007bff;
         color: white;
         &::after {
           display: none;
         }
         .avatar {
           width: 60px;
           height: 60px;
           background-color: #fff;
           border-radius: 50%;
           margin-right: 10px;
         }
         .username {
           font-size: 17px;
           font-weight: bold;
         }
       }
     }
     .img{
       border: 1px solid #ebedf0;
       border-radius: 10px;
       flex:1;
       text-align: center;
       p{
         margin: 0;
         padding: 0;
         color: #323233;
         font-size: 14px;
       }
     }
     .car {
       display: flex;
       justify-content: space-evenly;
       align-items: center;
       margin-top: 1px;
       img {
         height: 50px;
         width: 50px;
         border-radius: 50%;
       }
     }
     .card-contain{
       display: flex;
       flex-wrap: wrap;
       justify-content: space-around;
     }
     .card{
       display: inline-block;
       border-radius: 10px;
       width: 120px;
       height: 120px;
       padding: 10px;
       margin: 10px 0;
       img{
         display: inline-block;
         width: 60px;
       }
       div{
         display: inline-block;
         p{
           font-size: 14px;
           color: #fff;
         }
       }
     }
   }
</style>
