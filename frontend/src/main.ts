import './assets/main.css'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootswatch/dist/darkly/bootstrap.min.css'
import 'bootstrap'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(fab, fas)

import VueApexCharts from 'vue3-apexcharts'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(VueApexCharts as any)
app.use(router)

app.mount('#app')
