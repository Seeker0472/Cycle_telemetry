import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// const { dialog } = require('electron')
// console.log(dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] }))

import dayjs from "dayjs"
import utc from 'dayjs-plugin-utc'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'
dayjs.extend(isSameOrBefore)
dayjs.extend(utc)

// import Vue3BaiduMapGL from 'vue3-baidu-map-gl'

const app = createApp(App)
app.config.globalProperties.$dayjs = dayjs;
app.use(ElementPlus)
// app.use(Vue3BaiduMapGL, {
//     ak: 'qGX0DAQrfrdJ7HFCzg73UVSnyJwruKk7'
// })

app.mount('#app')


