<template>
  <div class="workout-view">
    <div class="workout-header">
      <h1>Тренировка</h1>
      <button 
        v-if="isSessionActive" 
        @click="endWorkout" 
        class="btn btn-secondary"
      >
        Завершить тренировку
      </button>
    </div>
    
    <div class="workout-content">
      <!-- Workout Controls -->
      <div class="card glass-effect workout-controls">
        <h2>Управление тренировкой</h2>
        <div class="controls">
          <button 
            v-if="!isSessionActive" 
            @click="startWorkout" 
            class="btn btn-primary"
          >
            Начать тренировку
          </button>
          <div v-else class="session-info">
            <div class="timer">{{ formattedTime }}</div>
            <div class="session-id">ID: {{ sessionId }}</div>
          </div>
        </div>
      </div>
      
      <!-- Real-time Workout Data -->
      <div class="card glass-effect workout-data" v-if="isSessionActive">
        <h2>Данные тренировки</h2>
        <div class="data-grid">
          <div class="data-item">
            <div class="data-label">Текущая нагрузка</div>
            <div class="data-value">{{ workoutData.currentLoad }}%</div>
          </div>
          <div class="data-item">
            <div class="data-label">Уровень усталости</div>
            <div class="data-value">{{ fatigueLevelText }}</div>
          </div>
          <div class="data-item">
            <div class="data-label">Состояние восстановления</div>
            <div class="data-value">{{ workoutData.recoveryState }}%</div>
          </div>
          <div class="data-item">
            <div class="data-label">Эффективность тренировки</div>
            <div class="data-value">{{ effectivenessText }}</div>
          </div>
          <div class="data-item">
            <div class="data-label">Время до изнеможения</div>
            <div class="data-value">{{ workoutData.timeToExhaustion }}</div>
          </div>
        </div>
      </div>
      
      <!-- Workout Chart -->
      <div class="card glass-effect workout-chart" v-if="isSessionActive">
        <h2>График нагрузки</h2>
        <canvas ref="workoutChart"></canvas>
      </div>
      
      <!-- AI Recommendations -->
      <div class="card glass-effect recommendations" v-if="workoutData.recommendations.length > 0">
        <h2>Рекомендации ИИ</h2>
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
    </div>
    
    <!-- Audio Assistant -->
    <AudioAssistant ref="audioAssistant" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto'
import api from '../services/api.js'
import AudioAssistant from '../components/AudioAssistant.vue'

export default {
  name: 'Workout',
  components: {
    AudioAssistant
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const workoutChart = ref(null)
    const chartInstance = ref(null)
    const audioAssistant = ref(null)
    
    // Workout state
    const isSessionActive = ref(false)
    const sessionId = ref('')
    const startTime = ref(null)
    const timerInterval = ref(null)
    const elapsedTime = ref(0)
    
    // Workout data
    const workoutData = computed(() => store.state.workoutData)
    const userProfile = computed(() => store.state.userProfile)
    
    // Computed properties for text display
    const fatigueLevelText = computed(() => {
      const levels = {
        'low': 'Низкий',
        'medium': 'Средний',
        'high': 'Высокий'
      }
      return levels[workoutData.value.fatigueLevel] || workoutData.value.fatigueLevel
    })
    
    const effectivenessText = computed(() => {
      const levels = {
        'optimal': 'Оптимальная',
        'good': 'Хорошая',
        'moderate': 'Умеренная',
        'poor': 'Низкая'
      }
      return levels[workoutData.value.trainingEffectiveness] || workoutData.value.trainingEffectiveness
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
    
    // Start workout session
    const startWorkout = async () => {
      try {
        const sessionData = {
          user_id: userProfile.value.user_id,
          start_time: new Date().toISOString(),
          user_profile: userProfile.value
        }
        
        const response = await api.startWorkoutSession(sessionData)
        sessionId.value = response.data.session_id
        isSessionActive.value = true
        startTime.value = Date.now()
        elapsedTime.value = 0
        
        // Start timer
        timerInterval.value = setInterval(() => {
          elapsedTime.value = Math.floor((Date.now() - startTime.value) / 1000)
        }, 1000)
        
        // Initialize chart
        initChart()
        
        // Store session in Vuex
        store.dispatch('startWorkoutSession', response.data)
        
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
        const sessionData = {
          session_id: sessionId.value,
          end_time: new Date().toISOString(),
          duration_seconds: elapsedTime.value
        }
        
        await api.endWorkoutSession(sessionData)
        
        // Clean up
        isSessionActive.value = false
        if (timerInterval.value) {
          clearInterval(timerInterval.value)
        }
        
        // Destroy chart
        if (chartInstance.value) {
          chartInstance.value.destroy()
        }
        
        // Redirect to dashboard
        router.push('/dashboard')
      } catch (error) {
        console.error('Error ending workout session:', error)
      }
    }
    
    // Initialize chart
    const initChart = () => {
      if (!workoutChart.value) return
      
      const ctx = workoutChart.value.getContext('2d')
      
      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({length: 60}, (_, i) => i + 1),
          datasets: [{
            label: 'Нагрузка (%)',
            data: Array(60).fill(0),
            borderColor: '#00BFFF',
            backgroundColor: 'rgba(0, 191, 255, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              min: 0,
              max: 100,
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: 'rgba(255, 255, 255, 0.7)'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: 'white'
              }
            }
          }
        }
      })
      
      // Update chart with real data periodically
      setInterval(updateChart, 1000)
    }
    
    // Update chart with new data
    const updateChart = () => {
      if (!chartInstance.value) return
      
      const chart = chartInstance.value
      const data = chart.data.datasets[0].data
      
      // Remove first data point and add new one
      data.shift()
      data.push(workoutData.value.currentLoad)
      
      chart.update()
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
      if (chartInstance.value) {
        chartInstance.value.destroy()
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
      workoutData,
      fatigueLevelText,
      effectivenessText,
      workoutChart,
      audioAssistant,
      startWorkout,
      endWorkout
    }
  }
}
</script>

<style scoped>
.workout-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.workout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.workout-header h1 {
  margin-bottom: 0;
}

.workout-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workout-controls .controls {
  text-align: center;
  padding: 20px 0;
}

.session-info {
  text-align: center;
}

.timer {
  font-size: 2.5rem;
  font-weight: bold;
  color: #00BFFF;
  margin-bottom: 10px;
}

.session-id {
  opacity: 0.7;
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.data-item {
  text-align: center;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.data-label {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 5px;
}

.data-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #00BFFF;
}

.workout-chart {
  height: 300px;
  padding: 20px;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
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

@media (max-width: 768px) {
  .workout-view {
    padding: 15px;
  }
  
  .workout-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .data-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .workout-chart {
    height: 250px;
  }
  
  .recommendation-item {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .workout-view {
    padding: 10px;
  }
  
  .workout-header h1 {
    font-size: 1.5rem;
  }
  
  .data-grid {
    grid-template-columns: 1fr;
  }
  
  .workout-chart {
    height: 200px;
  }
  
  .timer {
    font-size: 2rem;
  }
}
</style>