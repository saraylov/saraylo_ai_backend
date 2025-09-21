<template>
  <div class="audio-settings-view">
    <div class="container">
      <div class="header">
        <h1>Настройки аудио-ассистента</h1>
        <p>Персонализируйте ваше аудио-взаимодействие с системой</p>
      </div>

      <div class="settings-content">
        <!-- Voice Settings Card -->
        <div class="card glass-effect">
          <h2>Настройки голоса</h2>
          <div class="settings-group">
            <div class="setting-item">
              <label for="voice-type">Тип голоса:</label>
              <select id="voice-type" v-model="audioSettings.voiceType">
                <option value="female">Женский</option>
                <option value="male">Мужской</option>
              </select>
            </div>

            <div class="setting-item">
              <label for="voice-rate">Скорость речи:</label>
              <input 
                id="voice-rate" 
                type="range" 
                min="0.5" 
                max="2" 
                step="0.1" 
                v-model="audioSettings.voiceRate"
              >
              <div class="range-value">{{ audioSettings.voiceRate }}x</div>
            </div>

            <div class="setting-item">
              <label for="voice-volume">Громкость:</label>
              <input 
                id="voice-volume" 
                type="range" 
                min="0" 
                max="1" 
                step="0.1" 
                v-model="audioSettings.voiceVolume"
              >
              <div class="range-value">{{ Math.round(audioSettings.voiceVolume * 100) }}%</div>
            </div>

            <button @click="previewVoice" class="btn btn-secondary">
              Прослушать образец
            </button>
          </div>
        </div>

        <!-- Feedback Frequency Card -->
        <div class="card glass-effect">
          <h2>Частота обратной связи</h2>
          <div class="settings-group">
            <div class="setting-item">
              <label>Частота аудио-обратной связи:</label>
              <div class="radio-group">
                <label v-for="frequency in feedbackFrequencies" :key="frequency.value">
                  <input 
                    type="radio" 
                    :value="frequency.value" 
                    v-model="audioSettings.feedbackFrequency"
                  >
                  {{ frequency.label }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Language Settings Card -->
        <div class="card glass-effect">
          <h2>Языковые настройки</h2>
          <div class="settings-group">
            <div class="setting-item">
              <label for="language">Язык:</label>
              <select id="language" v-model="audioSettings.language">
                <option value="ru-RU">Русский</option>
                <option value="en-US">English</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Accessibility Settings Card -->
        <div class="card glass-effect">
          <h2>Настройки доступности</h2>
          <div class="settings-group">
            <div class="setting-item checkbox-item">
              <label>
                <input 
                  type="checkbox" 
                  v-model="audioSettings.visualIndicators"
                >
                Визуальные индикаторы для пользователей с нарушениями слуха
              </label>
            </div>

            <div class="setting-item checkbox-item">
              <label>
                <input 
                  type="checkbox" 
                  v-model="audioSettings.tactileFeedback"
                >
                Тактильная обратная связь
              </label>
            </div>

            <div class="setting-item checkbox-item">
              <label>
                <input 
                  type="checkbox" 
                  v-model="audioSettings.textToSpeechFallback"
                >
                Резервный переход к преобразованию текста в речь
              </label>
            </div>
          </div>
        </div>

        <!-- Save Button -->
        <div class="save-section">
          <button @click="saveSettings" class="btn btn-primary btn-large">
            Сохранить настройки
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AudioSettings',
  setup() {
    const store = useStore()
    
    const audioSettings = reactive({
      voiceType: 'female',
      voiceRate: 1.0,
      voiceVolume: 0.8,
      feedbackFrequency: 'medium',
      language: 'ru-RU',
      visualIndicators: true,
      tactileFeedback: false,
      textToSpeechFallback: true
    })
    
    const feedbackFrequencies = [
      { value: 'rare', label: 'Редко (один раз за тренировку)' },
      { value: 'medium', label: 'Средне (каждые 10-15 минут)' },
      { value: 'frequent', label: 'Часто (каждые 5 минут или при значительном улучшении)' }
    ]
    
    // Load settings from store or localStorage on mount
    onMounted(() => {
      const savedSettings = localStorage.getItem('audioSettings')
      if (savedSettings) {
        try {
          const parsedSettings = JSON.parse(savedSettings)
          Object.assign(audioSettings, parsedSettings)
        } catch (e) {
          console.error('Error parsing saved audio settings:', e)
        }
      }
    })
    
    const previewVoice = () => {
      // In a real app, this would trigger a voice preview
      alert(`Прослушивание образца голоса: ${audioSettings.voiceType}, скорость: ${audioSettings.voiceRate}x`)
    }
    
    const saveSettings = () => {
      // Save to localStorage
      localStorage.setItem('audioSettings', JSON.stringify(audioSettings))
      
      // In a real app, you might also save to a backend
      // store.commit('setAudioSettings', audioSettings)
      
      alert('Настройки аудио-ассистента сохранены!')
    }
    
    return {
      audioSettings,
      feedbackFrequencies,
      previewVoice,
      saveSettings
    }
  }
}
</script>

<style scoped>
.audio-settings-view {
  padding: 20px 0;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header p {
  font-size: 1.1rem;
  opacity: 0.8;
}

.settings-group {
  padding: 20px 0;
}

.setting-item {
  margin-bottom: 25px;
}

.setting-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.setting-item select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.setting-item input[type="range"] {
  width: 100%;
  margin: 10px 0;
}

.range-value {
  text-align: center;
  font-weight: bold;
  color: #00BFFF;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-group label {
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

.radio-group input {
  margin-right: 10px;
}

.checkbox-item label {
  display: flex;
  align-items: flex-start;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-item input {
  margin-top: 4px;
  margin-right: 10px;
}

.save-section {
  text-align: center;
  margin-top: 30px;
}

.btn-large {
  padding: 15px 30px;
  font-size: 1.1rem;
}
</style>