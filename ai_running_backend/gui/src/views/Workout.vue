<template>
  <div class="training-screen">
    <!-- Training Stats (Height reduced by 30%) -->
    <div class="training-stats glass-panel">
      <div class="stat-item">
        <span class="stat-label">Время</span>
        <span class="stat-value">{{ formattedTime }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Дистанция</span>
        <span class="stat-value">{{ distance }} км</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Скорость</span>
        <span class="stat-value">{{ speed }} км/ч</span>
      </div>
    </div>
    
    <!-- Workout Button Container -->
    <div class="workout-button-container">
      <button 
        class="workout-button" 
        :class="buttonClass"
        @click="toggleWorkout"
      >
        <div class="circular-progress" v-if="isSessionActive">
          <svg viewBox="0 0 120 120">
            <circle class="progress-background" cx="60" cy="60" r="54"></circle>
            <circle 
              class="progress-indicator" 
              cx="60" 
              cy="60" 
              r="54"
              :stroke-dashoffset="progressOffset"
            ></circle>
          </svg>
        </div>
        <span class="button-label">{{ buttonLabel }}</span>
      </button>
    </div>
    
    <!-- Additional workout data -->
    <div class="workout-details glass-panel" v-if="isSessionActive">
      <div class="detail-item">
        <span class="detail-label">Текущая нагрузка</span>
        <span class="detail-value">{{ workoutData.currentLoad }}%</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Уровень усталости</span>
        <span class="detail-value">{{ fatigueLevelText }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Состояние восстановления</span>
        <span class="detail-value">{{ workoutData.recoveryState }}%</span>
      </div>
      
      <!-- Добавляем кнопку для отправки элемента -->
      <div class="send-element-container">
        <button @click="handleSendElement" class="send-element-button">
          Отправить элемент
        </button>
      </div>
    </div>
    
    <!-- AI Recommendations -->
    <div class="recommendations glass-panel" v-if="workoutData.recommendations.length > 0">
      <h3>Рекомендации ИИ</h3>
      <div class="recommendations-list">
        <div 
          v-for="(rec, index) in workoutData.recommendations" 
          :key="index" 
          class="recommendation-item"
        >
          <div class="rec-icon">{{ rec.type === 'adjustment' ? '⚙️' : '💡' }}</div>
          <div class="rec-text">{{ rec.text }}</div>
        </div>
      </div>
    </div>
    
    <!-- Отображение отправленных элементов -->
    <div class="elements-panel glass-panel" v-if="elements.length > 0">
      <h3>Отправленные элементы</h3>
      <div class="elements-list">
        <div 
          v-for="(element, index) in elements" 
          :key="index" 
          class="element-item"
        >
          <div class="element-info">
            <span class="element-type">{{ element.type }}</span>
            <span class="element-time">{{ new Date(element.timestamp).toLocaleTimeString() }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Audio Assistant -->
    <AudioAssistant ref="audioAssistant" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import AudioAssistant from '../components/AudioAssistant.vue'
import api from '../services/api.js'

export default {
  name: 'Workout',
  components: {
    AudioAssistant
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const audioAssistant = ref(null)
    
    // Workout state
    const isSessionActive = ref(false)
    const sessionId = ref('')
    const startTime = ref(null)
    const timerInterval = ref(null)
    const elapsedTime = ref(0)
    
    // Simulated data
    const distance = ref(0)
    const speed = ref(0)
    
    // Workout data
    const workoutData = computed(() => store.state.workoutData)
    const userProfile = computed(() => store.state.userProfile)
    const apiKey = computed(() => store.state.apiKey)
    const user = computed(() => store.state.user)
    // Добавляем вычисляемое свойство для элементов
    const elements = computed(() => store.state.elements)
    
    // Computed properties for text display
    const fatigueLevelText = computed(() => {
      const levels = {
        'low': 'Низкий',
        'medium': 'Средний',
        'high': 'Высокий'
      }
      return levels[workoutData.value.fatigueLevel] || workoutData.value.fatigueLevel
    })
    
    const formattedTime = computed(() => {
      const totalSeconds = elapsedTime.value
      const hours = Math.floor(totalSeconds / 3600)
      const minutes = Math.floor((totalSeconds % 3600) / 60)
      const seconds = totalSeconds % 60
      
      if (hours > 0) {
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
      }
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    })
    
    // Button properties
    const buttonLabel = computed(() => {
      if (!isSessionActive.value) return 'СТАРТ'
      return 'СТОП'
    })
    
    const buttonClass = computed(() => {
      if (!isSessionActive.value) return 'start-button'
      return 'stop-button'
    })
    
    // Progress circle
    const progressOffset = computed(() => {
      const progress = (elapsedTime.value % 60) / 60
      return 339.292 - (339.292 * progress)
    })
    
    // Toggle workout session
    const toggleWorkout = () => {
      if (isSessionActive.value) {
        endWorkout()
      } else {
        startWorkout()
      }
    }
    
    // Start workout session
    const startWorkout = async () => {
      try {
        // Подготавливаем данные для начала тренировки
        const sessionData = {
          user_id: userProfile.value.user_id,
          start_time: new Date().toISOString(),
          user_profile: userProfile.value
        }
        
        // Если у пользователя есть API ключ, добавляем его в данные
        if (apiKey.value) {
          sessionData.api_key = apiKey.value
        } else if (user.value && user.value.api_key) {
          sessionData.api_key = user.value.api_key
        }
        
        // For demo purposes, we'll just simulate a response
        sessionId.value = 'session_' + Date.now()
        isSessionActive.value = true
        startTime.value = Date.now()
        elapsedTime.value = 0
        
        // Start timer
        timerInterval.value = setInterval(() => {
          elapsedTime.value = Math.floor((Date.now() - startTime.value) / 1000)
          
          // Simulate distance and speed
          distance.value = (elapsedTime.value / 60 * 0.2).toFixed(2)
          speed.value = (0.2 + Math.random() * 0.1).toFixed(1)
        }, 1000)
        
        // Store session in Vuex
        store.dispatch('startWorkoutSession', { session_id: sessionId.value })
        
        // Notify audio assistant
        if (audioAssistant.value) {
          audioAssistant.value.sayHello()
        }
      } catch (error) {
        console.error('Error starting workout session:', error)
      }
    }
    
    // End workout session
    const endWorkout = async () => {
      if (!isSessionActive.value) return
      
      try {
        // Clean up
        isSessionActive.value = false
        if (timerInterval.value) {
          clearInterval(timerInterval.value)
        }
        
        // Redirect to dashboard
        router.push('/dashboard')
      } catch (error) {
        console.error('Error ending workout session:', error)
      }
    }
    
    // Добавляем метод для отправки элементов данных
    const sendElement = async (elementData) => {
      try {
        // Используем действие из хранилища Vuex
        const response = await store.dispatch('sendElement', elementData)
        console.log('Element sent successfully:', response.data)
        return response.data
      } catch (error) {
        console.error('Error sending element:', error)
        throw error
      }
    }
    
    // Добавляем обработчик для кнопки отправки элемента
    const handleSendElement = async () => {
      try {
        // Подготавливаем данные для отправки
        const elementData = {
          id: Date.now(), // Уникальный ID для элемента
          type: 'workout_data',
          session_id: sessionId.value,
          timestamp: new Date().toISOString(),
          workout_data: {
            current_load: workoutData.value.currentLoad,
            fatigue_level: workoutData.value.fatigueLevel,
            recovery_state: workoutData.value.recoveryState,
            elapsed_time: elapsedTime.value,
            distance: distance.value,
            speed: speed.value
          },
          user_id: userProfile.value.user_id
        }
        
        // Отправляем элемент
        await sendElement(elementData)
        
        // Уведомляем пользователя об успешной отправке
        if (audioAssistant.value) {
          audioAssistant.value.speak('Элемент данных успешно отправлен')
        }
      } catch (error) {
        console.error('Failed to send element:', error)
        // Уведомляем пользователя об ошибке
        if (audioAssistant.value) {
          audioAssistant.value.speak('Ошибка при отправке элемента данных')
        }
      }
    }
    
    // Simulate real-time data updates
    const simulateDataUpdates = () => {
      setInterval(() => {
        if (!isSessionActive.value) return
        
        const newData = {
          currentLoad: Math.min(100, Math.max(0, workoutData.value.currentLoad + (Math.random() * 10 - 5))),
          fatigueLevel: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)],
          recoveryState: Math.min(100, Math.max(0, workoutData.value.recoveryState + (Math.random() * 4 - 2))),
          trainingEffectiveness: ['optimal', 'good', 'moderate', 'poor'][Math.floor(Math.random() * 4)],
          timeToExhaustion: `${Math.floor(Math.random() * 10)}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
          recommendations: [
            {
              type: 'adjustment',
              text: 'Увеличьте темп на 5% для оптимизации тренировки'
            },
            {
              type: 'tip',
              text: 'Следите за дыханием - вдох на 3 шага, выдох на 2'
            }
          ]
        }
        
        store.dispatch('updateWorkoutData', newData)
        
        // Provide audio feedback occasionally
        if (audioAssistant.value && Math.random() > 0.7) {
          audioAssistant.value.provideWorkoutUpdate({
            load: Math.round(newData.currentLoad),
            fatigue: fatigueLevelText.value
          })
        }
      }, 3000)
    }
    
    // Cleanup on unmount
    onUnmounted(() => {
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }
    })
    
    // Initialize on mount
    onMounted(() => {
      simulateDataUpdates()
    })
    
    return {
      isSessionActive,
      sessionId,
      elapsedTime,
      formattedTime,
      distance,
      speed,
      workoutData,
      elements,
      fatigueLevelText,
      audioAssistant,
      buttonLabel,
      buttonClass,
      progressOffset,
      toggleWorkout,
      startWorkout,
      endWorkout,
      sendElement,
      handleSendElement
    }
  }
}
</script>

<style scoped>
.training-screen {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 20px;
}

/* Training Stats (Height reduced by 30%) */
.training-stats {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
  /* Height reduced by 30% */
  height: 70px; /* instead of 100px */
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  margin-bottom: 5px;
}

.stat-value {
  color: white;
  font-size: 16px;
  font-weight: bold;
}

/* Workout Button */
.workout-button-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.workout-button {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: none;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 191, 255, 0.5);
  transition: all 0.3s ease;
}

.workout-button:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 30px rgba(0, 191, 255, 0.7);
}

.workout-button:active {
  transform: scale(0.95);
}

.start-button {
  background: linear-gradient(45deg, #00BFFF, #1E90FF);
}

.stop-button {
  background: linear-gradient(45deg, #FF4500, #FF0000);
}

.circular-progress {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.progress-background {
  fill: none;
  stroke: rgba(255, 255, 255, 0.2);
  stroke-width: 8;
}

.progress-indicator {
  fill: none;
  stroke: white;
  stroke-width: 8;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  stroke-dasharray: 339.292;
  stroke-dashoffset: 339.292;
  transition: stroke-dashoffset 1s linear;
}

.button-label {
  position: relative;
  z-index: 1;
  color: white;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

/* Workout Details */
.workout-details {
  padding: 20px;
  border-radius: 15px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  opacity: 0.8;
}

.detail-value {
  font-weight: bold;
  color: #00BFFF;
}

/* Recommendations */
.recommendations {
  padding: 20px;
  border-radius: 15px;
}

/* Добавляем стили для кнопки отправки элемента */
.send-element-container {
  margin-top: 20px;
  text-align: center;
}

.send-element-button {
  background: linear-gradient(45deg, #32CD32, #228B22);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(50, 205, 50, 0.3);
}

.send-element-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(50, 205, 50, 0.4);
}

.send-element-button:active {
  transform: translateY(0);
}

/* Добавляем стили для панели элементов */
.elements-panel {
  padding: 20px;
  border-radius: 15px;
}

.elements-panel h3 {
  color: #32CD32;
  margin-top: 0;
  margin-bottom: 15px;
}

.elements-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.element-item {
  padding: 10px;
  background: rgba(50, 205, 50, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(50, 205, 50, 0.3);
}

.element-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.element-type {
  font-weight: bold;
  color: #32CD32;
}

.element-time {
  font-size: 0.9em;
  color: rgba(255, 255, 255, 0.7);
}

.recommendations h3 {
  color: #00BFFF;
  margin-top: 0;
  margin-bottom: 15px;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.rec-icon {
  font-size: 1.5rem;
}

.rec-text {
  flex: 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .training-screen {
    padding: 10px;
  }
  
  .training-stats {
    padding: 10px;
    height: 60px; /* Further reduced height for mobile */
  }
  
  .stat-label {
    font-size: 10px;
  }
  
  .stat-value {
    font-size: 14px;
  }
  
  .workout-button {
    width: 100px;
    height: 100px;
  }
  
  .detail-item {
    flex-direction: column;
    gap: 5px;
  }
  
  .recommendation-item {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .training-stats {
    flex-direction: column;
    gap: 10px;
    height: auto;
    text-align: center;
  }
  
  .stat-item {
    gap: 5px;
  }
}
</style>