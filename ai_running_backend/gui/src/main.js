import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Создаем Vue приложение
const app = createApp(App)

// Регистрируем router и store
app.use(router)
app.use(store)

// Монтируем приложение
app.mount('#app')