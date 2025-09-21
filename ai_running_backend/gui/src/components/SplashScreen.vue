<template>
  <div class="splash-screen" v-if="showSplash">
    <div class="logo-container">
      <!-- Логотип с анимацией -->
      <div class="logo-wrapper" :class="{ 'logo-animation': animateLogo }">
        <img src="/images/Smart.png" alt="SARAYLO Logo" class="logo" />
      </div>
      
      <!-- Название приложения -->
      <div class="app-name">Saraylo</div>
      
      <!-- Надпись "Добро пожаловать" -->
      <div class="welcome-text">Добро пожаловать</div>
      
      <!-- Прогресс-бар загрузки -->
      <div class="progress-container" v-if="showProgress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="progress-text">{{ Math.round(progress) }}%</div>
      </div>
    </div>
    
    <!-- Аудио элемент для звуковых эффектов -->
    <audio ref="splashSound" preload="auto">
      <source src="/sounds/splash.mp3" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
export default {
  name: 'SplashScreen',
  data() {
    return {
      showSplash: true,
      showProgress: true,
      progress: 0,
      animateLogo: false,
      resourcesLoaded: false,
      minDisplayTime: 5000, // Минимальное время отображения 5 секунд
      startTime: null
    }
  },
  async mounted() {
    this.startTime = Date.now();
    
    // Начинаем анимацию логотипа
    setTimeout(() => {
      this.animateLogo = true;
    }, 100);
    
    // Проигрываем звуковой эффект
    this.playSound();
    
    // Начинаем имитацию загрузки ресурсов
    this.simulateResourceLoading();
    
    // Предзагрузка ресурсов
    await this.preloadResources();
    
    // Устанавливаем прогресс в 100%
    this.progress = 100;
    
    // Проверяем, прошло ли минимальное время отображения
    this.checkMinDisplayTime();
  },
  methods: {
    playSound() {
      try {
        // В реальной реализации здесь будет воспроизведение звука
        // this.$refs.splashSound.play();
        console.log('Playing splash sound effect');
      } catch (error) {
        console.log('Sound playback failed:', error);
      }
    },
    
    simulateResourceLoading() {
      // Имитация загрузки ресурсов
      const interval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += Math.random() * 15;
          if (this.progress > 90) this.progress = 90;
        } else {
          clearInterval(interval);
        }
      }, 200);
    },
    
    async preloadResources() {
      // Предзагрузка критически важных ресурсов
      const resources = [
        '/images/home-icon.png',
        '/images/run-icon.png',
        '/images/device-icon.png',
        // Добавьте сюда другие важные ресурсы
      ];
      
      const promises = resources.map(src => {
        return new Promise((resolve, reject) => {
          const img = new Image();
          img.onload = resolve;
          img.onerror = reject;
          img.src = src;
        });
      });
      
      try {
        await Promise.all(promises);
        this.resourcesLoaded = true;
      } catch (error) {
        console.error('Resource loading failed:', error);
        this.resourcesLoaded = true; // Продолжаем даже при ошибке
      }
    },
    
    checkMinDisplayTime() {
      const elapsedTime = Date.now() - this.startTime;
      const remainingTime = this.minDisplayTime - elapsedTime;
      
      if (remainingTime <= 0) {
        // Минимальное время уже прошло, скрываем сплеш-скрин
        this.hideSplash();
      } else {
        // Ждем оставшееся время
        setTimeout(() => {
          this.hideSplash();
        }, remainingTime);
      }
    },
    
    hideSplash() {
      // Добавляем небольшую задержку перед скрытием для плавного перехода
      setTimeout(() => {
        this.showSplash = false;
        this.$emit('splash-finished');
      }, 300);
    }
  }
}
</script>

<style scoped>
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #000033, #33001a);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: fadeIn 0.5s ease-in-out;
}

.logo-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

/* Логотип */
.logo-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo {
  width: 200px;
  height: 200px;
  border: none;
  outline: none;
}

/* Название приложения */
.app-name {
  color: #00BFFF;
  font-family: 'Montserrat', sans-serif;
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  text-shadow: 0 0 15px rgba(0, 191, 255, 0.7);
  animation: glow 2s ease-in-out infinite alternate;
}

/* Надпись "Добро пожаловать" */
.welcome-text {
  color: white;
  font-family: 'Montserrat', sans-serif;
  font-size: 24px;
  font-weight: 500;
  text-align: center;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
  animation: fadeIn 1s ease-in-out;
}

/* Прогресс-бар */
.progress-container {
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00BFFF, #FF1493);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  color: white;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-weight: 500;
}

/* Анимации */
.logo-animation {
  animation: 
    pulse 2s infinite,
    rotate 20s linear infinite,
    float 3s ease-in-out infinite;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes glow {
  from {
    text-shadow: 0 0 5px rgba(0, 191, 255, 0.5);
  }
  to {
    text-shadow: 0 0 20px rgba(0, 191, 255, 0.8), 0 0 30px rgba(0, 191, 255, 0.6);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
    filter: brightness(1);
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
    filter: brightness(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
    filter: brightness(1);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

/* Адаптивность для мобильных устройств */
@media (max-width: 480px) {
  .logo {
    width: 150px;
    height: 150px;
  }
  
  .app-name {
    font-size: 28px;
  }
  
  .welcome-text {
    font-size: 20px;
  }
  
  .progress-container {
    width: 150px;
  }
}
</style>