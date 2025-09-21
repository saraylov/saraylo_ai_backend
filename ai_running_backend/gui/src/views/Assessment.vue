<template>
  <div class="assessment">
    <div class="assessment-header">
      <h1>Оценочная тренировка</h1>
      <button @click="goBack" class="btn btn-secondary">Назад</button>
    </div>
    
    <div class="assessment-content">
      <!-- Инструкции по оценочной тренировке -->
      <div class="instructions glass-effect">
        <h2>Инструкции</h2>
        <p>Оценочная тренировка поможет определить ваши персональные зоны интенсивности. Следуйте инструкциям аудио-ассистента и двигайтесь в заданном темпе.</p>
        <div class="zones-info">
          <div class="zone-item blue">
            <div class="zone-color"></div>
            <div class="zone-name">Синяя зона</div>
            <div class="zone-description">Подготовка (6 минут)</div>
          </div>
          <div class="zone-item green">
            <div class="zone-color"></div>
            <div class="zone-name">Зеленая зона</div>
            <div class="zone-description">Легкая нагрузка (5 минут)</div>
          </div>
          <div class="zone-item yellow">
            <div class="zone-color"></div>
            <div class="zone-name">Желтая зона</div>
            <div class="zone-description">Умеренная нагрузка (5 минут)</div>
          </div>
          <div class="zone-item orange">
            <div class="zone-color"></div>
            <div class="zone-name">Оранжевая зона</div>
            <div class="zone-description">Высокая нагрузка (3 минуты)</div>
          </div>
          <div class="zone-item red">
            <div class="zone-color"></div>
            <div class="zone-name">Красная зона</div>
            <div class="zone-description">Максимальная нагрузка (1 минута)</div>
          </div>
        </div>
      </div>
      
      <!-- Панель управления оценочной тренировкой -->
      <div class="assessment-controls glass-effect">
        <div class="current-phase">
          <div class="phase-name">{{ currentPhase.name }}</div>
          <div class="phase-description">{{ currentPhase.description }}</div>
          <div class="phase-timer">{{ formatTime(phaseTimeLeft) }}</div>
        </div>
        
        <div class="control-buttons">
          <button 
            v-if="assessmentState === 'not_started'" 
            @click="startAssessment" 
            class="btn btn-primary"
          >
            Начать оценку
          </button>
          
          <button 
            v-else-if="assessmentState === 'in_progress'" 
            @click="pauseAssessment" 
            class="btn btn-warning"
          >
            Пауза
          </button>
          
          <button 
            v-else-if="assessmentState === 'paused'" 
            @click="resumeAssessment" 
            class="btn btn-success"
          >
            Продолжить
          </button>
          
          <button 
            v-if="assessmentState === 'in_progress' || assessmentState === 'paused'" 
            @click="stopAssessment" 
            class="btn btn-danger"
          >
            Завершить
          </button>
        </div>
      </div>
      
      <!-- Прогресс оценочной тренировки -->
      <div class="assessment-progress glass-effect">
        <h2>Прогресс</h2>
        <div class="progress-steps">
          <div 
            v-for="(phase, index) in assessmentPhases" 
            :key="index"
            class="progress-step"
            :class="{ 
              'completed': index < currentPhaseIndex,
              'active': index === currentPhaseIndex,
              'pending': index > currentPhaseIndex
            }"
          >
            <div class="step-zone" :class="phase.zone"></div>
            <div class="step-name">{{ phase.name }}</div>
            <div class="step-duration">{{ phase.duration }} мин</div>
          </div>
        </div>
      </div>
      
      <!-- Статистика оценочной тренировки -->
      <div class="assessment-stats glass-effect">
        <h2>Статистика</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-label">Пройдено времени</div>
            <div class="stat-value">{{ formatTime(totalElapsedTime) }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Средняя скорость</div>
            <div class="stat-value">{{ averageSpeed.toFixed(1) }} км/ч</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Максимальная скорость</div>
            <div class="stat-value">{{ maxSpeed.toFixed(1) }} км/ч</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Средний пульс</div>
            <div class="stat-value">{{ averageHR.toFixed(0) }} уд/мин</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Assessment',
  data() {
    return {
      assessmentState: 'not_started', // not_started, in_progress, paused, completed
      assessmentPhases: [
        {
          name: 'Подготовка',
          description: 'Разминка в синей зоне',
          zone: 'blue',
          duration: 6 // минуты
        },
        {
          name: 'Легкая нагрузка',
          description: 'Движение в зеленой зоне',
          zone: 'green',
          duration: 5
        },
        {
          name: 'Умеренная нагрузка',
          description: 'Движение в желтой зоне',
          zone: 'yellow',
          duration: 5
        },
        {
          name: 'Высокая нагрузка',
          description: 'Движение в оранжевой зоне',
          zone: 'orange',
          duration: 3
        },
        {
          name: 'Максимальная нагрузка',
          description: 'Максимальные усилия в красной зоне',
          zone: 'red',
          duration: 1
        }
      ],
      currentPhaseIndex: 0,
      phaseStartTime: 0,
      phaseTimeLeft: 0,
      totalElapsedTime: 0,
      averageSpeed: 0,
      maxSpeed: 0,
      averageHR: 0,
      speedData: [],
      hrData: [],
      assessmentInterval: null
    }
  },
  computed: {
    currentPhase() {
      return this.assessmentPhases[this.currentPhaseIndex] || {}
    }
  },
  methods: {
    goBack() {
      this.$router.push('/dashboard')
    },
    startAssessment() {
      this.assessmentState = 'in_progress'
      this.currentPhaseIndex = 0
      this.startPhase()
      this.startAssessmentTimer()
    },
    pauseAssessment() {
      this.assessmentState = 'paused'
      if (this.assessmentInterval) {
        clearInterval(this.assessmentInterval)
        this.assessmentInterval = null
      }
    },
    resumeAssessment() {
      this.assessmentState = 'in_progress'
      this.startAssessmentTimer()
    },
    stopAssessment() {
      this.assessmentState = 'not_started'
      if (this.assessmentInterval) {
        clearInterval(this.assessmentInterval)
        this.assessmentInterval = null
      }
      this.resetAssessment()
    },
    startPhase() {
      const phase = this.assessmentPhases[this.currentPhaseIndex]
      this.phaseTimeLeft = phase.duration * 60 * 1000 // Переводим в миллисекунды
      this.phaseStartTime = Date.now()
    },
    startAssessmentTimer() {
      // Останавливаем предыдущий таймер, если есть
      if (this.assessmentInterval) {
        clearInterval(this.assessmentInterval)
      }
      
      // Начинаем таймер обновлений
      this.assessmentInterval = setInterval(() => {
        if (this.assessmentState === 'in_progress') {
          this.updateAssessment()
        }
      }, 1000)
    },
    updateAssessment() {
      // Обновляем таймер фазы
      const elapsed = Date.now() - this.phaseStartTime
      this.phaseTimeLeft = Math.max(0, (this.assessmentPhases[this.currentPhaseIndex].duration * 60 * 1000) - elapsed)
      
      // Обновляем общий таймер
      this.totalElapsedTime += 1000
      
      // Генерируем демонстрационные данные
      this.generateDemoData()
      
      // Проверяем завершение фазы
      if (this.phaseTimeLeft <= 0) {
        this.nextPhase()
      }
    },
    nextPhase() {
      // Переходим к следующей фазе
      if (this.currentPhaseIndex < this.assessmentPhases.length - 1) {
        this.currentPhaseIndex++
        this.startPhase()
      } else {
        // Оценочная тренировка завершена
        this.assessmentState = 'completed'
        if (this.assessmentInterval) {
          clearInterval(this.assessmentInterval)
          this.assessmentInterval = null
        }
        this.calculateCalibrationData()
      }
    },
    generateDemoData() {
      // Генерируем демонстрационные данные для симуляции оценочной тренировки
      const phase = this.assessmentPhases[this.currentPhaseIndex]
      let speed = 0
      let hr = 0
      
      // Определяем скорость и пульс в зависимости от зоны
      switch (phase.zone) {
        case 'blue': // Подготовка
          speed = 6 + Math.random() * 1
          hr = 100 + Math.random() * 10
          break
        case 'green': // Легкая нагрузка
          speed = 8 + Math.random() * 1
          hr = 120 + Math.random() * 10
          break
        case 'yellow': // Умеренная нагрузка
          speed = 10 + Math.random() * 1
          hr = 140 + Math.random() * 10
          break
        case 'orange': // Высокая нагрузка
          speed = 12 + Math.random() * 1
          hr = 160 + Math.random() * 10
          break
        case 'red': // Максимальная нагрузка
          speed = 14 + Math.random() * 1
          hr = 180 + Math.random() * 10
          break
      }
      
      // Добавляем немного случайного шума
      speed += (Math.random() - 0.5) * 0.5
      hr += (Math.random() - 0.5) * 5
      
      // Сохраняем данные
      this.speedData.push(speed)
      this.hrData.push(hr)
      
      // Обновляем статистику
      this.averageSpeed = this.speedData.reduce((a, b) => a + b, 0) / this.speedData.length
      this.maxSpeed = Math.max(...this.speedData, this.maxSpeed)
      this.averageHR = this.hrData.reduce((a, b) => a + b, 0) / this.hrData.length
    },
    calculateCalibrationData() {
      // В реальной системе здесь будет расчет калибровочных данных
      // на основе собранных данных скорости и пульса
      console.log('Calibration data calculated')
    },
    resetAssessment() {
      this.currentPhaseIndex = 0
      this.phaseTimeLeft = 0
      this.totalElapsedTime = 0
      this.averageSpeed = 0
      this.maxSpeed = 0
      this.averageHR = 0
      this.speedData = []
      this.hrData = []
    },
    formatTime(milliseconds) {
      const totalSeconds = Math.floor(milliseconds / 1000)
      const minutes = Math.floor(totalSeconds / 60)
      const seconds = totalSeconds % 60
      
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }
  },
  beforeUnmount() {
    // Очищаем интервал при уничтожении компонента
    if (this.assessmentInterval) {
      clearInterval(this.assessmentInterval)
    }
  }
}
</script>

