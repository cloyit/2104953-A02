import Vue from 'vue'
import Vuex from 'vuex'
import { reqToken, reqAllCar, reqEmergency, reqDelCar, reqLastUserHealth, reqGetUser, reqDrivingInformationlast, reqDrivingInformationByTime, reqgetHealthByTime, reqgetAllBmi } from '@/api'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: '',
    cars: [],
    emergencys: [],
    health: [],
    dayHealth: [],
    weekHealth: [],
    monthHealth: [],
    userinfo: {},
    weekHistory: [],
    lastHistory: {},
    bmi: []
  },
  mutations: {
    reset (state) {
      state.token = ''
      state.cars = []
      state.emergencys = []
      state.health = []
      state.dayHealth = []
      state.weekHealth = []
      state.monthHealth = []
      state.userinfo = {}
      state.weekHistory = []
      state.lastHistory = {}
      state.bmi = []
    },
    ADDToken (state, token) {
      state.token = token
    },
    GETAllCAR (state, obj) {
      state.cars = obj
    },
    GETEMERGENCY (state, obj) {
      state.emergencys = obj
    },
    GETLASTUSERHEALTH (state, obj) {
      obj[0].forEach((item) => {
        item.time = item.time.replace('T', ' ')
      })
      state.health = obj
    },
    GETUSER (state, obj) {
      state.userinfo = obj
    },
    GETDRIVINGHISTORYLAST (state, obj) {
      obj.begin = obj.begin.replace('T', ' ')
      obj.end = obj.end.replace('T', ' ')
      state.lastHistory = obj
    },
    GETALLBMI (state, obj) {
      obj.forEach((item) => {
        if (item.time !== null) {
          item.time = item.time.substring(0, 10)
        }
      })
      state.bmi = obj
    },
    GETDRIVINGHISTORYBYTIME (state, obj) {
      if (obj === null) state.weekHistory = []
      else {
        obj.forEach(function (p) {
          p.forEach(function (item) {
            item.begin = item.begin.replace('T', ' ')
            item.end = item.end.replace('T', ' ')
          })
        })
        state.weekHistory = obj
      }
    },
    GETDRIVINGHISTORYBYTIMEMONTH (state, obj) {
      if (obj === null) state.monthHistory = []
      else {
        obj.forEach(function (p) {
          p.forEach(function (item) {
            item.begin = item.begin.replace('T', ' ')
            item.end = item.end.replace('T', ' ')
          })
        })
        state.monthHistory = obj
      }
    },
    GETDAYHEALTH (state, obj) {
      if (obj.length === 0 || obj === null) state.dayHealth = []
      else {
        obj[0].forEach(item => {
          item.time = item.time.replace('T', ' ')
        })
        state.dayHealth = obj
      }
    },
    GETWEEKHEALTH (state, obj) {
      if (obj === null) state.weekHealth = []
      else {
        var temp = []
        obj.forEach((p) => {
          var avgbloodOxygen = 0
          var avgheartbeat = 0
          var avgtemperature = 0
          var maxbloodOxygen = -1e9
          var maxheartbeat = -1e9
          var maxtemperature = -1e9
          var minbloodOxygen = 1e9
          var minheartbeat = 1e9
          var mintemperature = 1e9
          p.forEach((item) => {
            avgbloodOxygen += Number(item.bloodOxygen)
            avgheartbeat += Number(item.heartbeat)
            avgtemperature += Number(item.temperature)
            maxbloodOxygen = Math.max(maxbloodOxygen, Number(item.bloodOxygen))
            maxheartbeat = Math.max(maxheartbeat, Number(item.heartbeat))
            maxtemperature = Math.max(maxtemperature, Number(item.temperature))
            minbloodOxygen = Math.min(minbloodOxygen, Number(item.bloodOxygen))
            minheartbeat = Math.min(minheartbeat, Number(item.heartbeat))
            mintemperature = Math.min(mintemperature, Number(item.temperature))
          })
          var t = {}
          t.avgbloodOxygen = (avgbloodOxygen / p.length).toFixed(2)
          t.avgheartbeat = (avgheartbeat / p.length).toFixed(2)
          t.avgtemperature = (avgtemperature / p.length).toFixed(2)
          t.maxbloodOxygen = maxbloodOxygen
          t.maxheartbeat = maxheartbeat
          t.maxtemperature = maxtemperature
          t.minbloodOxygen = minbloodOxygen
          t.minheartbeat = minheartbeat
          t.mintemperature = mintemperature
          t.time = p[0].time.substring(5, 10)
          temp.push(t)
        })
        state.weekHealth = temp
      }
    },
    GETMONTHHEALTH (state, obj) {
      if (obj === null) state.monthHealth = []
      else {
        var temp = []
        obj.forEach((p) => {
          var avgbloodOxygen = 0
          var avgheartbeat = 0
          var avgtemperature = 0
          var maxbloodOxygen = -1e9
          var maxheartbeat = -1e9
          var maxtemperature = -1e9
          var minbloodOxygen = 1e9
          var minheartbeat = 1e9
          var mintemperature = 1e9
          p.forEach((item) => {
            avgbloodOxygen += Number(item.bloodOxygen)
            avgheartbeat += Number(item.heartbeat)
            avgtemperature += Number(item.temperature)
            maxbloodOxygen = Math.max(maxbloodOxygen, Number(item.bloodOxygen))
            maxheartbeat = Math.max(maxheartbeat, Number(item.heartbeat))
            maxtemperature = Math.max(maxtemperature, Number(item.temperature))
            minbloodOxygen = Math.min(minbloodOxygen, Number(item.bloodOxygen))
            minheartbeat = Math.min(minheartbeat, Number(item.heartbeat))
            mintemperature = Math.min(mintemperature, Number(item.temperature))
          })
          var t = {}
          t.avgbloodOxygen = (avgbloodOxygen / p.length).toFixed(2)
          t.avgheartbeat = (avgheartbeat / p.length).toFixed(2)
          t.avgtemperature = (avgtemperature / p.length).toFixed(2)
          t.maxbloodOxygen = maxbloodOxygen
          t.maxheartbeat = maxheartbeat
          t.maxtemperature = maxtemperature
          t.minbloodOxygen = minbloodOxygen
          t.minheartbeat = minheartbeat
          t.mintemperature = mintemperature
          t.time = p[0].time.substring(0, 10)
          temp.push(t)
        })
        state.monthHealth = temp
      }
    }
  },
  actions: {
    async getToken ({ commit }, { username, password }) {
      const result = await reqToken(username, password)
      if (result.status === 200) {
        commit('ADDToken', result.obj)
      }
    },
    async getAllCar ({ commit }) {
      const result = await reqAllCar()
      if (result.status === 200) {
        commit('GETAllCAR', result.obj)
      }
    },
    async getEmergency ({ commit }) {
      const result = await reqEmergency()
      if (result.status === 200) {
        commit('GETEMERGENCY', result.obj)
      }
    },
    async getLastUserHealth ({ commit }) {
      const result = await reqLastUserHealth()
      if (result.status === 200) {
        commit('GETLASTUSERHEALTH', result.obj)
      }
    },
    async GetUser ({ commit }) {
      const result = await reqGetUser()
      if (result.status === 200) {
        commit('GETUSER', result.obj)
      }
    },
    async getDrivingInformationLast ({ commit }) {
      const result = await reqDrivingInformationlast()
      if (result.status === 200) {
        commit('GETDRIVINGHISTORYLAST', result.obj)
      }
    },
    async getDrivingInformationByTime ({ commit }, params) {
      const result = await reqDrivingInformationByTime(params)
      if (result.status === 200) {
        commit('GETDRIVINGHISTORYBYTIME', result.obj)
      }
      if (result.msg === 'is empty') {
        commit('GETDRIVINGHISTORYBYTIME', result.obj)
      }
    },
    async getDayHealth ({ commit }, params) {
      const result = await reqgetHealthByTime(params)
      if (result.status === 200) {
        commit('GETDAYHEALTH', result.obj)
      }
    },
    async getWeekHealth ({ commit }, params) {
      const result = await reqgetHealthByTime(params)
      if (result.status === 200) {
        commit('GETWEEKHEALTH', result.obj)
      }
    },
    async getMonthHealth ({ commit }, params) {
      const result = await reqgetHealthByTime(params)
      if (result.status === 200) {
        commit('GETMONTHHEALTH', result.obj)
      }
    },
    async getDrivingInformationByTimeMonth ({ commit }, params) {
      const result = await reqDrivingInformationByTime(params)
      if (result.status === 200) {
        commit('GETDRIVINGHISTORYBYTIMEMONTH', result.obj)
      }
    },
    async DelCarById ({ commit }, id) {
      const result = await reqDelCar(id)
      if (result.status === 200) {
      }
    },
    async getAllBmi ({ commit }) {
      const result = await reqgetAllBmi()
      if (result.status === 200) {
        commit('GETALLBMI', result.obj)
      }
    }
  },
  modules: {
  },
  getters: {
    bloodOxygen (state) {
      var bloodOxygens = []
      state.health[0].forEach(function (item) {
        bloodOxygens.push(item.bloodOxygen)
      })
      return bloodOxygens
    },
    temperature (state) {
      var temperatures = []
      state.health[0].forEach(function (item) {
        temperatures.push(item.temperature)
      })
      return temperatures
    },
    heartbeat (state) {
      var heartbeats = []
      state.health[0].forEach(function (item) {
        heartbeats.push(item.heartbeat)
      })
      return heartbeats
    },
    closeEye (state) {
      var closeEye = []

      state.weekHistory.forEach(function (p) {
        p.forEach(function (item) {
          closeEye.push(item.closeEye)
        })
      })

      return closeEye
    },
    attention (state) {
      var attention = []
      state.weekHistory.forEach(function (p) {
        p.forEach(function (item) {
          attention.push(item.attention)
        })
      })
      return attention
    },
    yawn (state) {
      var yawn = []
      state.weekHistory.forEach(function (p) {
        p.forEach(function (item) {
          yawn.push(item.yawn)
        })
      })
      return yawn
    }
  }
})
