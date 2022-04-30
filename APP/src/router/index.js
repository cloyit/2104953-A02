import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/login'
import User from '@/views/User.vue'
import Home from '@/views/Home.vue'
import History from '@/views/history.vue'
import Cardetail from '@/views/Cardetail.vue'
import Resgiter from '@/views/Resgiter.vue'
import Userdetail from '@/views/userdetail.vue'
import AddCar from '@/views/AddCar.vue'
import HistoryDetail from '@/views/historyDetail.vue'
import WeekHistory from '@/views/weekHistory.vue'
import Bmi from '@/components/bmi.vue'
import bloodOxygen from '@/components/blood.vue'
import Temperature from '@/components/temperature.vue'
import Heartbeat from '@/components/heartbeat.vue'
import CarDev from '@/views/carDev.vue'
import MovDev from '@/views/movDev.vue'
import HealthReport from '@/views/healthReport.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/history', component: History },
  { path: '/user', component: User },
  { path: '/login', component: Login },
  { path: '/resgiter', component: Resgiter },
  { path: '/userdetail', component: Userdetail },
  { path: '/cardev', component: CarDev },
  { path: '/movdev', component: MovDev },
  { path: '/health/healthReport', component: HealthReport },
  { path: '/home', component: Home },
  { path: '/car/cardetail', component: Cardetail },
  { path: '/weekhistory', component: WeekHistory },
  { path: '/health/bmi', component: Bmi },
  { path: '/health/temperature', component: Temperature },
  { path: '/health/heartbeat', component: Heartbeat },
  { path: '/health/bloodoxygen', component: bloodOxygen },
  { path: '/car/addcar', component: AddCar },
  { path: '/historydetail/:id', component: HistoryDetail, name: 'historydetail' }
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  if (to.path === '/home') {
    sessionStorage.quit = 1
  } else {
    sessionStorage.quit = 0
  }
  next()
})
router.afterEach(() => { document.body.scrollTop = 0; document.documentElement.scrollTop = 0 })
export default router
