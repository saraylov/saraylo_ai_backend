<template>
  <div class="login-container">
    <div class="login-card glass-effect">
      <h2>Вход в систему</h2>
      
      <!-- Telegram Login Widget -->
      <div class="telegram-login">
        <p>Войти через Telegram:</p>
        <div class="telegram-widget-container" ref="telegramContainer"></div>
      </div>
      
      <!-- Removed API Key form -->
      
      <div class="demo-mode" v-if="!isAuthenticated">
        <p>Или попробуйте в демо-режиме:</p>
        <button @click="demoLogin" class="btn btn-secondary">
          Демо-режим
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '../services/api'

export default {
  name: 'Login',
  data() {
    return {
      error: ''
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  mounted() {
    // Clear any existing auth data when visiting login page
    if (this.isAuthenticated) {
      // If user is already authenticated, redirect to dashboard
      this.$router.push('/dashboard')
    }
    
    // Initialize Telegram Login Widget
    this.initTelegramWidget();
    
    // Проверяем, есть ли данные авторизации через Telegram в URL
    const urlParams = new URLSearchParams(window.location.search);
    const telegramAuth = urlParams.get('telegram_auth');
    
    if (telegramAuth) {
      try {
        const userData = JSON.parse(atob(telegramAuth));
        this.handleTelegramLogin(userData);
      } catch (e) {
        console.error('Ошибка обработки данных Telegram авторизации:', e);
      }
    }
    
    // Проверяем, есть ли данные авторизации через Telegram в хэше URL (после редиректа)
    if (window.location.hash) {
      try {
        const hashParams = new URLSearchParams(window.location.hash.substring(1));
        const telegramData = hashParams.get('telegram');
        
        if (telegramData) {
          const userData = JSON.parse(decodeURIComponent(telegramData));
          this.handleTelegramLoginWithApiKey(userData);
        }
      } catch (e) {
        console.error('Ошибка обработки данных Telegram авторизации из хэша:', e);
      }
    }
  },
  methods: {
    ...mapActions(['login']),
    
    initTelegramWidget() {
      // Create script element for Telegram Widget
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://telegram.org/js/telegram-widget.js?22';
      script.setAttribute('data-telegram-login', 'saraylov_bot');
      script.setAttribute('data-size', 'large');
      script.setAttribute('data-onauth', 'window.onTelegramAuth(user)');
      script.setAttribute('data-request-access', 'write');
      
      // Clear container and add script
      if (this.$refs.telegramContainer) {
        this.$refs.telegramContainer.innerHTML = '';
        this.$refs.telegramContainer.appendChild(script);
      }
    },
    
    demoLogin() {
      // Демо вход без проверки API ключа
      localStorage.setItem('access_token', 'demo_token')
      this.login({ 
        id: 'demo_user', 
        isDemo: true,
        isAuthenticated: true
      })
      this.$router.push('/dashboard')
    },
    
    async handleTelegramLoginWithApiKey(telegramData) {
      try {
        // Используем API ключ, полученный от сервера
        const apiKey = telegramData.api_key;
        
        if (!apiKey) {
          throw new Error('API ключ не предоставлен');
        }
        
        // Сохраняем API ключ в localStorage
        localStorage.setItem('api_key', apiKey);
        
        // Создаем токен на основе данных Telegram
        const token = btoa(JSON.stringify(telegramData));
        localStorage.setItem('access_token', token);
        
        // Обновляем состояние Vuex
        this.login({ 
          id: telegramData.id, 
          username: telegramData.username,
          firstName: telegramData.first_name,
          lastName: telegramData.last_name,
          isAuthenticated: true,
          isTelegramUser: true,
          apiKey: apiKey
        })
        
        // Перенаправляем на dashboard
        this.$router.push('/dashboard')
      } catch (err) {
        this.error = 'Ошибка авторизации через Telegram. Пожалуйста, попробуйте снова.'
        console.error('Telegram login error:', err)
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
}

.login-card h2 {
  text-align: center;
  margin-bottom: 30px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.telegram-login {
  text-align: center;
  margin-bottom: 25px;
}

.telegram-login p {
  margin-bottom: 15px;
  opacity: 0.9;
}

.telegram-widget-container {
  display: flex;
  justify-content: center;
  margin: 15px 0;
  min-height: 40px; /* Ensure space for widget */
}

.demo-mode {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.demo-mode p {
  margin-bottom: 15px;
  opacity: 0.8;
}

.btn-secondary {
  width: 100%;
  padding: 15px;
  margin-bottom: 15px;
  font-size: 1rem;
  font-weight: bold;
}

.error-message {
  color: #ff6b6b;
  text-align: center;
  margin-top: 15px;
  padding: 10px;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 5px;
  border: 1px solid rgba(255, 107, 107, 0.3);
}

@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 30px 20px;
  }
  
  .login-card h2 {
    font-size: 1.5rem;
  }
}
</style>