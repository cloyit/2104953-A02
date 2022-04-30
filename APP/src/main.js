import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vant from 'vant'
import 'vant/lib/index.css'
import * as echarts from 'echarts'
import Mui from 'vue-awesome-mui'

Vue.prototype.$echarts = echarts
Vue.config.productionTip = false

Vue.use(Vant)
Vue.use(Mui)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
