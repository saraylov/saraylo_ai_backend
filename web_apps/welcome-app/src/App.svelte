<script>
  import { onMount } from 'svelte';
  
  let logoVisible = false;
  let titleVisible = false;
  let darknessVisible = true;
  let beepSound;
  
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
  });
  
  function playSound() {
    if (beepSound) {
      // Reset sound to beginning and play
      beepSound.currentTime = 0;
      beepSound.play().catch(e => console.log("Sound play prevented by browser policy:", e));
    }
  }
</script>

<div class="app-container">
  <!-- Darkness overlay that reveals the content -->
  <div class="darkness-overlay" class:revealed={!darknessVisible}></div>
  
  <div class="welcome-screen">
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

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #000033, #33001a);
    font-family: 'Arial', sans-serif;
    height: 100vh;
    overflow: hidden;
  }
  
  .app-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
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
  
  .welcome-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 551px;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
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
  
  /* Glassmorphism effect for future use */
  .glass-panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
  }
</style>