import { createApp } from "vue";
import App from "./App.vue";
import router from "./plugins/router"; // router.tsをインポート
import vuetify from "./plugins/vuetify"



const app = createApp(App);
app.use(router); // Vue Routerを使用する
app.use(vuetify); //vuetifyを使用する
app.mount("#app");
