<script>
  import { createEventDispatcher, onMount } from 'svelte';
  
  export let user;
  
  const dispatch = createEventDispatcher();
  
  let isTransitioning = false;
  let transitionDirection = 'forward';
  
  onMount(() => {
    // Add a small delay to ensure smooth transition
    setTimeout(() => {
      isTransitioning = true;
    }, 50);
  });
  
  function handleLogout() {
    dispatch('logout');
  }
  
  function startWorkout() {
    alert('Начало тренировки!');
  }
</script>

<div class="home-container" class:transitioning={isTransitioning}>
  <header class="header glass-panel">
    <h1>Добро пожаловать, {user?.first_name || 'Пользователь'}!</h1>
    <button class="logout-btn" on:click={handleLogout}>Выйти</button>
  </header>
  
  <main class="main-content">
    <div class="stats-card glass-panel">
      <h2>Ваша статистика</h2>
      <div class="stat-item">
        <span>Пройдено км:</span>
        <span class="stat-value">12.5</span>
      </div>
      <div class="stat-item">
        <span>Калории:</span>
        <span class="stat-value">840</span>
      </div>
      <div class="stat-item">
        <span>Тренировки:</span>
        <span class="stat-value">7</span>
      </div>
    </div>
    
    <div class="workout-card glass-panel">
      <h2>Тренировка сегодня</h2>
      <p>План: 5 км бег трусцой</p>
      <button class="start-workout-btn" on:click={startWorkout}>
        Начать тренировку
      </button>
    </div>
  </main>
  
  <!-- Bottom navigation panel -->
  <nav class="bottom-nav glass-panel">
    <div class="nav-item" role="button" tabindex="0" aria-label="Статистика">
      <div class="nav-icon">📊</div>
      <span class="nav-label">Статистика</span>
    </div>
    
    <div class="nav-item" role="button" tabindex="0" aria-label="Здоровье">
      <div class="nav-icon">❤️</div>
      <span class="nav-label">Здоровье</span>
    </div>
    
    <div class="nav-item workout-btn" role="button" tabindex="0" aria-label="Начать тренировку" on:click={startWorkout}>
      <div class="nav-icon">🏃</div>
    </div>
    
    <div class="nav-item" role="button" tabindex="0" aria-label="Устройства">
      <div class="nav-icon">⌚</div>
      <span class="nav-label">Устройства</span>
    </div>
    
    <div class="nav-item" role="button" tabindex="0" aria-label="Профиль">
      <div class="nav-icon">👤</div>
      <span class="nav-label">Профиль</span>
    </div>
  </nav>
</div>

<style>
  .home-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background: linear-gradient(135deg, #000033, #33001a);
    color: white;
    font-family: 'Arial', sans-serif;
    padding-bottom: 140px; /* Increased to accommodate fixed nav panel */
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.5s ease;
    max-width: 716px;
    margin: 0 auto;
    width: 100%;
  }
  
  .home-container.transitioning {
    opacity: 1;
    transform: translateY(0);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    margin: 20px;
    border-radius: 15px;
    flex-shrink: 0;
  }
  
  .logout-btn {
    background: linear-gradient(135deg, #00BFFF, #0066CC);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    flex-shrink: 0;
  }
  
  .logout-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0, 191, 255, 0.3);
  }
  
  .main-content {
    flex: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto; /* Разрешаем вертикальную прокрутку */
  }
  
  .glass-panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 191, 255, 0.1);
  }
  
  .stats-card h2, .workout-card h2 {
    margin-top: 0;
    color: #00BFFF;
    text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    margin: 15px 0;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .stat-value {
    font-weight: bold;
    color: #00BFFF;
  }
  
  .start-workout-btn {
    background: linear-gradient(135deg, #00FF00, #006600);
    color: black;
    border: none;
    border-radius: 25px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    width: 100%;
    margin-top: 15px;
    transition: all 0.3s ease;
  }
  
  .start-workout-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0, 255, 0, 0.3);
  }
  
  /* Bottom navigation panel */
  .bottom-nav {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 50px);
    max-width: 666px; /* 716px - 50px for margins */
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    padding: 20px 15px;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.3), rgba(51, 51, 51, 0.3));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 191, 255, 0.1);
    z-index: 1000;
    align-items: center;
    justify-items: center;
    flex-shrink: 0;
  }
  
  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 8px;
    border-radius: 15px;
    transition: all 0.3s ease;
    text-align: center;
    min-width: 0;
    width: 60px; /* Fixed width for all items */
    height: 60px; /* Fixed height for all items */
  }
  
  .nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  .nav-icon {
    font-size: 28px;
    margin-bottom: 8px;
    flex-shrink: 0;
  }
  
  .nav-label {
    font-size: 14px;
    flex-shrink: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
  }
  
  .workout-btn {
    background: linear-gradient(135deg, #00FF00, #006600);
    border-radius: 50%;
    width: 70px;
    height: 70px;
    margin-top: -35px;
    box-shadow: 0 4px 20px rgba(0, 255, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  
  .workout-btn .nav-icon {
    font-size: 35px;
    margin-bottom: 0;
  }
  
  /* Responsive design */
  @media (max-width: 768px) {
    .home-container {
      padding-bottom: 110px;
    }
    
    .header {
      padding: 15px;
      margin: 15px;
    }
    
    .main-content {
      padding: 15px;
    }
    
    .bottom-nav {
      bottom: 30px;
      left: 20px;
      right: 20px;
      padding: 15px 10px;
      gap: 8px;
      border-radius: 25px;
    }
    
    .nav-icon {
      font-size: 24px;
      margin-bottom: 5px;
    }
    
    .nav-label {
      font-size: 12px;
    }
    
    .workout-btn {
      width: 60px;
      height: 60px;
      margin-top: -30px;
    }
    
    .workout-btn .nav-icon {
      font-size: 28px;
    }
  }
  
  @media (max-width: 480px) {
    .home-container {
      padding-bottom: 100px;
    }
    
    .header {
      padding: 10px;
      margin: 10px;
    }
    
    .main-content {
      padding: 10px;
    }
    
    .bottom-nav {
      bottom: 25px;
      left: 15px;
      right: 15px;
      padding: 12px 8px;
      gap: 5px;
      border-radius: 20px;
    }
    
    .nav-icon {
      font-size: 20px;
      margin-bottom: 3px;
    }
    
    .nav-label {
      font-size: 10px;
    }
    
    .workout-btn {
      width: 55px;
      height: 55px;
      margin-top: -27px;
    }
    
    .workout-btn .nav-icon {
      font-size: 24px;
    }
  }
</style>