<script lang="ts">
  import { onMount } from 'svelte';
  import './app.css';
  import Profile from './Profile.svelte';
  import Training from './Training.svelte';
  import PreTraining from './PreTraining.svelte';
  import Devices from './Devices.svelte';
  import Health from './Health.svelte';
  import Settings from './Settings.svelte';
  import HistoryTrain from './HistoryTrain.svelte';
  import AssessmentTraining from './AssessmentTraining.svelte';
  import AudioAssistedAssessment from './AudioAssistedAssessment.svelte';
  import Dashboard from './Dashboard.svelte';
  import Login from './Login.svelte';
  import Calendar from './Calendar.svelte';
  import { saveDailyData, loadDailyData, getToday, formatDate } from './utils/dataStorage';
  import { requestAllPermissions } from './permissions';
  
  /** @type {boolean} */
  let isAuthorized = true; // Временно установим в true для обхода авторизации
  /** @type {string} */
  let authStatus = '';
  /** @type {boolean} */
  let isLoading = false;
  /** @type {{id?: number, first_name: string, last_name?: string, username?: string} | null} */
  let userData = {
    id: 123456789,
    first_name: 'Тестовый',
    last_name: 'Пользователь',
    username: 'testuser'
  };
  /** @type {string} */
  let currentView = 'dashboard'; // Всегда показываем dashboard
  /** @type {boolean} */
  let showTelegramWidget = false;
  
  
  // Activity rings data - initialized to 0 to avoid simulation
  let activityData = {
    move: { value: 0, goal: 500, color: '#00BFFF' }, // calories
    exercise: { value: 0, goal: 60, color: '#FF1493' }, // exercise minutes
    stand: { value: 0, goal: 12, color: '#00FF00' } // sleep hours
  };
  
  // Steps data for progress bar - initialized to 0 to avoid simulation
  let stepsData = {
    value: 0,
    goal: 50000
  };
  
  // Store today's date to check when the day changes
  let today = getToday();
  
  // Helper function to check if in training mode
  function isInTrainingMode() {
    return currentView === 'training';
  }
  
  // Function to save today's data
  function saveTodaysData() {
    const todayDate = getToday();
    const dataToSave = {
      date: todayDate,
      steps: { ...stepsData },
      activity: { ...activityData }
    };
    
    saveDailyData(dataToSave);
    console.log(`Saved data for ${todayDate}`);
  }
  
  // Function to get real user data
  function getRealUserData() {
    // In a real implementation, this would fetch actual user data from sensors or API
    // For now, we'll set all values to 0 as there's no real data source
    // This ensures we're not showing any simulated/emulated data
    
    // Reset all activity data to 0 since we don't have real data sources
    activityData.move.value = 0;
    activityData.exercise.value = 0;
    activityData.stand.value = 0;
    
    // Reset steps data to 0
    stepsData.value = 0;
  }
  
  // Handle logout
  function handleLogout() {
    // Save data before logout
    saveTodaysData();
    // Временно отключим logout
    console.log('Logout temporarily disabled');
  }
  
  // Handle add button click
  function handleAddClick() {
    console.log('Add button clicked');
    // TODO: Implement add functionality
  }
  
  // Handle details button click
  function handleDetailsClick() {
    console.log('Details button clicked');
    // TODO: Implement details functionality
  }
  
  // Handle popstate events for browser navigation
  function handlePopState() {
    currentView = 'dashboard';
  }
  
  // Initialize
  onMount(() => {
    // Add event listener for browser navigation (back/forward buttons)
    window.addEventListener('popstate', handlePopState);
  
    // Always show dashboard
    currentView = 'dashboard';
    authStatus = 'Production by V Saraylo';
    
    // Request necessary permissions for Android app
    requestAllPermissions().then((permissions) => {
      console.log('Permissions granted:', permissions);
    }).catch((error) => {
      console.error('Error requesting permissions:', error);
    });
    
    // Initialize with real user data
    getRealUserData();
    
    // Update data every minute to ensure it stays at 0 (no simulation)
    setInterval(getRealUserData, 60000);
  
    // Cleanup event listeners
    return () => {
      window.removeEventListener('popstate', handlePopState);
      // Save data when component is destroyed
      saveTodaysData();
    };
  });
  
  // Watch for changes in showTelegramWidget
  $: if (showTelegramWidget) {
    // Temporarily disabled since loadTelegramWidget function is not defined
  }
  
  // Function to trigger Telegram Login Widget
  function handleTelegramAuth() {
    showTelegramWidget = true;
  }
  
  // Handle training button click - now goes to pre-training page
  function handleTrainingClick() {
    console.log('handleTrainingClick called, setting currentView to pre-training');
    currentView = 'pre-training';
  }
  
  // Handle start training from pre-training page
  function handleStartTraining() {
    console.log('handleStartTraining called, setting currentView to training');
    currentView = 'training';
  }
  
  // Handle back to dashboard from training
  function handleBackToDashboard() {
    console.log('handleBackToDashboard called, setting currentView to dashboard');
    currentView = 'dashboard';
  }

  // Handle profile navigation
  function handleProfileClick() {
    console.log('handleProfileClick called, setting currentView to profile');
    currentView = 'profile';
  }

  // Handle devices navigation
  function handleDevicesClick() {
    console.log('handleDevicesClick called, setting currentView to devices');
    currentView = 'devices';
  }

  // Handle health navigation
  function handleHealthClick() {
    console.log('handleHealthClick called, setting currentView to health');
    currentView = 'health';
  }

  // Handle settings navigation
  function handleSettingsClick() {
    console.log('handleSettingsClick called, setting currentView to settings');
    currentView = 'settings';
  }

  // Handle history navigation
  function handleHistoryClick() {
    console.log('handleHistoryClick called in App.svelte');
    console.log('Current view before change:', currentView);
    // Let's also add a small delay to see if there's a timing issue
    setTimeout(() => {
      currentView = 'history';
      console.log('Current view after change:', currentView);
    }, 10);
  }
  
  // Handle assessment training navigation
  function handleAssessmentTrainingClick() {
    console.log('handleAssessmentTrainingClick called, setting currentView to assessment');
    currentView = 'assessment';
  }
  
  // Handle calendar navigation
  function handleCalendarClick() {
    console.log('handleCalendarClick called, setting currentView to calendar');
    currentView = 'calendar';
  }
  
  // Handle workout navigation
  function handleStartWorkout() {
    console.log('handleStartWorkout called');
    // TODO: Implement workout start functionality
  }
  
  function handleStopWorkout() {
    console.log('handleStopWorkout called');
    // TODO: Implement workout stop functionality
  }
  
  function handlePauseWorkout() {
    console.log('handlePauseWorkout called');
    // TODO: Implement workout pause functionality
  }
  
  function handleResumeWorkout() {
    console.log('handleResumeWorkout called');
    // TODO: Implement workout resume functionality
  }
  
  // Handle setting current view (for Login component)
  function setCurrentView(view: string) {
    currentView = view;
  }
  
  // Helper function to ensure userData has all required properties for Settings component
  function getSettingsUserData() {
    if (!userData) {
      return {
        id: 0,
        first_name: '',
        last_name: '',
        username: ''
      };
    }
    
    return {
      id: userData.id || 0,
      first_name: userData.first_name,
      last_name: userData.last_name || '',
      username: userData.username || ''
    };
  }
