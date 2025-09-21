import axios from 'axios'

// Создаем экземпляр axios с базовой конфигурацией
const apiClient = axios.create({
  baseURL: '/api', // Используем прокси, определенный в vite.config.js
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Интерцептор для добавления токена авторизации к каждому запросу
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Интерцептор для обработки ошибок авторизации
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Если токен недействителен, удаляем его и перенаправляем на страницу входа
      localStorage.removeItem('access_token')
      localStorage.removeItem('api_key')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Аутентификация
  login(apiKey) {
    return apiClient.post('/v1/auth/login', { api_key: apiKey })
  },
  
  // Аутентификация через Telegram
  telegramLogin(telegramData) {
    return apiClient.post('/auth/telegram', telegramData)
  },
  
  // Управление сессиями тренировок
  startWorkoutSession(userData) {
    // Получаем API ключ из localStorage или используем переданный
    const apiKey = localStorage.getItem('api_key') || userData.api_key
    return apiClient.post('/v1/workout/start', { ...userData, api_key: apiKey })
  },
  
  updateWorkoutSession(workoutData) {
    return apiClient.post('/v1/workout/update', workoutData)
  },
  
  endWorkoutSession(sessionData) {
    return apiClient.post('/v1/workout/end', sessionData)
  },
  
  // Управление профилем пользователя
  getUserProfile() {
    // В реальной системе это будет GET запрос к API
    // Пока возвращаем фиктивные данные
    return Promise.resolve({
      data: {
        user_id: 'user123',
        age: 30,
        gender: 'male',
        weight_kg: 70,
        height_cm: 175,
        fitness_level: 2
      }
    })
  },
  
  updateUserProfile(profileData) {
    // В реальной системе это будет PUT/POST запрос к API
    return Promise.resolve({ data: { status: 'success' } })
  },
  
  // Калибровочные данные
  getCalibrationData() {
    // В реальной системе это будет GET запрос к API
    // Пока возвращаем фиктивные данные
    return Promise.resolve({
      data: {
        "10%": 2.8,
        "20%": 3.2,
        "30%": 3.6,
        "40%": 4.0,
        "50%": 4.4,
        "60%": 4.8,
        "70%": 5.2,
        "80%": 5.6,
        "90%": 6.0,
        "100%": 6.4
      }
    })
  },
  
  saveCalibrationData(calibrationData) {
    // В реальной системе это будет POST запрос к API
    return Promise.resolve({ data: { status: 'success' } })
  },
  
  // Добавляем функцию для отправки элементов данных
  sendElement(elementData) {
    return apiClient.post('/v1/elements/send', elementData)
  },
  
  // Функция для получения элементов данных (если потребуется)
  getElements() {
    return apiClient.get('/v1/elements')
  },
  
  // Функция для получения конкретного элемента по ID
  getElementById(elementId) {
    return apiClient.get(`/v1/elements/${elementId}`)
  },
  
  // Система питания
  setNutritionPreferences(preferences) {
    return apiClient.post('/v1/nutrition/preferences', preferences)
  },
  
  generateNutritionPlan(planData) {
    return apiClient.post('/v1/nutrition/plan', planData)
  }
}