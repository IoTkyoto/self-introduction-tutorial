import { createApp } from 'vue'
// import './style.css'
import App from './App.vue'
import router from './router'; // router.tsをインポート

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App)
app.use(router) // Vue Routerを使用する
app.use(vuetify)//vuetifyを使用する
app.mount('#app')
// createApp(App).use(vuetify).mount('#app')


// createApp(App).use(router).mount('#app')


