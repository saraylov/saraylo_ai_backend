<template>
  <div class="login-container">
    <div class="login-card glass-effect">
      <h2>Вход в систему</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="api_key" class="form-label">API Ключ</label>
          <input 
            type="password" 
            id="api_key" 
            v-model="apiKey" 
            class="form-input" 
            placeholder="Введите ваш API ключ"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
      
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
      apiKey: '',
      loading: false,
      error: ''
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      if (!this.apiKey.trim()) {
        this.error = 'Пожалуйста, введите API ключ'
        return
      }
      
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.login(this.apiKey)
        const token = response.data.access_token
        
        // Сохраняем токен в localStorage
        localStorage.setItem('access_token', token)
        
        // Обновляем состояние Vuex
        this.login({ 
          id: 'user123', 
          apiKey: this.apiKey,
          isAuthenticated: true
        })
        
        // Перенаправляем на dashboard
        this.$router.push('/dashboard')
      } catch (err) {
        this.error = 'Неверный API ключ. Пожалуйста, попробуйте снова.'
        console.error('Login error:', err)
      } finally {
        this.loading = false
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
    }
  },
  mounted() {
    // Clear any existing auth data when visiting login page
    if (this.isAuthenticated) {
      // If user is already authenticated, redirect to dashboard
      this.$router.push('/dashboard')
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

.form-group {
  margin-bottom: 25px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #00BFFF;
  box-shadow: 0 0 0 2px rgba(0, 191, 255, 0.2);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.btn-primary, .btn-secondary {
  width: 100%;
  padding: 15px;
  margin-bottom: 15px;
  font-size: 1rem;
  font-weight: bold;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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