import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
    isDemoUser: false,
    workoutSession: null,
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
    },
    LOGOUT(state) {
      state.user = null
      state.isAuthenticated = false
      state.isDemoUser = false
      state.workoutSession = null
      localStorage.removeItem('access_token')
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
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    isDemoUser: state => state.isDemoUser,
    workoutSession: state => state.workoutSession,
    workoutData: state => state.workoutData,
    userProfile: state => state.userProfile,
    calibrationData: state => state.calibrationData,
    audioSettings: state => state.audioSettings,
    nutritionSettings: state => state.nutritionSettings
  }
})