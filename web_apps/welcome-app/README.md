# SARAYLO Welcome Page

This is a Svelte-based welcome page for the SARAYLO Quantum Running Coach application. It features:

1. Animated logo and title appearance
2. Sound effects on element appearance
3. Glassmorphism design based on the project's design document
4. Responsive layout

## Features

- **Animated Entrance**: The logo and title fade in with scaling animations
- **Sound Effects**: Play subtle sound effects when elements appear
- **Glassmorphism Design**: Implements the glass-like panels from the design document
- **Responsive Layout**: Works on different screen sizes

## Design Elements

The page implements the following design elements from the SARAYLO design document:

- Miami Hit color scheme (`#00BFFF` blue and `#FF1493` pink)
- Glassmorphism effects with backdrop blur
- Proper typography sizing
- Centered layout with maximum width of 551px

## Technical Implementation

- Built with Svelte and Vite
- Uses Web Audio API for sound effects
- CSS transitions for smooth animations
- Responsive design with media queries

## Development

To run the development server:

```bash
npm run dev
```

To build for production:

```bash
npm run build
```