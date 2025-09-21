import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
    isDemoUser: false,
    isTelegramUser: false,
    apiKey: null,
    workoutSession: null,
    // Добавляем поле для элементов
    elements: [],
    workoutData: {
      currentLoad: 0,
      fatigueLevel: 'low',
      recoveryState: 100,
      trainingEffectiveness: 'optimal',
      timeToExhaustion: '00:00',
      recommendations: []
    },
    userProfile: {
      user_id: 'user123',
      age: 30,
      gender: 'male',
      weight_kg: 70,
      height_cm: 175,
      fitness_level: 2
    },
    calibrationData: {},
    audioSettings: {
      voiceType: 'female',
      voiceRate: 1.0,
      voiceVolume: 0.8,
      feedbackFrequency: 'medium',
      language: 'ru-RU',
      visualIndicators: true,
      tactileFeedback: false,
      textToSpeechFallback: true
    },
    nutritionSettings: {
      goal: 'general_health',
      restrictions: [],
      cuisines: []
    }
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = true
      state.isDemoUser = user.isDemo || false
      state.isTelegramUser = user.isTelegramUser || false
      state.apiKey = user.apiKey || null
    },
    LOGOUT(state) {
      state.user = null
      state.isAuthenticated = false
      state.isDemoUser = false
      state.isTelegramUser = false
      state.apiKey = null
      state.workoutSession = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('api_key')
    },
    SET_WORKOUT_SESSION(state, session) {
      state.workoutSession = session
    },
    UPDATE_WORKOUT_DATA(state, data) {
      state.workoutData = { ...state.workoutData, ...data }
    },
    SET_USER_PROFILE(state, profile) {
      state.userProfile = { ...state.userProfile, ...profile }
    },
    SET_CALIBRATION_DATA(state, data) {
      state.calibrationData = { ...state.calibrationData, ...data }
    },
    SET_AUDIO_SETTINGS(state, settings) {
      state.audioSettings = { ...state.audioSettings, ...settings }
    },
    SET_NUTRITION_SETTINGS(state, settings) {
      state.nutritionSettings = { ...state.nutritionSettings, ...settings }
    },
    SET_API_KEY(state, apiKey) {
      state.apiKey = apiKey
    },
    
    // Добавляем мутацию для элементов
    ADD_ELEMENT(state, element) {
      // Создаем массив элементов, если его еще нет
      if (!state.elements) {
        state.elements = []
      }
      state.elements.push(element)
    },
    
    SET_ELEMENTS(state, elements) {
      state.elements = elements
    }
  },
  actions: {
    login({ commit }, userData) {
      // В реальной системе здесь будет API вызов
      commit('SET_USER', userData)
      return Promise.resolve()
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    // Добавляем действие для отправки элементов
    async sendElement({ commit }, elementData) {
      try {
        // В реальной системе здесь будет API вызов
        // const response = await api.sendElement(elementData)
        // Пока используем имитацию
        console.log('Sending element:', elementData)
        
        // Добавляем элемент в состояние
        commit('ADD_ELEMENT', elementData)
        
        return Promise.resolve({ data: { status: 'success', message: 'Element sent successfully' } })
      } catch (error) {
        console.error('Error sending element:', error)
        return Promise.reject(error)
      }
    },
    
    // Добавляем действие для получения элементов
    async getElements({ commit }) {
      try {
        // В реальной системе здесь будет API вызов
        // const response = await api.getElements()
        // Пока используем имитацию
        return Promise.resolve({ 
          data: { 
            status: 'success', 
            elements: [
              { id: 1, type: 'workout_data', timestamp: new Date().toISOString() },
              { id: 2, type: 'heart_rate', timestamp: new Date().toISOString() }
            ]
          } 
        })
      } catch (error) {
        console.error('Error getting elements:', error)
        return Promise.reject(error)
      }
    },
    
    startWorkoutSession({ commit }, sessionData) {
      commit('SET_WORKOUT_SESSION', sessionData)
    },
    updateWorkoutData({ commit }, workoutData) {
      commit('UPDATE_WORKOUT_DATA', workoutData)
    },
    updateUserProfile({ commit }, profileData) {
      commit('SET_USER_PROFILE', profileData)
    },
    setCalibrationData({ commit }, calibrationData) {
      commit('SET_CALIBRATION_DATA', calibrationData)
    },
    setAudioSettings({ commit }, audioSettings) {
      commit('SET_AUDIO_SETTINGS', audioSettings)
    },
    setNutritionSettings({ commit }, nutritionSettings) {
      commit('SET_NUTRITION_SETTINGS', nutritionSettings)
    },
    setApiKey({ commit }, apiKey) {
      commit('SET_API_KEY', apiKey)
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    isDemoUser: state => state.isDemoUser,
    isTelegramUser: state => state.isTelegramUser,
    apiKey: state => state.apiKey,
    workoutSession: state => state.workoutSession,
    workoutData: state => state.workoutData,
    userProfile: state => state.userProfile,
    calibrationData: state => state.calibrationData,
    audioSettings: state => state.audioSettings,
    nutritionSettings: state => state.nutritionSettings,
    // Добавляем геттер для элементов
    elements: state => state.elements
  }
})