import requests from './requests'

// 获取全部车辆详情
export const reqAllCar = () => requests({ url: '/peach/car/getAllCar', method: 'get' })
// 登录
export const reqToken = (username, password) => requests({ url: `/peach/authentication/form?username=${username}&password=${password}`, method: 'post', params: { username, password } })
// 注册
export const reqRegister = (data) => requests({ url: '/peach/user/register', method: 'post', data })
// 紧急联系人
export const reqEmergency = () => requests({ url: '/peach/user/getEmergencyNumber', method: 'get' })
// 健康数据（15）
export const reqLastUserHealth = () => requests({ url: '/peach/health/getLastUserHealth', method: 'get' })
// 添加车辆
export const reqaddCar = (data) => requests({ url: '/peach/car/addCar', method: 'post', data })
// 删除车辆
export const reqDelCar = (data) => requests({ url: '/peach/car/deleteCarByIds', method: 'post', data })
// 完善个人信息
export const perfectInformation = (data) => requests({ url: '/peach/user/perfectInformation', method: 'post', data })
// 获取用户信息
export const reqGetUser = () => requests({ url: '/peach/user/getUser', method: 'get' })
// 获取一天的驾驶记录
export const reqDrivingInformationByDay = (beginTimeS) => requests({ url: `/peach/drivingInformation/getDrivingInformationByDay?beginTimeS=${beginTimeS}`, method: 'get' })
// 获取一段时间的驾驶记录
export const reqDrivingInformationByTime = (params) => requests({ url: `/peach/drivingInformation/getDrivingInformationByTime?beginTimeS=${params.beginTimeS}&endTimeS=${params.endTimeS}`, method: 'get' })
// 获取最新驾驶记录
export const reqDrivingInformationlast = () => requests({ url: '/peach/drivingInformation/getDrivingInformationLast', method: 'get' })
// 上传头像
export const reqUploadPortrait = (file) => requests({ url: '/peach/user/uploadPortrait', method: 'post', data: file })
// 获取健康数据
export const reqgetHealthByTime = (params) => requests({ url: `/peach/health/getHealthByTime?beginTimeS=${params.beginTimeS}&endTimeS=${params.endTimeS}`, method: 'get' })
// 获取体重
export const reqgetAllBmi = () => requests({ url: '/peach/bmi/getAllBmi', method: 'get' })
// 上传体重
export const requploadBmi = (data) => requests({ url: '/peach/bmi/uploadBmi', method: 'post', data })
// 获取驾驶图片
export const reqgetDPictureById = (params) => requests({ url: `/peach/drivingInformation/getDPictureById?did=${params}`, method: 'get' })
// 获取手环id
export const reqgetBracelet = () => requests({ url: '/peach/user/getBracelet', method: 'get' })
// 绑定手环
export const reqbindBracelet = (bracelet) => requests({ url: `/peach/user/bindBracelet?bracelet=${bracelet}`, method: 'post', params: { bracelet } })
