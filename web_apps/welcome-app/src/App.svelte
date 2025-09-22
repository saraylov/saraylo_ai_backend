<script>
  import { onMount } from 'svelte';
  import { TELEGRAM_CONFIG } from './config.js';
  import Home from './Home.svelte';
  
  let currentPage = 'welcome'; // 'welcome', 'auth', or 'main'
  let logoVisible = false;
  let titleVisible = false;
  let darknessVisible = true;
  let beepSound;
  let authenticatedUser = null;
  let isTransitioning = false;
  let transitionDirection = 'forward'; // 'forward' or 'backward'
  
  onMount(async () => {
    // Create audio object for sound effects
    beepSound = new Audio('/sounds/beep.wav');
    beepSound.volume = 0.3;
    
    // Start the darkness reveal animation
    setTimeout(() => {
      darknessVisible = false;
      playSound();
    }, 300);
    
    // Trigger logo animation after darkness reveal
    setTimeout(() => {
      logoVisible = true;
      playSound();
    }, 2600);
    
    // Trigger title animation
    setTimeout(() => {
      titleVisible = true;
      playSound();
    }, 3300);
    
    // Auto navigate to auth page after animations complete with transition
    setTimeout(() => {
      triggerPageTransition('auth');
    }, 5000);
  });
  
  function playSound() {
    if (beepSound) {
      // Reset sound to beginning and play
      beepSound.currentTime = 0;
      beepSound.play().catch(e => console.log("Sound play prevented by browser policy:", e));
    }
  }
  
  function onTelegramAuth(user) {
    // Handle Telegram authentication
    console.log('Logged in as ' + user.first_name + ' ' + user.last_name + ' (' + user.id + (user.username ? ', @' + user.username : '') + ')');
    
    // Store authenticated user data
    authenticatedUser = user;
    
    // Trigger transition animation
    triggerPageTransition('main');
  }
  
  // Function to emulate authentication
  function emulateAuth() {
    const fakeUser = {
      id: 123456789,
      first_name: "Test",
      last_name: "User",
      username: "testuser",
      photo_url: "",
      auth_date: Math.floor(Date.now() / 1000),
      hash: "fake_hash_for_emulation"
    };
    
    onTelegramAuth(fakeUser);
  }
  
  // Function to handle logout from Home component
  function handleLogout() {
    authenticatedUser = null;
    triggerPageTransition('auth', 'backward');
  }
  
  // Function to trigger page transition with animation
  function triggerPageTransition(targetPage, direction = 'forward') {
    isTransitioning = true;
    transitionDirection = direction;
    
    // Wait for transition animation to complete before changing page
    setTimeout(() => {
      isTransitioning = false;
      currentPage = targetPage;
    }, 500); // Match this to the CSS transition duration
  }
</script>

