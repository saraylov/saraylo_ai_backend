# SARAYLO - Quantum Running Coach
## Developer Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation and Setup](#installation-and-setup)
4. [Project Structure](#project-structure)
5. [Application Components](#application-components)
6. [Component Development](#component-development)
7. [Styling and Design](#styling-and-design)
8. [Testing](#testing)
9. [Building and Deployment](#building-and-deployment)
10. [Mobile Development](#mobile-development)
11. [API Integrations](#api-integrations)
12. [State Management](#state-management)
13. [Performance Optimization](#performance-optimization)
14. [Security](#security)
15. [Best Practices](#best-practices)
16. [Troubleshooting](#troubleshooting)
17. [Contributing](#contributing)

---

## Introduction

This document is intended for developers who want to contribute to the development of the SARAYLO application. It covers the installation process, project structure, architecture, and development best practices.

## System Requirements

### For Web Development
- Node.js version 20 or higher
- npm (comes with Node.js)
- Git (for version control)
- Modern text editor or IDE (VS Code recommended)

### For Mobile Development
- Android Studio (for Android)
- Xcode (for iOS, macOS only)
- JDK 11 or higher

### For Docker Deployment
- Docker and Docker Compose

## Installation and Setup

### Cloning the Repository
```bash
git clone https://github.com/saraylov/saraylo_web_app.git
cd saraylo_web_app
```

### Installing Dependencies
```bash
npm install
```

This command installs all necessary dependencies:
- Svelte and related libraries
- Vite as bundler
- TypeScript for typing
- Telegram Web Apps SDK
- Mapbox GL JS
- Capacitor for mobile build

### Environment Variables Configuration
1. Copy the [.env.example](file://e:/DevBuild/AI/AI%20Running/saraylo_web_app/.env.example) file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open the [.env](file://e:/DevBuild/AI/AI%20Running/saraylo_web_app/.env) file and replace `your_telegram_bot_token_here` with your actual Telegram bot token

**IMPORTANT**: The [.env](file://e:/DevBuild/AI/AI%20Running/saraylo_web_app/.env) file is added to [.gitignore](file://e:/DevBuild/AI/AI%20Running/saraylo_web_app/.gitignore) and will never be committed to the repository for security.

## Project Structure
```
saraylo_web_app/
├── src/                    # Application source code
│   ├── components/         # Svelte components
│   ├── utils/              # Utilities and stores
│   ├── styles/             # CSS styles
│   ├── assets/             # Static resources
│   ├── App.svelte          # Main application component
│   ├── main.ts             # Application entry point
│   └── app.css             # Global application styles
├── public/                 # Public files
├── Documentation/          # Project documentation
├── android/                # Android project (Capacitor)
├── ios/                    # iOS project (Capacitor)
├── dist/                   # Web build
├── distWebAuth/            # Build with authentication
├── .env.example            # Environment variables example file
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── index.html              # Main HTML page
├── package.json            # npm configuration
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration
└── viteWebAuth.config.ts   # Vite configuration for WebAuth
```

## Application Components

### Main Components

#### App.svelte
The main application component that contains:
- Navigation structure
- Main content
- Bottom navigation bar

#### Training.svelte
The main workout component with integration of all systems:
- Mapbox map initialization
- Geolocation tracking
- Workout statistics collection
- Audio assistant integration

#### AssessmentTraining.svelte
Assessment workout component:
- 5 intensity zones (blue, green, yellow, orange, red)
- Speed data collection during workout
- Calculation of personal intensity zones

#### WorkoutButton.svelte
Workout button component with unique hold mechanics:
- 2.5-second hold to start
- Visual indication through CircularProgressBar
- State switching (start, stop, pause, resume)

### Utilities

#### workoutStore.ts
Central workout state store:
- State management (idle, running, paused)
- Statistics storage (time, distance, speed)
- Control functions (start, pause, resume, stop)

#### audioAssistant.ts
Class for working with Web Speech API:
- Message queue for sequential playback
- Speech synthesis parameter configuration
- Error handling

#### calibrationCalculator.ts
Utilities for calibration and calculations:
- Kalman filter for data smoothing
- Distance calculation using Haversine formula
- Speed calculation

## Component Development

### Creating a New Component
1. Create a new file in the `src/components/` folder with the `.svelte` extension
2. Use the following structure:

```svelte
<script lang="ts">
  // Imports
  import { onMount, onDestroy } from 'svelte';
  
  // Variables
  let componentVariable: string = '';
  
  // Functions
  function handleAction(): void {
    // Component logic
  }
  
  // Lifecycle
  onMount(() => {
    // Initialization
  });
  
  onDestroy(() => {
    // Resource cleanup
  });
</script>

<!-- Markup -->
<div class="component-class">
  <h2>Component Header</h2>
  <button on:click={handleAction}>Action Button</button>
</div>

<!-- Styles -->
<style>
  .component-class {
    /* Component styles */
  }
</style>
```

### Working with Stores
To create a reactive store:

```typescript
import { writable, derived } from 'svelte/store';

// Creating a writable store
export const myStore = writable<DataType>(initialData);

// Creating a derived store
export const formattedData = derived(
  myStore,
  ($myStore) => {
    // Data transformation
    return formatData($myStore);
  }
);

// Usage in components
import { myStore } from '../utils/myStore';

// Subscription
myStore.subscribe((value) => {
  // React to changes
});

// Update
myStore.update((data) => ({
  ...data,
  newValue: updatedValue
}));

// Set
myStore.set(newData);
```

### Working with TypeScript
Use strict typing for all components:

```typescript
// Interfaces for data
interface WorkoutData {
  startTime: number | null;
  elapsedTime: number;
  // ... other fields
}

// Types for functions
function calculateDistance(
  lat1: number, 
  lon1: number, 
  lat2: number, 
  lon2: number
): number {
  // Implementation
}
```

## Styling and Design

### Color Scheme
Main colors:
- Primary blue: `#00BFFF`
- Primary pink: `#FF1493`
- Deep black: `#000000`
- Background gradient: from `#000033` to `#33001a`

### Glassmorphism Effect
Implementation through CSS:
```css
.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
}
```

### Responsive Design
Use CSS media queries:
```css
.component {
  /* Default styles */
}

@media (max-width: 768px) {
  .component {
    /* Styles for mobile devices */
  }
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

### Compatibility Testing
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile devices (Android 7+, iOS 12+)
- Tablets and desktop computers

## Building and Deployment

### Local Development
```bash
# Main application
npm run dev

# Application with Telegram authentication
npm run dev:webauth

# Using PowerShell scripts
.\run_dev.ps1
```

### Production Build
```bash
# Build main application
npm run build

# Build application with authentication
npm run build:webauth

# Preview build
npm run preview
npm run preview:webauth
```

## Mobile Development

### Preparation
1. Ensure necessary tools are installed:
   - Android Studio for Android
   - Xcode for iOS (macOS only)
   - JDK 11 or higher

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build web application:
   ```bash
   npm run build
   ```

4. Sync web resources with native projects:
   ```bash
   npm run cap:sync
   ```

### Working with Android
1. Add Android platform (if not already added):
   ```bash
   npm run cap:add:android
   ```

2. Open project in Android Studio:
   ```bash
   npm run cap:open:android
   ```

3. To run on device or emulator:
   ```bash
   npm run cap:run:android
   ```

### Working with iOS (macOS only)
1. Add iOS platform (if not already added):
   ```bash
   npm run cap:add:ios
   ```

2. Open project in Xcode:
   ```bash
   npm run cap:open:ios
   ```

## API Integrations

### Telegram Web App API
Integration with Telegram for authentication:
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

### Mapbox GL JS API
Map initialization:
```typescript
import mapboxgl from 'mapbox-gl';

// Set access token
mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';

// Create map
const map = new mapboxgl.Map({
  container: 'map-container',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [30.3158, 59.9343],
  zoom: 10
});
```

### Web Speech API
Speech synthesis:
```typescript
function speakText(text: string): void {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  }
}
```

## State Management

### Workout Store (src/utils/workoutStore.ts)
Central element for workout state control:
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

### State Functions
- `startWorkout()`: Start workout
- `pauseWorkout()`: Pause workout
- `resumeWorkout()`: Resume workout
- `stopWorkout()`: Stop workout

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

### Environment Variables
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
Telegram data validation:
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

## Best Practices

### Code Structure
1. Separate logic and presentation
2. Use strict typing
3. Comment complex logic
4. Follow consistent coding style

### Performance
1. Minimize DOM elements
2. Use reactive variables only when necessary
3. Avoid heavy computations in components
4. Optimize animations (prefer CSS over JavaScript)

### Security
1. Don't store sensitive data in code
2. Use environment variables for tokens
3. Validate all input data
4. Keep dependencies updated

## Troubleshooting

### Common Errors and Solutions

#### "Port already in use"
```bash
# Find process using port
netstat -ano | findstr :5173
# Terminate process
taskkill /PID <process_number> /F
```

#### "Node.js not found"
1. Ensure Node.js is installed
2. Check that Node.js is added to PATH
3. Restart terminal after installation

#### "npm install fails"
1. Check internet connection
2. Clear npm cache: `npm cache clean --force`
3. Try different registry: `npm config set registry https://registry.npmjs.org/`

### Debugging
1. Use browser console for debugging
2. Add console.log for tracking execution
3. Use browser developer tools
4. Check for errors in terminal during startup

## Contributing

### Development Process
1. Create a branch for new feature: `git checkout -b feature/new-feature`
2. Make changes and commit them
3. Push changes to repository: `git push origin feature/new-feature`
4. Create Pull Request

### Coding Conventions
1. Use camelCase for variables and functions
2. Use PascalCase for components
3. Name files according to their content
4. Comment complex logic

### Documenting Changes
1. Update documentation when changing functionality
2. Add comments to code
3. Create tests for new functionality

## Contacts and Support

For questions and support, contact:
- Project repository: https://github.com/saraylov/saraylo_web_app
- Telegram bot: @Saraylo_bot
- Documentation: see files in Documentation folder