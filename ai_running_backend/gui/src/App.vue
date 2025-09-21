<template>
  <div id="app">
    <!-- Splash Screen -->
    <SplashScreen @splash-finished="onSplashFinished" v-if="showSplash" />
    
    <!-- Main Content (only shown after splash screen finishes) -->
    <template v-else>
      <!-- Header Panel -->
      <header class="header-panel glass-panel" v-if="shouldShowHeader">
        <div class="header-content">
          <h1 class="header-title">SARAYLO</h1>
        </div>
      </header>
      
      <!-- Main Content -->
      <main class="main-content">
        <router-view />
      </main>
    </template>
    
    <!-- Removed Bottom Navigation -->
  </div>
</template>

<script>
import SplashScreen from './components/SplashScreen.vue'

export default {
  name: 'App',
  components: {
    SplashScreen
  },
  data() {
    return {
      showSplash: true // Always show splash screen initially
    }
  },
  computed: {
    shouldShowHeader() {
      const routeName = this.$route.name;
      return routeName !== 'Login' && routeName !== 'TelegramAuth' && routeName !== 'Home';
    }
  },
  methods: {
    onSplashFinished() {
      this.showSplash = false;
      // Navigate to login page after splash screen
      // Always go to login page regardless of authentication status
      this.$router.push('/login');
    }
  },
  mounted() {
    // If we're already on a route other than home, don't show splash screen
    if (this.$route.path !== '/') {
      this.showSplash = false;
    }
  }
}
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #000033, #33001a);
  color: #fff;
  min-height: 100vh;
  padding-bottom: 20px; /* Reduced padding since bottom nav is removed */
}

/* Glassmorphism effect */
.glass-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
}

/* Header Panel */
.header-panel {
  width: 551px; /* Фиксированная ширина */
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
  margin: 20px auto;
  position: relative;
}

.header-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.header-title {
  color: #00BFFF;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin: 0;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
}

/* Main Content */
.main-content {
  width: 100%;
  max-width: 551px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

/* Removed Bottom Navigation styles */

/* Button styles */
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(45deg, #00BFFF, #FF1493);
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Container styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Card styles */
.card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}

/* Typography */
h1, h2, h3 {
  margin-bottom: 15px;
}

h1 {
  font-size: 2rem;
  text-align: center;
}

h2 {
  font-size: 1.5rem;
}

p {
  line-height: 1.6;
  margin-bottom: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  h1 {
    font-size: 1.8rem;
  }
  
  h2 {
    font-size: 1.3rem;
  }
  
  .btn {
    padding: 10px 20px;
    font-size: 0.9rem;
  }
  
  .card {
    padding: 15px;
  }
  
  .header-panel,
  .main-content {
    width: 95%;
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 10px;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  h2 {
    font-size: 1.2rem;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 0.8rem;
    width: 100%;
    margin-bottom: 10px;
  }
  
  /* Stack elements on small screens */
  .plan-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .plan-summary {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
  
  .header-panel,
  .main-content {
    width: 100%;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1400px;
  }
  
  h1 {
    font-size: 2.5rem;
  }
  
  h2 {
    font-size: 1.8rem;
  }
}
</style>