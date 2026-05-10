import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

import {createHead} from "@unhead/vue/client";

import "./styles/global.css"
import "./styles/tailwind.css";

const app = createApp(App)

const head = createHead()
app.use(head)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)

app.use(router)

app.mount('#app')
