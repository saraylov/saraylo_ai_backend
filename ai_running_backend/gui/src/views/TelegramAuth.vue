<template>
  <div class="auth-container">
    <div class="auth-card glass-panel">
      <div class="auth-header">
        <h1 class="app-title">SARAYLO</h1>
        <h2 class="auth-title">Добро пожаловать</h2>
        <p class="auth-subtitle">Ваш персональный квантовый беговой тренер</p>
      </div>
      
      <div class="auth-content">
        <div class="telegram-auth-section">
          <p class="auth-instruction">Войдите через Telegram для начала работы:</p>
          <div class="telegram-widget-container" ref="telegramContainer"></div>
        </div>
        
        <div class="auth-divider">
          <span>или</span>
        </div>
        
        <div class="alternative-auth">
          <button class="btn btn-secondary" @click="$router.push('/login')">
            Войти с помощью API ключа
          </button>
          <button class="btn btn-demo" @click="demoLogin">
            Демо-режим
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'TelegramAuth',
  mounted() {
    this.initTelegramWidget();
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
    
    async demoLogin() {
      // Демо вход без проверки API ключа
      try {
        await this.login({ 
          id: 'demo_user', 
          isDemo: true,
          isAuthenticated: true
        });
        localStorage.setItem('access_token', 'demo_token');
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Demo login error:', error);
      }
    }
  }
}

// Telegram auth function - must be in global scope
window.onTelegramAuth = async function(user) {
  // Handle Telegram authentication
  console.log('Telegram user:', user);
  
  try {
    // In a real implementation, you would send the user data to your backend
    // for verification and receive an authentication token
    
    // For now, we'll store user data and navigate to dashboard
    localStorage.setItem('telegram_user', JSON.stringify(user));
    localStorage.setItem('access_token', 'telegram_token');
    
    // Update Vuex store
    // Note: We can't directly access Vuex store from global scope
    // So we'll redirect and let the app handle the store update
    
    // Redirect to dashboard
    window.location.hash = '#/dashboard';
    window.location.reload();
  } catch (error) {
    console.error('Telegram auth error:', error);
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #000033, #33001a);
}

.auth-card {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  text-align: center;
}

.auth-header {
  margin-bottom: 30px;
}

.app-title {
  color: #00BFFF;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
}

.auth-title {
  font-size: 1.8rem;
  margin-bottom: 15px;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.auth-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 30px;
}

.auth-content {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.telegram-auth-section {
  margin: 20px 0;
}

.auth-instruction {
  margin-bottom: 20px;
  font-size: 1.1rem;
  opacity: 0.9;
}

.telegram-widget-container {
  display: flex;
  justify-content: center;
  margin: 15px 0;
  min-height: 50px;
}

.auth-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.auth-divider::before,
.auth-divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.auth-divider span {
  padding: 0 15px;
  opacity: 0.7;
}

.alternative-auth {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.btn {
  padding: 15px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-demo {
  background: linear-gradient(45deg, #FF1493, #FF69B4);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.btn:active {
  transform: translateY(0);
}

@media (max-width: 480px) {
  .auth-card {
    padding: 30px 20px;
  }
  
  .app-title {
    font-size: 2rem;
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
}
</style>