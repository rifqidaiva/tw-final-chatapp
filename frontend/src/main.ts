import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import NotFound from './components/pages/NotFound.vue'
import Login from './components/pages/Login.vue'
import Register from './components/pages/Register.vue'

import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
  ],
})

createApp(App).use(router).mount('#app')
