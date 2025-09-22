# Bottom Control Panel Design

## Overall Description

The bottom control panel is a transparent glass panel in iOS 26 style, fixed at the bottom of the screen. The panel features a modern design with a background blur effect (backdrop-filter: blur) that creates a sense of depth and visual connection with the application content.

## Position and Dimensions

The panel is positioned at the bottom of the screen and stretches across the full width with small side margins. It uses a modern adaptive approach, automatically adjusting to device safe areas (safe-area-inset) for proper display on devices with notches and curved screen edges.

## Visual Characteristics

### Color Scheme
- Main background gradient: linear gradient from rgba(0, 0, 0, 0.3) to rgba(51, 51, 51, 0.3)
- Blur effect: blur(10px) to create a glass effect
- Border color: rgba(255, 255, 255, 0.1) for a barely visible outline
- Corner radius: --border-radius variable, adaptively changing from 10px to 25px

### Shadows and Effects
- Shadow: 0 8px 32px rgba(0, 191, 255, 0.1) to create a floating effect above the content
- Adaptive padding that changes depending on screen size

## Control Elements

The panel contains five navigation elements evenly distributed across the width:
1. Statistics - chart icon with label
2. Health - heart icon with label
3. Start workout - central circular button with running icon
4. Devices - smart device icon with label
5. Profile - human silhouette icon with label

Each navigation element is implemented as an interactive button with appropriate accessibility attributes (role="button", tabindex="0", aria-label).

## Central Button

The central "Start workout" button is visually emphasized:
- Larger size compared to other buttons
- Circular shape
- Runner icon sized 40x40 pixels
- Positioned in the center of the panel to draw attention

## Adaptability

The panel uses modern CSS functions for adaptability:
- clamp() for font sizes, padding and rounding
- Grid layout with even distribution of elements
- CSS variables for easy theming customization
- Support for safe zones for devices with notches

## Accessibility

All panel elements have:
- Clear accessibility labels (aria-label)
- Interactive states (hover, active)
- Labels under icons for better understanding of functions
- Appropriate sizes for touch interaction (variable --touch-target-min)

## Compatibility

The panel design is compatible with modern browsers and mobile devices, using:
- CSS Grid for layout
- CSS variables for theming
- Backdrop-filter for glass effect
- Flexbox for centering
- Adaptive measurement units (vw, clamp)