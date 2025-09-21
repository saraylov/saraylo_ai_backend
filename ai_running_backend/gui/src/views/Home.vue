<template>
  <div class="home">
    <div class="hero-section glass-effect">
      <h1>SARAYLO - Квантовый Беговой Тренер</h1>
      <p>Интеллектуальная система тренировок на основе нейронной сети</p>
      <div class="cta-buttons">
        <router-link to="/login" class="btn btn-primary" v-if="!isAuthenticated">
          Начать тренировку
        </router-link>
        <router-link to="/dashboard" class="btn btn-primary" v-else>
          Перейти к тренировкам
        </router-link>
      </div>
    </div>

    <div class="features-section">
      <h2>Основные возможности</h2>
      <div class="features-grid">
        <div class="feature-card glass-effect">
          <div class="feature-icon">🏃</div>
          <h3>Адаптивные тренировки</h3>
          <p>Нейросеть анализирует ваше физиологическое состояние в реальном времени и адаптирует тренировку под ваши потребности.</p>
        </div>
        <div class="feature-card glass-effect">
          <div class="feature-icon">🎯</div>
          <h3>Персональные рекомендации</h3>
          <p>Получайте индивидуальные рекомендации по интенсивности, темпу и восстановлению на основе ваших биометрических данных.</p>
        </div>
        <div class="feature-card glass-effect">
          <div class="feature-icon">📊</div>
          <h3>Интеллектуальный мониторинг</h3>
          <p>Система отслеживает уровень усталости, восстановление и эффективность тренировки для оптимизации результатов.</p>
        </div>
        <div class="feature-card glass-effect">
          <div class="feature-icon">🔊</div>
          <h3>Аудио-взаимодействие</h3>
          <p>Уточняйте цели и получайте мотивацию через голосовое взаимодействие с ИИ-тренером.</p>
        </div>
        <div class="feature-card glass-effect">
          <div class="feature-icon">🍎</div>
          <h3>Питание и восстановление</h3>
          <p>Персональные рекомендации по питанию и восстановлению на основе данных тренировок и целей.</p>
        </div>
        <div class="feature-card glass-effect">
          <div class="feature-icon">📈</div>
          <h3>Прогресс и аналитика</h3>
          <p>Подробная аналитика прогресса с прогнозами и достижениями для мотивации.</p>
        </div>
      </div>
    </div>

    <div class="how-it-works">
      <h2>Как это работает</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Калибровка</h3>
          <p>Пройдите оценочную тренировку для определения ваших персональных зон интенсивности.</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>Тренировка</h3>
          <p>Носите устройство с датчиками ЧСС и GPS во время тренировки.</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>Анализ</h3>
          <p>Нейросеть анализирует данные и предоставляет персональные рекомендации.</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>Оптимизация</h3>
          <p>Следующая тренировка адаптируется на основе полученных данных.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapGetters(['isAuthenticated'])
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0.9;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  margin-top: 30px;
}

.btn-primary {
  font-size: 1.1rem;
  padding: 15px 30px;
}

.features-section {
  margin-bottom: 50px;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 30px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.feature-card {
  padding: 25px;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.feature-card h3 {
  margin-bottom: 15px;
  color: #00BFFF;
}

.how-it-works {
  margin-bottom: 50px;
}

.how-it-works h2 {
  text-align: center;
  margin-bottom: 30px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.step {
  text-align: center;
}

.step-number {
  width: 50px;
  height: 50px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 20px;
  color: white;
}

.step h3 {
  margin-bottom: 15px;
  color: #00BFFF;
}

@media (max-width: 768px) {
  .home {
    padding: 15px;
  }
  
  .hero-section {
    padding: 40px 15px;
  }
  
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .hero-section p {
    font-size: 1rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .steps {
    grid-template-columns: 1fr;
  }
  
  .feature-card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 10px;
  }
  
  .hero-section h1 {
    font-size: 1.8rem;
  }
  
  .hero-section p {
    font-size: 0.9rem;
  }
  
  .btn-primary {
    font-size: 1rem;
    padding: 12px 24px;
  }
  
  .features-grid {
    gap: 15px;
  }
  
  .feature-card {
    padding: 15px;
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
}
</style>