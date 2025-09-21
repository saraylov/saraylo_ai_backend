<template>
  <div class="dashboard-screen">
    <div class="auth-options">
      <div class="auth-buttons">
        <button class="auth-button telegram-auth-button" @click="$router.push('/telegram-auth')">
          Войти через Telegram
        </button>
        <button class="auth-button demo-auth-button" @click="demoLogin">
          Демо-режим
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['login']),
    demoLogin() {
      // Демо вход без проверки API ключа
      localStorage.setItem('access_token', 'demo_token')
      this.login({ 
        id: 'demo_user', 
        isDemo: true,
        isAuthenticated: true
      })
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
.dashboard-screen {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 300px;
  margin: 0 auto;
}

.auth-button {
  padding: 15px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.telegram-auth-button {
  background: linear-gradient(45deg, #0088cc, #00aaff);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 136, 204, 0.4);
}

.demo-auth-button {
  background: linear-gradient(45deg, #FF1493, #FF69B4);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4);
}

.auth-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.auth-button:active {
  transform: translateY(0);
}
</style>