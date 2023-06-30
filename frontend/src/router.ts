// router.ts
import { createRouter,createWebHistory } from 'vue-router';
import Home from "./Home.vue";

const routes = [
    { path: '/', component: Home }
]

const router = createRouter({
    history: createWebHistory(), // HTML5 History モード
    routes,
})

export default router;
