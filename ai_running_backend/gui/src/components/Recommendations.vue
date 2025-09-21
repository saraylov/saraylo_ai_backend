<template>
  <div class="recommendations">
    <div class="recommendations-header">
      <h3>Персональные рекомендации</h3>
      <div class="refresh-controls">
        <button @click="refreshRecommendations" class="btn btn-secondary btn-sm">
          Обновить
        </button>
      </div>
    </div>
    
    <div class="recommendations-content">
      <!-- Рекомендации по тренировке -->
      <div class="recommendation-section" v-if="workoutRecommendations.length > 0">
        <h4>Тренировка</h4>
        <div class="recommendations-list">
          <div 
            v-for="(rec, index) in workoutRecommendations" 
            :key="index" 
            class="recommendation-item glass-effect"
          >
            <div class="rec-priority">{{ rec.priority }}</div>
            <div class="rec-content">
              <div class="rec-text">{{ rec.text }}</div>
              <div class="rec-actions" v-if="rec.actions">
                <button 
                  v-for="(action, actionIndex) in rec.actions" 
                  :key="actionIndex"
                  @click="executeAction(action)"
                  class="btn btn-secondary btn-sm"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Рекомендации по восстановлению -->
      <div class="recommendation-section" v-if="recoveryRecommendations.length > 0">
        <h4>Восстановление</h4>
        <div class="recommendations-list">
          <div 
            v-for="(rec, index) in recoveryRecommendations" 
            :key="index" 
            class="recommendation-item glass-effect"
          >
            <div class="rec-icon">
              <span v-if="rec.type === 'rest'">💤</span>
              <span v-else-if="rec.type === 'sleep'">😴</span>
              <span v-else-if="rec.type === 'nutrition'">🍎</span>
              <span v-else>💡</span>
            </div>
            <div class="rec-content">
              <div class="rec-text">{{ rec.text }}</div>
              <div class="rec-meta">
                <span class="rec-urgency" :class="rec.urgency">{{ getUrgencyText(rec.urgency) }}</span>
                <span class="rec-timing">{{ rec.timing }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Рекомендации по прогрессу -->
      <div class="recommendation-section" v-if="progressRecommendations.length > 0">
        <h4>Прогресс</h4>
        <div class="recommendations-list">
          <div 
            v-for="(rec, index) in progressRecommendations" 
            :key="index" 
            class="recommendation-item glass-effect"
          >
            <div class="rec-icon">📈</div>
            <div class="rec-content">
              <div class="rec-text">{{ rec.text }}</div>
              <div class="rec-meta">
                <span class="rec-impact">{{ getImpactText(rec.impact) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Сообщение, если нет рекомендаций -->
      <div class="no-recommendations" v-if="allRecommendations.length === 0">
        <p>На данный момент нет персональных рекомендаций. Продолжайте тренироваться, и система ИИ предоставит персональные советы.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Recommendations',
  data() {
    return {
      workoutRecommendations: [
        {
          priority: 1,
          text: 'Снизьте темп на 10% — вы в зоне перенагрузки',
          actions: [
            { label: 'Снизить темп', action: 'reduce_pace' },
            { label: 'Перейти в зону аэробного порога', action: 'aerobic_threshold' }
          ]
        },
        {
          priority: 2,
          text: 'Поддерживайте текущий ритм — анаэробный порог достигнут',
          actions: [
            { label: 'Сохранить темп', action: 'maintain_pace' }
          ]
        }
      ],
      recoveryRecommendations: [
        {
          type: 'rest',
          text: 'Отдохните минимум 24 часа перед следующей интенсивной тренировкой',
          urgency: 'high',
          timing: 'Сейчас'
        },
        {
          type: 'sleep',
          text: 'Увеличьте продолжительность сна до 8 часов для лучшего восстановления',
          urgency: 'medium',
          timing: 'Сегодня вечером'
        },
        {
          type: 'nutrition',
          text: 'Увеличьте потребление белка до 1.6 г на кг веса тела',
          urgency: 'low',
          timing: 'На следующий прием пищи'
        }
      ],
      progressRecommendations: [
        {
          text: 'Ваша выносливость улучшилась на 12% за последние 2 недели',
          impact: 'positive'
        },
        {
          text: 'Следующая цель: увеличить среднюю дистанцию на 10%',
          impact: 'goal'
        }
      ]
    }
  },
  computed: {
    ...mapGetters(['workoutData']),
    allRecommendations() {
      return [
        ...this.workoutRecommendations,
        ...this.recoveryRecommendations,
        ...this.progressRecommendations
      ]
    }
  },
  methods: {
    refreshRecommendations() {
      // В реальной системе здесь будет API вызов для получения новых рекомендаций
      // от нейросетевой системы
      console.log('Refreshing recommendations from AI system')
      
      // Симулируем обновление рекомендаций
      this.workoutRecommendations = [
        ...this.workoutRecommendations,
        {
          priority: 3,
          text: 'Увеличьте каденс до 180 шагов в минуту для лучшей эффективности',
          actions: [
            { label: 'Увеличить каденс', action: 'increase_cadence' }
          ]
        }
      ]
    },
    executeAction(action) {
      // В реальной системе здесь будет обработка действий пользователя
      console.log('Executing action:', action)
      
      // Показываем уведомление
      alert(`Выполняется действие: ${action.label}`)
    },
    getUrgencyText(urgency) {
      const urgencyMap = {
        'high': 'Срочно',
        'medium': 'Средний приоритет',
        'low': 'Низкий приоритет'
      }
      return urgencyMap[urgency] || urgency
    },
    getImpactText(impact) {
      const impactMap = {
        'positive': 'Позитивное влияние',
        'negative': 'Отрицательное влияние',
        'goal': 'Цель'
      }
      return impactMap[impact] || impact
    }
  }
}
</script>

<style scoped>
.recommendations {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  margin-bottom: 20px;
}

.recommendations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.recommendations-header h3 {
  margin-bottom: 0;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.9rem;
}

.recommendation-section {
  margin-bottom: 25px;
}

.recommendation-section h4 {
  margin-bottom: 15px;
  color: #00BFFF;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  border-radius: 8px;
}

.rec-priority {
  width: 25px;
  height: 25px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
  margin-right: 15px;
  flex-shrink: 0;
}

.rec-icon {
  font-size: 1.5rem;
  margin-right: 15px;
  flex-shrink: 0;
}

.rec-content {
  flex: 1;
}

.rec-text {
  margin-bottom: 10px;
}

.rec-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.rec-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.rec-urgency.high {
  color: #ff6b6b;
  font-weight: bold;
}

.rec-urgency.medium {
  color: #ffc107;
}

.rec-urgency.low {
  color: #6c757d;
}

.rec-impact.positive {
  color: #28a745;
}

.rec-impact.negative {
  color: #ff6b6b;
}

.rec-impact.goal {
  color: #00BFFF;
}

.no-recommendations {
  text-align: center;
  padding: 30px;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .recommendation-item {
    flex-direction: column;
  }
  
  .rec-priority, .rec-icon {
    margin-bottom: 10px;
  }
  
  .rec-actions {
    margin-top: 10px;
  }
  
  .rec-meta {
    flex-direction: column;
    gap: 5px;
  }
}
</style>