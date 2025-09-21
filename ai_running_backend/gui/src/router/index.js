import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Workout from '../views/Workout.vue'
import Assessment from '../views/Assessment.vue'
import Profile from '../views/Profile.vue'
import Nutrition from '../views/Nutrition.vue'
import AudioSettings from '../views/AudioSettings.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/workout',
    name: 'Workout',
    component: Workout,
    meta: { requiresAuth: true }
  },
  {
    path: '/assessment',
    name: 'Assessment',
    component: Assessment,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/nutrition',
    name: 'Nutrition',
    component: Nutrition,
    meta: { requiresAuth: true }
  },
  {
    path: '/audio-settings',
    name: 'AudioSettings',
    component: AudioSettings,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // If user is already authenticated and tries to go to login, redirect to dashboard
    next('/dashboard')
  } else {
    next()
  }
})

export default router