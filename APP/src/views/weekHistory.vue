<template>
  <div>
    <div class="nav">
      周 驾 驶 记 录
    </div>
    <!-- <div class="temp"></div> -->
    <router-link v-for="item in weekHistory" :key="item.drivingInformation.id" :to="{name: 'historydetail',params: {id:item.drivingInformation.id,obj: item}}">
      <div class="card">
          <van-icon name="todo-list-o" size="30px" color="black"/>
          <div>
            <p>开始时间: {{item.drivingInformation.begin}}</p>
            <p>结束时间: {{item.drivingInformation.end}}</p>
          </div>
      </div>
    </router-link>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
export default {
  name: 'history',
  computed: {
    ...mapState(['weekHistory', 'monthHistory']),
    ...mapGetters(['closeEye', 'attention'])
  },
  data () {
    return {

    }
  },
  created () {
  },
  methods: {
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
       border-radius: 10px;
       width: auto;
       height: 60px;
       padding: 10px;
       margin: 5px;
       box-shadow:  1px 1px 1px #fafafa;
       background-color: #fafafa;
       div{
         display: inline-block;
         margin-left: 10px;
         p{
           font-size: 10px;
           color: black;
         }
       }
}
.bbc{
  background-color: rgba(125, 255, 201, 0.555);
}
</style>
