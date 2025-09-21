# SARAYLO - Quantum Running Coach
## API Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [API Integrations](#api-integrations)
3. [Internal APIs and Utilities](#internal-apis-and-utilities)
4. [API Security](#api-security)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Updating the Application](#updating-the-application)

---

## Introduction

This document contains technical documentation for the SARAYLO application, including API integration descriptions, internal utilities, architectural solutions, and technical implementation details.

## API Integrations

### Telegram Web App API

#### Main Functions
Web App Initialization:
```typescript
function initTelegramWebApp(): boolean {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();
    return true;
  }
  return false;
}
```

User Authentication:
```typescript
interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code: string;
  is_premium?: boolean;
}

async function authenticateUser(): Promise<TelegramUser | null> {
  if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
    return window.Telegram.WebApp.initDataUnsafe.user;
  }
  return null;
}
```

#### Telegram Web App Methods
| Method | Description | Usage Example |
|-------|----------|---------------------|
| `WebApp.ready()` | Tells Telegram the app is ready | `window.Telegram.WebApp.ready()` |
| `WebApp.expand()` | Expands the app to full screen | `window.Telegram.WebApp.expand()` |
| `WebApp.close()` | Closes the app | `window.Telegram.WebApp.close()` |
| `WebApp.MainButton` | Object for working with main button | `window.Telegram.WebApp.MainButton.show()` |

#### Data Validation
```typescript
function validateTelegramData(initData: string, token: string): boolean {
  // Create secret key
  const secret = crypto.createHmac('sha256', 'WebAppData')
    .update(token)
    .digest();
    
  // Parse parameters
  const params = new URLSearchParams(initData);
  const hash = params.get('hash');
  params.delete('hash');
  
  // Sort parameters
  const sortedParams = [...params.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');
    
  // Calculate hash
  const calculatedHash = crypto
    .createHmac('sha256', secret)
    .update(sortedParams)
    .digest('hex');
    
  return calculatedHash === hash;
}
```

### Mapbox GL JS API

#### Map Initialization
```typescript
import mapboxgl from 'mapbox-gl';

// Set access token
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';

// Create map
const map = new mapboxgl.Map({
  container: 'map-container', // Container element ID
  style: 'mapbox://styles/mapbox/streets-v12', // Map style
  center: [30.3158, 59.9343], // Map center [longitude, latitude]
  zoom: 10 // Zoom level
});
```

#### Map Control
Navigation controls:
```typescript
// Add navigation controls
const nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'top-right');
```

Geolocation:
```typescript
// Add geolocation control
const geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
    enableHighAccuracy: true
  },
  trackUserLocation: true,
  showUserHeading: true
});

map.addControl(geolocate);
```

#### Working with Lines (Polylines)
Adding data source:
```typescript
// Create GeoJSON data
const geojson = {
  type: 'Feature',
  properties: {},
  geometry: {
    type: 'LineString',
    coordinates: [
      [30.3158, 59.9343],
      [30.3258, 59.9443],
      [30.3358, 59.9543]
    ]
  }
};

// Add data source
map.addSource('route', {
  type: 'geojson',
  data: geojson
});
```

Adding line layer:
```typescript
// Add line layer
map.addLayer({
  id: 'route-line',
  type: 'line',
  source: 'route',
  layout: {
    'line-join': 'round',
    'line-cap': 'round'
  },
  paint: {
    'line-color': '#00BFFF',
    'line-width': 4,
    'line-opacity': 0.8
  }
});
```

### Web Speech API

#### Speech Synthesis
Basic usage:
```typescript
function speakText(text: string): void {
  // Check browser support
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Configure parameters
    utterance.lang = 'en-US';     // Language
    utterance.rate = 1.0;         // Speech rate
    utterance.pitch = 1.0;        // Pitch
    utterance.volume = 1.0;       // Volume
    
    // Play
    window.speechSynthesis.speak(utterance);
  }
}
```

#### Advanced Implementation with Queue
```typescript
class AudioAssistant {
  private speechQueue: SpeechSynthesisUtterance[] = [];
  private isSpeaking = false;
  
  speak(text: string): void {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    
    // Event handlers
    utterance.onstart = () => {
      this.isSpeaking = true;
    };
    
    utterance.onend = () => {
      this.isSpeaking = false;
      this.processQueue();
    };
    
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event.error);
      this.isSpeaking = false;
      this.processQueue();
    };
    
    this.speechQueue.push(utterance);
    this.processQueue();
  }
  
  private processQueue(): void {
    if (this.isSpeaking || this.speechQueue.length === 0) {
      return;
    }
    
    const utterance = this.speechQueue.shift();
    if (utterance) {
      window.speechSynthesis.speak(utterance);
    }
  }
  
  // Support check
  isSupported(): boolean {
    return 'speechSynthesis' in window;
  }
}
```

### Capacitor Plugins API

#### Geolocation (@capacitor/geolocation)
Getting current position:
```typescript
import { Geolocation } from '@capacitor/geolocation';

async function getCurrentPosition(): Promise<GeolocationPosition> {
  const coordinates = await Geolocation.getCurrentPosition({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 3000
  });
  
  return coordinates;
}
```

Position tracking:
```typescript
async function watchPosition(): Promise<number> {
  const watchId = await Geolocation.watchPosition({
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 3000
  }, (position, err) => {
    if (err) {
      console.error('Geolocation error:', err);
      return;
    }
    
    console.log('New position:', position);
  });
  
  return watchId;
}
```

#### Notifications (@capacitor/push-notifications)
Requesting permissions:
```typescript
import { PushNotifications } from '@capacitor/push-notifications';

async function requestNotificationPermissions(): Promise<boolean> {
  const result = await PushNotifications.requestPermissions();
  return result.receive === 'granted';
}
```

## Internal APIs and Utilities

### Workout Store (src/utils/workoutStore.ts)

#### Workout Data Interface
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

#### Control Functions
Starting a workout:
```typescript
export const startWorkout = () => {
  workoutStore.update(data => ({
    ...data,
    startTime: Date.now(),
    isWorkoutActive: true,
    workoutState: 'running',
    // Reset statistics
    totalDistance: 0,
    currentSpeed: 0,
    averageSpeed: 0,
    maxSpeed: 0,
    elapsedTime: 0
  }));
};
```

Pausing a workout:
```typescript
export const pauseWorkout = () => {
  workoutStore.update(data => ({
    ...data,
    workoutState: 'paused'
  }));
};
```

Resuming a workout:
```typescript
export const resumeWorkout = () => {
  workoutStore.update(data => ({
    ...data,
    workoutState: 'running'
  }));
};
```

Stopping a workout:
```typescript
export const stopWorkout = () => {
  workoutStore.set(initialWorkoutData);
};
```

#### Derived Store for Time Formatting
```typescript
export const formattedTime = derived(
  workoutStore,
  ($workoutStore) => {
    const totalSeconds = Math.floor($workoutStore.elapsedTime / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
);
```

### Kalman Filter (src/utils/calibrationCalculator.ts)
Filter implementation:
```typescript
class KalmanFilter {
  private state: number;
  private covariance: number;
  private readonly processNoise: number;
  private readonly measurementNoise: number;
  
  constructor(initialState: number = 0, initialCovariance: number = 1) {
    this.state = initialState;
    this.covariance = initialCovariance;
    this.processNoise = 1e-5;
    this.measurementNoise = 1e-1;
  }
  
  filter(measurement: number): number {
    // Prediction step
    this.covariance += this.processNoise;
    
    // Update step
    const kalmanGain = this.covariance / (this.covariance + this.measurementNoise);
    this.state += kalmanGain * (measurement - this.state);
    this.covariance *= (1 - kalmanGain);
    
    return this.state;
  }
}
```

### Distance Calculation (src/utils/workoutStore.ts)
Haversine formula:
```typescript
export const calculateDistance = (
  lat1: number, 
  lon1: number, 
  lat2: number, 
  lon2: number
): number => {
  const R = 6371e3; // Earth radius in meters
  const phi1 = lat1 * Math.PI/180;
  const phi2 = lat2 * Math.PI/180;
  const deltaPhi = (lat2-lat1) * Math.PI/180;
  const deltaLambda = (lon2-lon1) * Math.PI/180;

  const a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) +
            Math.cos(phi1) * Math.cos(phi2) *
            Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

  return R * c; // Distance in meters
};
```

### Speed Calculation (src/utils/workoutStore.ts)
```typescript
export const calculateSpeed = (
  distance: number, 
  timeDiffMs: number
): number => {
  // Convert distance from meters to kilometers
  const distanceKm = distance / 1000;
  // Convert time from milliseconds to hours
  const timeHours = timeDiffMs / (1000 * 60 * 60);
  
  // Avoid division by zero
  if (timeHours <= 0) return 0;
  
  // Return speed in km/h
  return distanceKm / timeHours;
};
```

## API Security

### Token Protection
Environment variables:
```bash
# .env (added to .gitignore)
VITE_TELEGRAM_TOKEN=your_token_here
VITE_MAPBOX_TOKEN=your_token_here
```

Example .env.example:
```bash
# .env.example (in repository)
VITE_TELEGRAM_TOKEN=your_telegram_token_here
VITE_MAPBOX_TOKEN=your_mapbox_token_here
```

### Data Validation
Data integrity check:
```typescript
function validateIncomingData(data: any): boolean {
  // Check data structure
  if (!data || typeof data !== 'object') {
    return false;
  }
  
  // Check required fields
  const requiredFields = ['timestamp', 'coordinates'];
  for (const field of requiredFields) {
    if (!(field in data)) {
      return false;
    }
  }
  
  // Check data types
  if (typeof data.timestamp !== 'number') {
    return false;
  }
  
  return true;
}
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

## Rate Limiting

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

## Monitoring and Logging

### Local Logging
Logs are displayed in the terminal where the server is running

### Docker Logging
View container logs:
```bash
docker-compose logs -f
```

### Mobile Logs
1. Use Android Studio to view Android logs
2. Use Xcode to view iOS logs
3. Add console.log to code for debugging

## Updating the Application

### Local Development
1. Get latest changes from repository
2. Install new dependencies: `npm install`
3. Restart development server

### Docker (Production)
1. Get latest changes from repository
2. Rebuild and restart containers:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

### GitHub Pages
1. Make necessary code changes
2. Rebuild application: `npm run build:webauth`
3. Commit and push changes:
   ```bash
   git add .
   git commit -m "Application update"
   git push origin main
   ```

If you use GitHub Actions, the application will be updated automatically.

## API Limitations and Known Issues

### Telegram Web App Limitations
1. Works only within Telegram
2. Limited access to some browser APIs
3. Requires HTTPS for full functionality

### Mapbox Limitations
1. Request limits
2. Registration required to get token
3. Usage restrictions

## Problem Solutions

### White Screen on Load
1. Check browser console (F12) for errors
2. Ensure resource paths in index.html start with "./", not "/"
3. Check that all necessary files were uploaded to GitHub Pages

### Resource Loading Errors (404)
1. Ensure the `distWebAuth` folder contains all necessary files
2. Check that GitHub Pages is configured for the correct folder
3. Ensure Vite configuration has `base: './'` parameter

### Routing Issues
If you use client-side routing, create a `404.html` file in the `distWebAuth` folder with the content of `index.html`:
```bash
cp distWebAuth/index.html distWebAuth/404.html
```

### Geolocation Errors
1. Check location permissions in browser
2. Ensure HTTPS is used (except localhost)
3. Check device privacy settings

### Telegram Authentication Issues
1. Ensure bot token is set in environment variables
2. Check that Web App URL is correctly configured in @BotFather
3. Ensure the application opens within Telegram