</script>

<svelte:head>
  <title>SARAYLO</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <script>
    function onTelegramAuth(user) {
      // Dispatch event to Svelte component
      window.dispatchEvent(new CustomEvent('telegramAuth', { detail: user }));
    }
  </script>
</svelte:head>

{#if currentView === 'login'}
  <Login {setCurrentView} />
{:else if currentView === 'dashboard'}
  <Dashboard 
    {activityData}
    {stepsData}
    {handleAddClick}
    {handleDetailsClick}
    {handleLogout}
    isInTrainingMode={isInTrainingMode()}
    {handleBackToDashboard}
    {handleHealthClick}
    {handleTrainingClick}
    {handleDevicesClick}
    {handleProfileClick}
    {handleSettingsClick}
    {handleCalendarClick}
  />
{:else if currentView === 'pre-training'}
  <PreTraining 
    {handleBackToDashboard}
    {handleStartTraining}
    {handleHealthClick}
    {handleTrainingClick}
    {handleDevicesClick}
    {handleProfileClick}
    {handleSettingsClick}
  />
{:else if currentView === 'training'}
  <Training 
    {handleBackToDashboard} 
    {handleHealthClick} 
    {handleTrainingClick} 
    {handleDevicesClick} 
    {handleProfileClick} 
    {handleSettingsClick} 
    {handleHistoryClick}
    onStartWorkoutProp={handleStartWorkout}
    onStopWorkoutProp={handleStopWorkout}
    onPauseWorkoutProp={handlePauseWorkout}
    onResumeWorkoutProp={handleResumeWorkout}
  />
{:else if currentView === 'devices'}
  <Devices {handleBackToDashboard} {handleHealthClick} {handleTrainingClick} {handleDevicesClick} {handleProfileClick} />
{:else if currentView === 'health'}
  <Health {handleBackToDashboard} {handleHealthClick} {handleTrainingClick} {handleDevicesClick} {handleProfileClick} />
{:else if currentView === 'profile'}
  <Profile {userData} {handleBackToDashboard} {handleHealthClick} {handleTrainingClick} {handleDevicesClick} {handleProfileClick} {handleSettingsClick} />
{:else if currentView === 'settings'}
  <Settings 
    userData={getSettingsUserData()} 
    handleBackToDashboard={handleBackToDashboard} 
    handleHealthClick={handleHealthClick} 
    handleTrainingClick={handleTrainingClick} 
    handleDevicesClick={handleDevicesClick} 
    handleProfileClick={handleProfileClick} 
    handleLogout={handleLogout}
  />
{:else if currentView === 'history'}
  <HistoryTrain {handleBackToDashboard} {handleHealthClick} {handleTrainingClick} {handleDevicesClick} {handleProfileClick} {handleSettingsClick} />
{:else if currentView === 'assessment'}
  <AssessmentTraining 
    {handleBackToDashboard} 
    {handleHealthClick} 
    {handleTrainingClick} 
    {handleDevicesClick} 
    {handleProfileClick} 
    {handleSettingsClick} 
  />
{:else if currentView === 'audio-assessment'}
  <AudioAssistedAssessment 
    {handleBackToDashboard} 
    {handleHealthClick} 
    {handleTrainingClick} 
    {handleDevicesClick} 
    {handleProfileClick} 
    {handleSettingsClick} 
  />
{:else if currentView === 'calendar'}
  <Calendar {handleBackToDashboard} {handleHealthClick} {handleTrainingClick} {handleDevicesClick} {handleProfileClick} {handleSettingsClick} />
{/if}

<style>
  /* Main title */
  .main-title {
    font-size: clamp(2rem, 8vw, 4rem);
    font-weight: 800;
    /* Updated to use Miami Hit color scheme */
    background: linear-gradient(90deg, var(--primary-blue), var(--primary-pink));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: clamp(15px, 3vw, 30px);
    text-shadow: 0 0 clamp(10px, 2vw, 25px) rgba(0, 191, 255, 0.3);
    animation: shimmer 3s ease-in-out infinite;
    background-size: 200% 200%;
  }
  
  .subtitle {
    font-size: clamp(1.1rem, 3.5vw, 1.8rem);
    color: var(--light-gray);
    text-align: center;
    margin-bottom: clamp(20px, 3vw, 40px);
    font-weight: 500;
  }
  
  /* Description */
  .description {
    text-align: center;
    margin-bottom: clamp(20px, 3vw, 40px);
    color: var(--light-gray);
  }
  
  .description p {
    margin-bottom: clamp(10px, 1.5vw, 20px);
    line-height: 1.6;
    font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  }
  
  /* Auth section */
  .auth-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(15px, 2.5vw, 30px);
  }
  
  .production-info-static {
    font-size: clamp(1rem, 2.8vw, 1.3rem);
    color: var(--light-gray);
    margin-bottom: clamp(8px, 1.5vw, 15px);
  }
  
  .telegram-auth-button {
    background: linear-gradient(135deg, var(--primary-blue), var(--primary-pink));
    border: none;
    border-radius: clamp(8px, 2vw, 15px);
    padding: clamp(12px, 2vw, 18px) clamp(25px, 4vw, 40px);
    color: white;
    font-size: clamp(1rem, 2.5vw, 1.2rem);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: clamp(8px, 1.5vw, 12px);
    box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
  }
  
  .telegram-auth-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 191, 255, 0.4);
  }
  
  .telegram-auth-button:active {
    transform: translateY(0);
  }
  
  /* Loading spinner */
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .spinner {
    width: clamp(40px, 8vw, 60px);
    height: clamp(40px, 8vw, 60px);
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 4px solid var(--primary-blue);
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Auth error message */
  .auth-error {
    color: #ff6b6b;
    text-align: center;
    margin-top: clamp(15px, 2vw, 25px);
    font-size: clamp(0.9rem, 2vw, 1.1rem);
  }
  
  /* App container */
  .app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, var(--background-dark), var(--background-light));
    padding: clamp(10px, 2vw, 20px);
    position: relative;
    overflow-x: hidden;
  }
  
  /* Glass panel */
  .glass-panel {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(51, 51, 51, 0.2));
    backdrop-filter: blur(10px);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: clamp(15px, 3vw, 30px);
    box-shadow: 0 8px 32px rgba(0, 191, 255, 0.2);
    margin-bottom: clamp(70px, 10vw, 90px);
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  /* Background animation */
  .background-animation {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
  }
  
  .sports-item {
    position: absolute;
    opacity: 0.05;
    animation: float 20s infinite linear;
  }
  
  .football {
    width: clamp(30px, 5vw, 60px);
    height: clamp(30px, 5vw, 60px);
    background: radial-gradient(circle, var(--primary-blue) 30%, transparent 70%);
    border-radius: 50%;
    top: 10%;
    left: 5%;
    animation-duration: 25s;
  }
  
  .basketball {
    width: clamp(25px, 4vw, 50px);
    height: clamp(25px, 4vw, 50px);
    background: radial-gradient(circle, var(--primary-pink) 30%, transparent 70%);
    border-radius: 50%;
    top: 20%;
    right: 10%;
    animation-duration: 30s;
  }
  
  .sneakers {
    width: clamp(40px, 6vw, 80px);
    height: clamp(20px, 3vw, 40px);
    background: linear-gradient(45deg, var(--primary-blue), var(--primary-pink));
    border-radius: 30% 30% 50% 50%;
    bottom: 15%;
    left: 15%;
    animation-duration: 35s;
  }
  
  .shorts {
    width: clamp(30px, 5vw, 60px);
    height: clamp(15px, 2.5vw, 30px);
    background: linear-gradient(135deg, var(--primary-pink), var(--primary-blue));
    border-radius: 10%;
    top: 40%;
    right: 20%;
    animation-duration: 28s;
  }
  
  .tshirt {
    width: clamp(35px, 5.5vw, 70px);
    height: clamp(35px, 5.5vw, 70px);
    background: linear-gradient(90deg, var(--primary-blue), var(--primary-pink));
    clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 100%, 0% 100%, 0% 30%);
    bottom: 25%;
    right: 25%;
    animation-duration: 32s;
  }
  
  @keyframes float {
    0% {
      transform: translate(0, 0) rotate(0deg);
    }
    25% {
      transform: translate(100px, 50px) rotate(90deg);
    }
    50% {
      transform: translate(200px, 100px) rotate(180deg);
    }
    75% {
      transform: translate(100px, 150px) rotate(270deg);
    }
    100% {
      transform: translate(0, 0) rotate(360deg);
    }
  }
  
  @keyframes shimmer {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
    100% {
      background-position: 0% 50%;
    }
  }
  
  /* Responsive design */
  @media (max-width: 768px) {
    .glass-panel {
      padding: clamp(10px, 2vw, 20px);
      margin-bottom: 80px;
    }
    
    .main-title {
      font-size: clamp(1.8rem, 10vw, 3rem);
    }
    
    .subtitle {
      font-size: clamp(1rem, 4vw, 1.5rem);
    }
  }
  
  @media (max-width: 480px) {
    .app-container {
      padding: 10px;
    }
    
    .glass-panel {
      padding: 15px;
      margin-bottom: 70px;
    }
    
    .telegram-auth-button {
      padding: 12px 25px;
      font-size: 1rem;
    }
  }
</style>