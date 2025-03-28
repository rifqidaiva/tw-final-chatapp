import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import PageNotFound from './components/pages/PageNotFound.vue'
import PageLogin from './components/pages/PageLogin.vue'
import PageRegister from './components/pages/PageRegister.vue'
import PageChats from './components/pages/Chats/Chats.vue'

import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: PageNotFound },
    { path: '/', redirect: '/login' },
    { path: '/login', component: PageLogin },
    { path: '/register', component: PageRegister },
    { path: '/chats', component: PageChats },
  ],
})

createApp(App).use(router).mount('#app')