{#if currentPage === 'welcome'}
  <div class="app-container" class:transitioning={isTransitioning} class:transition-forward={transitionDirection === 'forward'} class:transition-backward={transitionDirection === 'backward'}>
    <!-- Darkness overlay that reveals the content -->
    <div class="darkness-overlay" class:revealed={!darknessVisible}></div>
    
    <div class="welcome-screen" class:transitioning={isTransitioning} class:transition-forward={transitionDirection === 'forward'} class:transition-backward={transitionDirection === 'backward'}>
      <div class="logo-container">
        <img 
          src="/images/saraylo-logo.png" 
          alt="SARAYLO Logo" 
          class="logo"
          class:visible={logoVisible}
        />
      </div>
      
      <div class="title-container">
        <h1 class="app-title" class:visible={titleVisible}>SARAYLO</h1>
        <p class="app-subtitle" class:visible={titleVisible}>Ваш персональный квантовый беговой тренер</p>
      </div>
    </div>
  </div>
{:else if currentPage === 'auth'}
  <div class="app-container" class:transitioning={isTransitioning} class:transition-forward={transitionDirection === 'forward'} class:transition-backward={transitionDirection === 'backward'}>
    <div class="auth-screen" class:transitioning={isTransitioning} class:transition-forward={transitionDirection === 'forward'} class:transition-backward={transitionDirection === 'backward'}>
      <div class="logo-container">
        <img 
          src="/images/saraylo-logo.png" 
          alt="SARAYLO Logo" 
          class="logo auth-logo"
        />
      </div>
      
      <div class="auth-container">
        <h1 class="auth-title">Авторизация</h1>
        <p class="auth-subtitle">Войдите через Telegram для продолжения</p>
        
        <div class="telegram-login-container">
          <script async src={TELEGRAM_CONFIG.WIDGET_SCRIPT_URL} data-telegram-login={TELEGRAM_CONFIG.BOT_NAME} data-size="large" data-onauth="onTelegramAuth(user)" data-request-access="write"></script>
        </div>
        
        <div class="auth-divider">
          <span>или</span>
        </div>
        
        <button class="emulate-auth-btn" on:click={emulateAuth}>
          Эмуляция авторизации (для тестирования)
        </button>
        
        <p class="auth-note">Нажимая на кнопку, вы соглашаетесь с <button class="auth-link" on:click={() => {}}>условиями использования</button> и <button class="auth-link" on:click={() => {}}>политикой конфиденциальности</button></p>
      </div>
    </div>
  </div>
{:else if currentPage === 'main'}
  <div class="app-container" class:transitioning={isTransitioning} class:transition-forward={transitionDirection === 'forward'} class:transition-backward={transitionDirection === 'backward'}>
    <Home user={authenticatedUser} on:logout={handleLogout} />
  </div>
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #000033, #33001a);
    font-family: 'Arial', sans-serif;
    height: 100vh;
    overflow-x: hidden;
    overflow-y: auto; /* Разрешаем вертикальную прокрутку */
  }
  
  .app-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    transition: all 0.5s ease;
    position: relative;
  }
  
  .app-container.transitioning.transition-forward {
    animation: slideOutLeft 0.5s ease forwards;
  }
  
  .app-container.transitioning.transition-backward {
    animation: slideOutRight 0.5s ease forwards;
  }
  
  @keyframes slideOutLeft {
    0% {
      transform: translateX(0);
      opacity: 1;
    }
    100% {
      transform: translateX(-100%);
      opacity: 0;
    }
  }
  
  @keyframes slideOutRight {
    0% {
      transform: translateX(0);
      opacity: 1;
    }
    100% {
      transform: translateX(100%);
      opacity: 0;
    }
  }
  
  @keyframes slideInLeft {
    0% {
      transform: translateX(-100%);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideInRight {
    0% {
      transform: translateX(100%);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  /* Incoming page animations */
  .app-container:not(.transitioning) {
    animation: fadeIn 0.3s ease forwards;
  }
  
  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
  
  /* Darkness overlay that covers the entire screen initially */
  .darkness-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #000000;
    z-index: 1000;
    transition: opacity 2.3s cubic-bezier(0.22, 0.61, 0.36, 1);
    opacity: 1;
  }
  
  .darkness-overlay.revealed {
    opacity: 0;
    pointer-events: none;
  }
  
  .welcome-screen, .auth-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 716px;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
    transition: all 0.5s ease;
    min-height: 100vh; /* Минимальная высота экрана */
  }
  
  .welcome-screen.transitioning.transition-forward,
  .auth-screen.transitioning.transition-forward {
    animation: slideOutLeft 0.5s ease forwards;
  }
  
  .welcome-screen.transitioning.transition-backward,
  .auth-screen.transitioning.transition-backward {
    animation: slideOutRight 0.5s ease forwards;
  }
  
  .logo-container {
    margin-bottom: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  
  .logo {
    width: 250px;
    height: 250px;
    opacity: 0;
    transform: scale(0.5);
    transition: all 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  
  .logo.visible {
    opacity: 1;
    transform: scale(1);
  }
  
  .auth-logo {
    opacity: 1;
    transform: scale(1);
    width: 150px;
    height: 150px;
  }
  
  .title-container {
    text-align: center;
    margin-top: -10px;
  }
  
  .app-title {
    color: #00BFFF;
    font-size: 24px;
    font-weight: bold;
    margin: 0 0 10px 0;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.8s ease-out 0.3s;
    text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
  }
  
  .app-title.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .app-subtitle {
    color: white;
    font-size: 16px;
    margin: 0;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.8s ease-out 0.5s;
  }
  
  
  .app-subtitle.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  /* Auth screen styles */
  .auth-container {
    text-align: center;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 15px;
    padding: 30px;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 0 20px rgba(0, 191, 255, 0.3);
    animation: fadeIn 0.5s ease-out;
    max-height: 90vh; /* Ограничиваем высоту */
    overflow-y: auto; /* Разрешаем прокрутку внутри контейнера */
  }
  
  .auth-title {
    color: #00BFFF;
    font-size: 28px;
    margin: 0 0 15px 0;
    text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
  }
  
  .auth-subtitle {
    color: white;
    font-size: 16px;
    margin: 0 0 30px 0;
  }
  
  .telegram-login-container {
    margin: 20px 0;
  }
  
  .auth-divider {
    display: flex;
    align-items: center;
    text-align: center;
    color: #aaa;
    margin: 20px 0;
  }
  
  .auth-divider::before,
  .auth-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #444;
  }
  
  .auth-divider::before {
    margin-right: 10px;
  }
  
  .auth-divider::after {
    margin-left: 10px;
  }
  
  .emulate-auth-btn {
    background: linear-gradient(135deg, #00BFFF, #0066CC);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 20px;
    font-size: 16px;
    cursor: pointer;
    width: 100%;
    max-width: 300px;
    margin: 10px auto;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
  }
  
  .emulate-auth-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 191, 255, 0.5);
  }
  
  .auth-note {
    color: #aaa;
    font-size: 12px;
    margin-top: 30px;
  }
  
  .auth-link {
    color: #00BFFF;
    text-decoration: none;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 12px;
    padding: 0;
  }
  
  .auth-link:hover {
    text-decoration: underline;
  }
  
  /* Responsive design */
  @media (max-width: 768px) {
    .welcome-screen, .auth-screen {
      padding: 15px;
      max-width: 90%;
    }
    
    .logo {
      width: 200px;
      height: 200px;
    }
    
    .auth-logo {
      width: 120px;
      height: 120px;
    }
    
    .app-title {
      font-size: 20px;
    }
    
    .app-subtitle {
      font-size: 14px;
    }
    
    .auth-container {
      padding: 20px;
      max-width: 90%;
    }
    
    .auth-title {
      font-size: 24px;
    }
    
    .auth-subtitle {
      font-size: 14px;
    }
    
    .emulate-auth-btn {
      font-size: 14px;
      padding: 10px 16px;
    }
    
    .auth-note {
      font-size: 10px;
    }
  }
  
  @media (max-width: 480px) {
    .welcome-screen, .auth-screen {
      padding: 10px;
      max-width: 95%;
    }
    
    .logo {
      width: 150px;
      height: 150px;
    }
    
    .auth-logo {
      width: 100px;
      height: 100px;
    }
    
    .app-title {
      font-size: 18px;
    }
    
    .app-subtitle {
      font-size: 12px;
    }
    
    .auth-container {
      padding: 15px;
    }
    
    .auth-title {
      font-size: 20px;
    }
    
    .auth-subtitle {
      font-size: 12px;
    }
    
    .emulate-auth-btn {
      font-size: 12px;
      padding: 8px 12px;
    }
    
    .auth-note {
      font-size: 9px;
    }
  }
</style>