<style scoped>
.assessment {
  padding: 20px;
}

.assessment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.assessment-header h1 {
  margin-bottom: 0;
}

.assessment-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 25px;
}

.instructions {
  padding: 25px;
}

.zones-info {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 20px;
}

.zone-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  flex: 1;
  min-width: 150px;
}

.zone-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 10px;
}

.zone-item.blue .zone-color {
  background: #1E90FF;
}

.zone-item.green .zone-color {
  background: #32CD32;
}

.zone-item.yellow .zone-color {
  background: #FFD700;
}

.zone-item.orange .zone-color {
  background: #FF8C00;
}

.zone-item.red .zone-color {
  background: #FF0000;
}

.zone-name {
  font-weight: bold;
  margin-right: 10px;
}

.assessment-controls {
  padding: 30px;
  text-align: center;
}

.current-phase {
  margin-bottom: 30px;
}

.phase-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.phase-description {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 20px;
}

.phase-timer {
  font-size: 2rem;
  font-weight: bold;
  font-family: 'Courier New', monospace;
}

.assessment-progress {
  padding: 25px;
}

.progress-steps {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 20px;
}

.progress-step {
  flex: 1;
  min-width: 120px;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
}

.progress-step.completed {
  background: rgba(50, 205, 50, 0.2);
}

.progress-step.active {
  background: rgba(0, 191, 255, 0.2);
  transform: scale(1.05);
}

.progress-step.pending {
  background: rgba(255, 255, 255, 0.05);
}

.step-zone {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin: 0 auto 10px;
}

.step-zone.blue {
  background: #1E90FF;
}

.step-zone.green {
  background: #32CD32;
}

.step-zone.yellow {
  background: #FFD700;
}

.step-zone.orange {
  background: #FF8C00;
}

.step-zone.red {
  background: #FF0000;
}

.assessment-stats {
  padding: 25px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
}

@media (max-width: 768px) {
  .zones-info {
    flex-direction: column;
  }
  
  .zone-item {
    min-width: 100%;
  }
  
  .progress-steps {
    flex-direction: column;
  }
  
  .progress-step {
    min-width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>