import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

//axios
import axios from 'axios'
axios.defaults.baseURL = 'http://localhost:5000'

// const { dialog } = require('electron')
// console.log(dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] }))

//dayjs
import dayjs from "dayjs"
import utc from 'dayjs-plugin-utc'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'

dayjs.extend(isSameOrBefore)
dayjs.extend(utc)

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.config.globalProperties.$dayjs = dayjs;
app.config.globalProperties.$axios = axios;
app.use(ElementPlus)


app.mount('#app')


