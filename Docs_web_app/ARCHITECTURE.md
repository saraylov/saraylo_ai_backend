# SARAYLO - Quantum Running Coach
## Application Architecture

## Table of Contents
1. [Overview](#overview)
2. [Component Architecture](#component-architecture)
3. [State Management](#state-management)
4. [UI Components](#ui-components)
5. [Audio Assistant System](#audio-assistant-system)
6. [Permissions System](#permissions-system)
7. [API Integrations](#api-integrations)
8. [Application States](#application-states)
9. [Error Handling](#error-handling)
10. [Performance Optimization](#performance-optimization)
11. [Security](#security)
12. [Extensibility](#extensibility)
13. [Testing](#testing)
14. [Monitoring and Logging](#monitoring-and-logging)

---

## Overview

The SARAYLO application is built on a component-based Svelte architecture with a clear separation of responsibilities. The architecture follows modern development practices to ensure stability, maintainability, and extensibility.

### Technical Architecture
- **Frontend**: Svelte 4 with TypeScript and Vite 5
- **Design**: Glassmorphism with Miami Hit color scheme
- **Integrations**: Telegram Web App API, Mapbox GL JS, Web Speech API
- **Mobile Version**: Build via Capacitor for Android and iOS

## Component Architecture

### Component Structure
```
App.svelte
├── Header.svelte
├── MainContent.svelte
│   ├── Dashboard.svelte
│   ├── Training.svelte
│   │   ├── WorkoutButton.svelte
│   │   ├── CircularProgressBar.svelte
│   │   └── BottomNav.svelte
│   ├── AssessmentTraining.svelte
│   ├── Health.svelte
│   ├── Devices.svelte
│   ├── Profile.svelte
│   └── Settings.svelte
└── BottomNav.svelte
    └── WorkoutButton.svelte
```

### Central Data Store

#### Workout Store (src/utils/workoutStore.ts)
The central element for workout state control:

```typescript
interface WorkoutData {
  startTime: number | null;
  elapsedTime: number;
  totalDistance: number;
  currentSpeed: number;
  averageSpeed: number;
  maxSpeed: number;
  isWorkoutActive: boolean;
  workoutState: 'idle' | 'running' | 'paused';
  currentPosition: GeolocationPosition | null;
  locationError: string | null;
  isLocating: boolean;
  watchId: number | null;
}
```

Control functions:
- `startWorkout()`: Start workout
- `pauseWorkout()`: Pause workout
- `resumeWorkout()`: Resume workout
- `stopWorkout()`: Stop workout
- `updateWorkoutStats()`: Update statistics
- `updateCurrentPosition()`: Update position
- `setLocationError()`: Set geolocation error
- `setLocating()`: Set location determination state
- `setWatchId()`: Set tracking ID

## State Management

### Application Lifecycle

#### Workout Lifecycle
1. **Idle State**
   - User in application
   - "Start" button active
   - Geolocation not tracked
   - Statistics reset

2. **Running State**
   - Workout active
   - Geolocation tracked
   - Statistics updated
   - "Stop" and "Pause" buttons active

3. **Paused State**
   - Workout paused
   - Geolocation suspended
   - Statistics frozen
   - "Stop" and "Resume" buttons active

### State Management
Using Svelte Stores for reactive management:

```typescript
// Create store
export const workoutStore = writable<WorkoutData>(initialWorkoutData);

// Subscribe to changes
workoutStore.subscribe(data => {
  // Update UI
});

// Update data
workoutStore.update(data => ({
  ...data,
  ...newStats
}));
```

## UI Components

### WorkoutButton.svelte
Workout button component with unique hold mechanics:

**States:**
1. **Start** (blue gradient): Hold for 2.5 seconds to start
2. **Stop** (red gradient): Immediate stop
3. **Pause** (yellow gradient): Immediate pause
4. **Resume** (green gradient): Immediate resume

**Hold Mechanics:**
- Touch/Mouse events: touchstart/mousedown and touchend/mouseup
- 2500ms timer with updates every 50ms
- Visual indication through CircularProgressBar
- Reset on premature release

### CircularProgressBar.svelte
SVG component for visual progress indication:

```svelte
<svg viewBox="0 0 120 120">
  <circle class="background" cx="60" cy="60" r="54" />
  <circle 
    class="progress" 
    cx="60" 
    cy="60" 
    r="54"
    stroke-dasharray="{circumference}"
    stroke-dashoffset="{offset}"
  />
</svg>
```

### Training.svelte
Main workout component with integration of all systems:

**Functions:**
- Mapbox map initialization
- Geolocation tracking
- Workout statistics collection
- Route management
- Audio assistant integration

**Mapbox Integration:**
```typescript
mapboxgl.accessToken = 'YOUR_TOKEN';
const map = new mapboxgl.Map({
  container: mapContainer,
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [lng, lat],
  zoom: 15
});
```

### AssessmentTraining.svelte
Assessment workout component:

**Stages:**
1. Preparation (6 minutes blue zone)
2. Light load (5 minutes green zone)
3. Moderate load (5 minutes yellow zone)
4. High load (3 minutes orange zone)
5. Maximum load (1 minute red zone)

**Zone Calculation Algorithm:**
- Speed data collection during workout
- Kalman filter application for smoothing
- Calculation of 20th and 80th percentiles
- Determination of intensity zone boundaries

## Audio Assistant System

### AudioAssistant (src/utils/audioAssistant.ts)
Class for working with Web Speech API:

```typescript
class AudioAssistant {
  private speechQueue: SpeechSynthesisUtterance[] = [];
  private isSpeaking = false;
  
  speak(text: string): void {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    this.speechQueue.push(utterance);
    this.processQueue();
  }
}
```

## Permissions System

### Permissions (src/permissions.ts)
Permission management for mobile devices:

```typescript
async function requestLocationPermissions(): Promise<boolean> {
  const { geolocation } = Plugins;
  const result = await geolocation.requestPermissions();
  return result.location === 'granted';
}

async function requestNotificationPermissions(): Promise<boolean> {
  const { PushNotifications } = Plugins;
  const result = await PushNotifications.requestPermissions();
  return result.receive === 'granted';
}
```

## API Integrations

### Telegram Web App API
Telegram integration for authentication:

```typescript
interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code: string;
  is_premium?: boolean;
}

function authenticateUser(): Promise<TelegramUser | null> {
  if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
    return Promise.resolve(window.Telegram.WebApp.initDataUnsafe.user);
  }
  return Promise.resolve(null);
}
```

### Mapbox GL JS
Map service integration:

```typescript
// Map initialization
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [lng, lat],
  zoom: 15
});

// Add geolocation
const geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: true
  },
  trackUserLocation: true
});

map.addControl(geolocate);
```

### Capacitor Plugins
Integration with native mobile device capabilities:

```typescript
// Geolocation
import { Geolocation } from '@capacitor/geolocation';

const coordinates = await Geolocation.getCurrentPosition();

// Notifications
import { PushNotifications } from '@capacitor/push-notifications';

PushNotifications.requestPermissions().then(result => {
  if (result.receive === 'granted') {
    // Permission granted
  }
});
```

## Error Handling

### Geolocation Errors
```typescript
geolocateControl.on('error', (error) => {
  console.error('Geolocation error:', error);
  locationError = true;
  isLocating = false;
  
  // Retry geolocation
  setTimeout(() => {
    geolocateControl.trigger();
  }, 5000);
});
```

### Audio Assistant Errors
```typescript
utterance.onerror = (event) => {
  console.error('Speech synthesis error:', event.error);
  this.isSpeaking = false;
  this.processQueue();
};
```

## Performance Optimization

### Update Rate Limiting
```typescript
// Limit route updates
const ROUTE_UPDATE_INTERVAL = 1000; // 1 second
let lastRouteUpdate = 0;

function updateRouteTracking(lng: number, lat: number) {
  const now = Date.now();
  if (now - lastRouteUpdate < ROUTE_UPDATE_INTERVAL) {
    return;
  }
  lastRouteUpdate = now;
  // Update route
}
```

### Memory Efficiency
```typescript
// Clean up resources when component is destroyed
onDestroy(() => {
  if (watchId !== null) {
    navigator.geolocation.clearWatch(watchId);
  }
  
  if (map) {
    map.remove();
  }
});
```

## Security

### Telegram Data Validation
```typescript
function validateTelegramData(initData: string, token: string): boolean {
  const secret = crypto.createHmac('sha256', 'WebAppData')
    .update(token)
    .digest();
    
  const params = new URLSearchParams(initData);
  const hash = params.get('hash');
  params.delete('hash');
  
  const sortedParams = [...params.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');
    
  const calculatedHash = crypto
    .createHmac('sha256', secret)
    .update(sortedParams)
    .digest('hex');
    
  return calculatedHash === hash;
}
```

### Personal Data Protection
```typescript
// Minimize data storage
const userData = {
  id: user.id,
  first_name: user.first_name,
  // Don't save sensitive data
};
```

## Extensibility

### Modular Architecture
Each component is responsible for its functional area:
- UI components are responsible for display
- Utilities are responsible for logic
- Stores are responsible for state

### Extendable Interfaces
```typescript
// Extendable workout interface
interface WorkoutData {
  // Basic fields
  startTime: number | null;
  // ... other fields
  
  // Extendable fields
  [key: string]: any;
}
```

## Testing

### Functional Testing
- Test button hold mechanics
- Test state switching
- Test geolocation data collection
- Test audio assistant

### Performance Testing
- Measure UI response time
- Check memory consumption
- Test on weak devices

## Monitoring and Logging

### Event Logging
```typescript
// Log key events
console.log('Workout started at:', new Date());
console.log('Location updated:', position);
console.log('Workout paused at:', new Date());
```

### Error Monitoring
```typescript
// Monitor geolocation errors
window.addEventListener('error', (event) => {
  console.error('Application error:', event.error);
});
```

## Conclusion

The SARAYLO application architecture is built with modern development practices:
- Clear separation of responsibilities
- Reactive state management
- Effective error handling
- Performance optimization
- Data security
- Extensibility and maintainability

This architecture ensures stable application operation, easy maintenance, and the ability to further develop functionality.