<template>
  <div class="dashboard">
    <div class="user-info">
      <h1>Панель управления</h1>
      <div class="user-details" v-if="user">
        <span v-if="isTelegramUser" class="user-type telegram">Telegram пользователь</span>
        <span v-else-if="isDemoUser" class="user-type demo">Демо режим</span>
        <span v-else class="user-type api">API пользователь</span>
      </div>
    </div>
    
    <div class="stats-overview glass-panel">
      <h2>Обзор тренировок</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ workoutStats.totalWorkouts }}</div>
          <div class="stat-label">Всего тренировок</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ workoutStats.totalDistance }} км</div>
          <div class="stat-label">Пройдено</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ workoutStats.totalTime }} ч</div>
          <div class="stat-label">Время тренировок</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ workoutStats.avgLoad }}%</div>
          <div class="stat-label">Средняя нагрузка</div>
        </div>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2>Быстрые действия</h2>
      <div class="actions-grid">
        <div class="action-card glass-panel" @click="$router.push('/workout')">
          <h3>Начать тренировку</h3>
          <p>Запустить новую тренировку с мониторингом в реальном времени</p>
        </div>
        <div class="action-card glass-panel" @click="$router.push('/assessment')">
          <h3>Оценочная тренировка</h3>
          <p>Определить персональные зоны интенсивности</p>
        </div>
        <div class="action-card glass-panel" @click="$router.push('/profile')">
          <h3>Профиль</h3>
          <p>Настроить параметры пользователя и цели</p>
        </div>
        <div class="action-card glass-panel" @click="$router.push('/nutrition')">
          <h3>Питание</h3>
          <p>Получить персональные рекомендации по питанию</p>
        </div>
      </div>
    </div>
    
    <div class="recent-workouts" v-if="recentWorkouts.length > 0">
      <h2>Последние тренировки</h2>
      <div class="workouts-list">
        <div 
          v-for="workout in recentWorkouts" 
          :key="workout.id" 
          class="workout-item glass-panel"
        >
          <div class="workout-date">{{ formatDate(workout.date) }}</div>
          <div class="workout-details">
            <div class="workout-distance">{{ workout.distance }} км</div>
            <div class="workout-duration">{{ workout.duration }} мин</div>
            <div class="workout-load">{{ workout.load }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      workoutStats: {
        totalWorkouts: 12,
        totalDistance: 86.5,
        totalTime: 18.5,
        avgLoad: 68
      },
      recentWorkouts: [
        {
          id: 1,
          date: '2024-03-15T10:30:00Z',
          distance: 5.2,
          duration: 32,
          load: 72
        },
        {
          id: 2,
          date: '2024-03-12T08:15:00Z',
          distance: 10.1,
          duration: 65,
          load: 65
        },
        {
          id: 3,
          date: '2024-03-10T18:45:00Z',
          distance: 3.8,
          duration: 24,
          load: 80
        }
      ]
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isDemoUser', 'isTelegramUser', 'user'])
  },
  methods: {
    ...mapActions(['logout']),
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.user-info {
  margin-bottom: 30px;
}

.user-info h1 {
  margin-bottom: 10px;
}

.user-details {
  display: flex;
  gap: 10px;
}

.user-type {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.user-type.telegram {
  background: linear-gradient(45deg, #0088cc, #00aaff);
}

.user-type.demo {
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
}

.user-type.api {
  background: linear-gradient(45deg, #00BFFF, #FF1493);
}

.stats-overview {
  padding: 25px;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #00BFFF;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.8;
}

.quick-actions {
  margin-bottom: 30px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.action-card {
  padding: 25px;
  transition: transform 0.3s ease;
  color: white;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-5px);
}

.action-card h3 {
  color: #00BFFF;
  margin-bottom: 10px;
}

.recent-workouts h2 {
  margin-bottom: 20px;
}

.workouts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.workout-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.workout-date {
  font-weight: 500;
}

.workout-details {
  display: flex;
  gap: 30px;
}

.workout-distance, .workout-duration, .workout-load {
  min-width: 80px;
  text-align: center;
}

@media (max-width: 768px) {
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .workout-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .workout-details {
    width: 100%;
    justify-content: space-between;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .workout-details {
    flex-direction: column;
    gap: 10px;
  }
}
</style>