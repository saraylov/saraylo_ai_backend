<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
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
}

/* Glassmorphism effect */
.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
}

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
}

/* Large screens */
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