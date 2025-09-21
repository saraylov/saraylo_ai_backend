# SARAYLO - Quantum Running Coach
## Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Dependency Installation](#dependency-installation)
3. [Local Development](#local-development)
4. [Production Build](#production-build)
5. [GitHub Pages Deployment](#github-pages-deployment)
6. [Mobile Build](#mobile-build)
7. [Docker Deployment](#docker-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Application Updates](#application-updates)
10. [Monitoring and Performance](#monitoring-and-performance)
11. [Backup and Recovery](#backup-and-recovery)

---

## System Requirements

### For Web Development:
- Node.js version 20 or higher
- npm (comes with Node.js)
- Git (for version control)

### For Mobile Development:
- Android Studio (for Android)
- Xcode (for iOS, macOS only)
- JDK 11 or higher

### For Docker Deployment:
- Docker and Docker Compose

## Dependency Installation

### 1. Cloning the Repository
```bash
git clone https://github.com/saraylov/saraylo_web_app.git
cd saraylo_web_app
```

### 2. Installing Node.js Dependencies
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

## Local Development

### Option 1: Main Application
```bash
npm run dev
```
Application will be available at: http://localhost:5173

### Option 2: Application with Telegram Authentication
```bash
npm run dev:webauth
```
Application will be available at: http://localhost:5177

### Option 3: Using PowerShell Scripts
```powershell
.\run_dev.ps1
```

## Production Build

### Building the Main Application
```bash
npm run build
```
Built files will be located in the `dist/` folder.

### Building the Application with Authentication
```bash
npm run build:webauth
```
Built files will be located in the `distWebAuth/` folder.

### Previewing the Build
```bash
# For main application
npm run preview

# For application with authentication
npm run preview:webauth
```

## GitHub Pages Deployment

### Preparation
1. Ensure you have the latest version of Node.js (20 or higher) installed
2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the application:
   ```bash
   npm run build:webauth
   ```

### Manual Deployment
1. Commit the contents of the `distWebAuth` folder to your repository:
   ```bash
   git add distWebAuth
   git commit -m "Add web application with Telegram authentication"
   git push origin main
   ```

2. Go to repository settings on GitHub:
   - Open the "Settings" tab
   - Scroll to the "Pages" section

3. Configure GitHub Pages:
   - In the "Source" section, select "Deploy from a branch"
   - In the "Branch" dropdown, select the branch (usually `main`)
   - In the "Folder" field, select `/distWebAuth`
   - Click "Save"

### Automatic Deployment with GitHub Actions
Create a file `.github/workflows/deploy-webauth.yml`:
```yaml
name: Deploy WebAuth App to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build
        run: npm run build:webauth
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./distWebAuth
```

Commit and push the workflow file:
```bash
git add .github/workflows/deploy-webauth.yml
git commit -m "Add GitHub Actions for web application deployment with authentication"
git push origin main
```

### Setting up Web App in Telegram
1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Select your bot (@Saraylo_bot)
3. Send the command `/setmenubutton`
4. Select the bot from the list
5. Enter your application URL: `https://your-username.github.io/repository-name/`
6. Enter text for the menu button (e.g., "Open Application")

## Mobile Build

### Preparation
1. Ensure necessary tools are installed:
   - Android Studio for Android
   - Xcode for iOS (macOS only)
   - JDK 11 or higher

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the web application:
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

### Permissions for Mobile Applications
The following permissions have been added to the `android/app/src/main/AndroidManifest.xml` file for proper mobile application operation on Android:
- `ACCESS_COARSE_LOCATION` and `ACCESS_FINE_LOCATION` - for location determination
- `ACCESS_BACKGROUND_LOCATION` - for background geolocation operation
- `POST_NOTIFICATIONS` - for sending notifications
- `WAKE_LOCK` and `SCHEDULE_EXACT_ALARM` - for background tasks
- `ACCESS_NETWORK_STATE` - for network state checking

### Capacitor Scripts
The following scripts have been added to package.json for convenient work:
- `npm run cap:sync` - Sync web resources with native projects
- `npm run cap:open:android` - Open Android project in Android Studio
- `npm run cap:open:ios` - Open iOS project in Xcode
- `npm run cap:run:android` - Run application on Android device or emulator

## Docker Deployment

### Local Build and Run
1. Build and run the application:
   ```bash
   docker-compose up -d
   ```

2. Open browser and go to: http://localhost:3003

### Stopping the Application
```bash
docker-compose down
```

### Docker Configuration
The `Dockerfile` contains a multi-stage build:
1. **Build stage**: Install dependencies and build application
2. **Production stage**: Copy built application to production image

The `docker-compose.yml` file configures:
- Port mapping (3003:80)
- Volume mounting for logs
- nginx as web server

### Docker Security
Configuration includes:
- HTTP security headers
- Access rights limitation
- Image size minimization
- Non-root user usage

## Troubleshooting

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

### Mobile Issues

#### Android
1. **Gradle sync failed**: Try "File" → "Sync Project with Gradle Files" in Android Studio
2. **Build errors**: Check that you're using a compatible version of Android Studio and SDK
3. **Permission dialog not showing**: Ensure permissions are correctly declared in AndroidManifest.xml

#### iOS
1. **CocoaPods errors**: Run `cd ios && pod install` to update pods
2. **Signing errors**: Ensure your Apple Developer account is correctly configured in Xcode

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

### Logging and Debugging

#### Local Development
Logs are displayed in the terminal where the server is running

#### Docker
View container logs:
```bash
docker-compose logs -f
```

#### Mobile Applications
1. Use Android Studio to view Android logs
2. Use Xcode to view iOS logs
3. Add console.log to code for debugging

## Application Updates

### Local Development
1. Get latest changes from repository
2. Install new dependencies:
   ```bash
   npm install
   ```
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
2. Rebuild application:
   ```bash
   npm run build:webauth
   ```
3. Commit and push changes:
   ```bash
   git add .
   git commit -m "Application update"
   git push origin main
   ```

If you use GitHub Actions, the application will be updated automatically.

## Monitoring and Performance

### Local Development
- Hot reload when files change
- Source maps for debugging
- Unoptimized builds for fast development

### Docker (Production)
- Optimized build
- Minified files
- Gzip compression
- Static resource caching
- Security through headers

### Performance
Performance optimization recommendations:
1. Minimize DOM elements
2. Use reactive variables only when necessary
3. Avoid heavy computations in components
4. Optimize animations (prefer CSS over JavaScript)

## Backup and Recovery

### Backup
1. Regularly commit changes to Git
2. Use GitHub for repository storage
3. Create tags for stable versions:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### Recovery
1. Clone repository from GitHub
2. Install dependencies: `npm install`
3. Restore environment variables from .env.example

## Conclusion

This guide covers all aspects of deploying and running the SARAYLO application. By following these instructions, you can successfully launch the application in various environments - from local development to production on mobile devices and the web.

If problems occur, it is recommended to:
1. Check logs and browser console
2. Ensure all dependencies are installed
3. Check environment variable configuration
4. Refer to documentation for specific technologies (Svelte, Vite, Capacitor, Docker)