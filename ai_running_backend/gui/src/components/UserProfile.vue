<template>
  <div class="user-profile">
    <div class="profile-header glass-effect">
      <div class="user-avatar" v-if="user && user.photo_url">
        <img :src="user.photo_url" :alt="user.username || user.first_name" />
      </div>
      <div class="user-avatar placeholder" v-else>
        <span>{{ getUserInitials }}</span>
      </div>
      
      <div class="user-info">
        <h2>{{ getUserName }}</h2>
        <p v-if="user && user.username" class="username">@{{ user.username }}</p>
        <p class="user-type">
          <span v-if="isTelegramUser" class="type-badge telegram">Telegram пользователь</span>
          <span v-else-if="isDemoUser" class="type-badge demo">Демо режим</span>
          <span v-else class="type-badge api">API пользователь</span>
        </p>
      </div>
    </div>
    
    <div class="profile-details glass-effect">
      <h3>Информация о пользователе</h3>
      <div class="user-details">
        <div class="detail-item">
          <span class="label">ID:</span>
          <span class="value">{{ user ? user.id : 'N/A' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Имя:</span>
          <span class="value">{{ user ? user.first_name : 'N/A' }}</span>
        </div>
        <div class="detail-item" v-if="user && user.last_name">
          <span class="label">Фамилия:</span>
          <span class="value">{{ user.last_name }}</span>
        </div>
        <div class="detail-item" v-if="user && user.username">
          <span class="label">Имя пользователя:</span>
          <span class="value">@{{ user.username }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Дата авторизации:</span>
          <span class="value">{{ authDate }}</span>
        </div>
        <div class="detail-item" v-if="apiKey">
          <span class="label">Ваш персональный API ключ:</span>
          <span class="value api-key">{{ apiKey }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'UserProfile',
  computed: {
    ...mapGetters(['user', 'isTelegramUser', 'isDemoUser', 'apiKey']),
    
    getUserName() {
      if (!this.user) return 'Гость'
      
      if (this.user.first_name && this.user.last_name) {
        return `${this.user.first_name} ${this.user.last_name}`
      } else if (this.user.first_name) {
        return this.user.first_name
      } else if (this.user.username) {
        return this.user.username
      } else {
        return 'Пользователь'
      }
    },
    
    getUserInitials() {
      if (!this.user) return 'Г'
      
      let initials = ''
      if (this.user.first_name) {
        initials += this.user.first_name.charAt(0).toUpperCase()
      }
      if (this.user.last_name) {
        initials += this.user.last_name.charAt(0).toUpperCase()
      }
      
      return initials || (this.user.username ? this.user.username.charAt(0).toUpperCase() : 'П')
    },
    
    authDate() {
      if (!this.user || !this.user.auth_date) return 'N/A'
      
      const date = new Date(this.user.auth_date * 1000)
      return date.toLocaleString('ru-RU')
    }
  }
}
</script>

<style scoped>
.user-profile {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 25px;
  gap: 20px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar.placeholder {
  background: linear-gradient(45deg, #00BFFF, #FF1493);
}

.user-info h2 {
  margin-bottom: 5px;
}

.username {
  opacity: 0.8;
  margin-bottom: 10px;
}

.type-badge {
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: bold;
}

.type-badge.telegram {
  background: linear-gradient(45deg, #0088cc, #00aaff);
}

.type-badge.demo {
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
}

.type-badge.api {
  background: linear-gradient(45deg, #00BFFF, #FF1493);
}

.profile-details {
  padding: 25px;
}

.profile-details h3 {
  margin-bottom: 20px;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: bold;
  opacity: 0.8;
}

.value {
  text-align: right;
  word-break: break-all;
}

.value.api-key {
  font-family: monospace;
  font-size: 0.9rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 5px 10px;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .detail-item {
    flex-direction: column;
    gap: 5px;
  }
  
  .value {
    text-align: center;
  }
}
</style>