# Deep-Sea — Phase 4 Design System Summary

**Phase 4 Deliverable | February 2, 2026**

---

## 1. Overview

Phase 4 delivers a complete design system for Deep-Sea, implemented as a functional React + TypeScript prototype. The design establishes a purple-themed, touch-optimized interface inspired by iOS design patterns, targeting both macOS development and Raspberry Pi 4 production with a 7" touchscreen (1280x720).

This document catalogs the delivered design system, extracts key design specifications, and maps the design to the Must-Have features defined in Phase 2.

---

## 2. Deliverable Location

All Phase 4 design assets are located in:

```
docs/04-ui-ux-design/
```

**IMPORTANT:** This directory is the source of truth for the design system. Do not modify files in this directory. All specifications should be extracted from the prototype and documented here for reference during architecture and development phases.

---

## 3. Live Prototype

**Figma Source:** [https://www.figma.com/make/SzayRR0qTKkMH1FFxC4HGr/Phish-Concert-Streaming-App]

**Local Prototype:**
- Run `npm install` in `docs/04-ui-ux-design/`
- Run `npm run dev` to start the development server
- Access at `http://localhost:5173`

The prototype is a functional React application demonstrating all primary screens, navigation patterns, and interactive components.

---

## 4. Directory Contents

### 4.1 Project Structure

```
docs/04-ui-ux-design/
├── README.md                    # Figma export metadata and run instructions
├── ATTRIBUTIONS.md              # Third-party credits (shadcn/ui, Unsplash)
├── package.json                 # Dependencies and build scripts
├── index.html                   # Application entry point
├── vite.config.ts              # Build configuration
├── postcss.config.mjs          # PostCSS configuration
├── guidelines/
│   └── Guidelines.md           # Design system guidelines template
└── src/
    ├── main.tsx                # React application bootstrap
    ├── app/
    │   ├── App.tsx             # Root application component
    │   ├── routes.ts           # React Router configuration
    │   ├── Layout.tsx          # Shared layout wrapper
    │   ├── screens/            # Main application screens (6 total)
    │   ├── components/         # Custom components (13+)
    │   └── store/              # State management (Zustand)
    └── styles/
        ├── theme.css           # Design tokens and CSS variables
        ├── tailwind.css        # Tailwind CSS imports
        ├── fonts.css           # Typography definitions
        └── index.css           # Global styles
```

### 4.2 Application Screens (6)

| Screen | File | Purpose |
|--------|------|---------|
| **Welcome** | `WelcomeScreen.tsx` | App entry point with primary actions |
| **Player** | `PlayerScreen.tsx` | Full now-playing interface with metadata and controls |
| **Browse** | `BrowseScreen.tsx` | Show discovery and date-based lookup |
| **Collections** | `CollectionsScreen.tsx` | Personal curation and favorites |
| **History** | `HistoryScreen.tsx` | User's listening history |
| **Tour Detail** | `TourDetailScreen.tsx` | Show list for a specific tour |

### 4.3 Custom Components (13+)

| Component | Purpose |
|-----------|---------|
| **Equalizer** | Animated visual indicator (compact + large sizes) |
| **PlayerControls** | Play/pause, previous, next, skip, rewind buttons |
| **ProgressBar** | Track progress with scrubbing |
| **VolumeControl** | Volume slider with mute toggle |
| **TrackList** | Scrollable setlist with jump-to-track |
| **NowPlayingBar** | Persistent player bar for non-player screens |
| **TouchDatePicker** | Touch-optimized date selector |
| **ShowCard** | Show preview card with metadata |
| **TourCard** | Tour preview card |
| **TopNav** | Top navigation bar |
| **BottomNav** | Bottom navigation with 4-5 primary tabs |
| **PrimaryButton** | Primary action button component |
| **ImageWithFallback** | Image component with fallback handling |

### 4.4 UI Component Library

The prototype uses **shadcn/ui** (Radix UI primitives + Tailwind CSS), providing 40+ production-ready components including:
- Accordion, Alert Dialog, Avatar, Badge, Button
- Card, Checkbox, Dialog, Drawer, Dropdown Menu
- Input, Label, Popover, Progress, Radio Group
- Scroll Area, Select, Separator, Sheet, Slider
- Switch, Tabs, Toast (Sonner), Tooltip
- And more...

All components are touch-friendly and fully customizable via Tailwind utilities.

---

## 5. Design Specifications

### 5.1 Color Palette

**Base Purple Scale:**
```
--purple-50:  #f5f3ff
--purple-100: #ede9fe
--purple-200: #ddd6fe
--purple-300: #c4b5fd
--purple-400: #a78bfa
--purple-500: #8b5cf6
--purple-600: #7c3aed
--purple-700: #6d28d9
--purple-800: #5b21b6
--purple-900: #4c1d95
--purple-950: #2e1065
```

**Deep Purple Gradients:**
```
--deep-purple-start: #1a0b2e  (Darkest - top of gradient)
--deep-purple-mid:   #2d1b4e  (Middle)
--deep-purple-end:   #4c1d95  (Lightest - bottom of gradient)
```

**Semantic Colors (Dark Theme):**
```
Background:         linear-gradient(180deg, #1a0b2e → #2d1b4e → #4c1d95)
Foreground:         #f0f0f0
Primary:            #a78bfa (Purple-400)
Primary Hover:      #c4b5fd (Purple-300)
Card:               rgba(139, 92, 246, 0.15)
Border/Input:       rgba(167, 139, 250, 0.3)
Success:            #10b981 (Green)
Warning:            #f59e0b (Amber)
Destructive:        #ef4444 (Red)
```

**Equalizer Gradient:**
```
Dark:  #5b21b6 (Purple-800)
Mid:   #7c3aed (Purple-600)
Light: #a78bfa (Purple-400)
```

### 5.2 Typography

**Font Stack:**
```css
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif
```

**iOS-Inspired Type Scale:**
```
Display:  2.5rem (40px)  | Weight: 500 | Line-height: 1.1  | Letter-spacing: -0.03em
Title:    1.75rem (28px) | Weight: 500 | Line-height: 1.2  | Letter-spacing: -0.02em
H1:       2rem (32px)    | Weight: 500 | Line-height: 1.2  | Letter-spacing: -0.02em
H2:       1.5rem (24px)  | Weight: 500 | Line-height: 1.3  | Letter-spacing: -0.01em
H3:       1.25rem (20px) | Weight: 500 | Line-height: 1.4
H4:       1rem (16px)    | Weight: 500 | Line-height: 1.5
Body:     1rem (16px)    | Weight: 400 | Line-height: 1.5
Caption:  0.875rem (14px)| Weight: 400 | Line-height: 1.4  | Opacity: 0.7
```

**Font Weights:**
```
Medium: 500 (headings, buttons, labels)
Normal: 400 (body text, inputs)
```

### 5.3 Spacing System

**8-Point Grid:**
```
--spacing-1:  4px   (0.25rem)
--spacing-2:  8px   (0.5rem)
--spacing-3:  12px  (0.75rem)
--spacing-4:  16px  (1rem)
--spacing-5:  24px  (1.5rem)
--spacing-6:  32px  (2rem)
--spacing-7:  48px  (3rem)
--spacing-8:  64px  (4rem)
```

**Touch Targets:**
```
--touch-target: 44px (minimum for all interactive elements)
```

All interactive elements (buttons, controls, navigation items) meet or exceed the 44px minimum for reliable touch input on the 7" touchscreen.

### 5.4 Border Radius

**iOS-Inspired Rounding:**
```
--radius:    0.75rem (12px)  [Base radius]
--radius-sm: 0.5rem (8px)    [Small elements]
--radius-md: 0.625rem (10px) [Medium elements]
--radius-lg: 0.75rem (12px)  [Large cards, panels]
--radius-xl: 1rem (16px)     [Extra large containers]
```

### 5.5 Shadows

**Subtle Depth:**
```
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)
```

Shadows are used sparingly to create subtle elevation and hierarchy on cards and modals against the dark gradient background.

---

## 6. Navigation Architecture

### 6.1 Primary Navigation (Bottom Nav)

The prototype uses a bottom navigation bar with 4-5 primary sections:
- **Home/Welcome** - App entry point
- **Browse** - Show discovery and search
- **Collections** - Personal curation and favorites
- **History** - Listening history

### 6.2 Screen Flow

```
Welcome Screen
├─→ Player Screen (now playing)
├─→ Browse Screen
│   └─→ Tour Detail Screen (tour → shows)
├─→ Collections Screen
└─→ History Screen
```

### 6.3 Persistent Elements

- **Now Playing Bar:** Appears on all non-player screens when audio is active. Shows compact Equalizer, current show/track, and basic controls. User can hide/show as needed.
- **Player Screen:** Full-screen now-playing interface accessible via Now Playing Bar or direct navigation.

---

## 7. Feature Coverage

This section maps the Must-Have features from Phase 2 (Requirements Definition) to the delivered design system.

| Must-Have Feature | Design Implementation | Notes |
|-------------------|----------------------|-------|
| **Date-Based Show Lookup** | `TouchDatePicker` component in Browse screen | Touch-optimized date selector with visual constraints for available show dates |
| **Gapless Playback** | `PlayerControls` + state management | UI design complete; backend implementation deferred to Phase 6 |
| **Full Player Screen** | `PlayerScreen.tsx` (2-column layout) | Left: show metadata + track list. Right: now playing card with controls |
| **Persistent Now Playing Bar** | `NowPlayingBar` component | Compact bar with Equalizer, show info, and media controls. Hideable by user |
| **Animated Visual Indicator** | `Equalizer` component (compact + large) | 5-bar animated equalizer with purple gradient. Compact (40px) and large (120px) sizes |
| **Track List with Jump-to-Track** | `TrackList` component with `ScrollArea` | Scrollable setlist with tap-to-play. Current track highlighted |
| **Favorites** | Collections screen + heart icon in Player | Personal collections with favorites as a dedicated section |
| **Random Show Selection** | Browse screen action | "Pick something for me" feature (implementation in BrowseScreen) |
| **Resume on Reconnect** | State management (Zustand `playerStore`) | Player state persisted across sessions. UI reflects state restoration |
| **Filter Unavailable Shows** | Data layer filtering | Not visible in UI; validation happens before rendering |
| **Touch-Friendly UI** | 44px minimum touch targets throughout | All interactive elements sized and spaced for reliable touch input |
| **Personal Curation System** | `CollectionsScreen` + state management | Create and manage collections, playlists, and favorites |

### Additional Features Addressed

| Feature | Design Implementation |
|---------|----------------------|
| **Listening History** | `HistoryScreen` with recent show cards |
| **Tour Browsing** | `TourCard` components + `TourDetailScreen` |
| **Jump to Highlight** | "Jump to Highlight" button in Player when `jam_starts_at_second` is available |
| **Waveform Images** | Image support in show/track cards (not yet implemented in prototype) |

---

## 8. Technology Stack

### 8.1 Prototype Stack

The Phase 4 prototype is built with:

- **React 18.3.1** - UI framework
- **TypeScript** - Type safety
- **Vite 6.3.5** - Build tool and dev server
- **Tailwind CSS 4.1.12** - Utility-first CSS framework
- **shadcn/ui** - Component library (Radix UI + Tailwind)
- **React Router 7.13.0** - Client-side routing
- **Zustand 5.0.11** - State management
- **Motion (Framer Motion) 12.23.24** - Animation library
- **Lucide React 0.487.0** - Icon library

### 8.2 Architecture Implications for Phase 5

The prototype demonstrates:
- **Component-based architecture** with clear separation of concerns
- **State management patterns** suitable for a desktop application
- **Responsive layout** that adapts to different screen sizes
- **Animation system** for visual feedback and transitions

Phase 5 (Technical Architecture Decision) will evaluate how to integrate this design with:
- **miniaudio** (Phase 3 audio engine decision)
- **Backend framework** (FastAPI or PyQt5 webview wrapper)
- **Python ↔ JavaScript bridge** for audio control and API integration

The prototype validates that a web-based UI (React + Tailwind) is feasible for the project and provides a concrete reference for development.

---

## 9. Design Principles Demonstrated

### 9.1 Touch-First Design

Every interactive element meets the 44px minimum touch target size. Buttons, controls, and navigation items are generously sized with adequate spacing to prevent mis-taps on the 7" touchscreen.

### 9.2 iOS-Inspired Polish

- Smooth animations and transitions
- Generous use of blur effects (`backdrop-blur-lg`) on cards
- Rounded corners (12px base radius)
- System font stack for native feel
- Subtle shadows for depth
- Minimalist, content-focused layouts

### 9.3 Dark Theme Optimization

The deep purple gradient background creates a unique visual identity while reducing eye strain. All text, borders, and interactive elements are optimized for legibility against the dark theme.

### 9.4 Performance Considerations

- Lightweight animation library (Motion vs. full Framer Motion)
- Efficient state management (Zustand)
- Lazy loading for routes (React Router)
- CSS variables for theme consistency
- Tailwind's utility-first approach for minimal CSS bundle size

---

## 10. Open Questions for Phase 5

Phase 4 delivers the design system, but several technical questions remain for Phase 5 (Technical Architecture Decision):

1. **UI Framework Integration:** How do we integrate this React prototype with the Python backend and miniaudio engine?
   - Option A: FastAPI backend serving a React build + webview wrapper
   - Option B: PyQt5 webview embedding the React app
   - Option C: Tauri or Electron-like approach (unlikely given Python audio engine)

2. **State Management Bridge:** How does the UI state (Zustand) communicate with the Python audio engine?
   - WebSocket connection?
   - REST API polling?
   - IPC mechanism?

3. **Asset Handling:** How are album art, waveform images, and other assets fetched and cached?
   - Client-side caching in the React app?
   - Backend proxy with cache?

4. **Build & Packaging:** How is the React app bundled and distributed with the Python backend for Raspberry Pi deployment?
   - Static build included in Python package?
   - Separate web server?

These questions are explicitly deferred to Phase 5 and are not blockers for Phase 4 completion.

---

## 11. Next Steps

Phase 4 is complete. The design system is documented and the prototype is functional.

**Phase 5 (Technical Architecture Decision)** will:
1. Evaluate UI framework integration options (FastAPI + webview vs. PyQt5)
2. Design the Python ↔ JavaScript bridge architecture
3. Define the state management and communication protocols
4. Establish build and packaging strategy for macOS and Raspberry Pi
5. Create a technical architecture document for developer approval

**Phase 6 (Development)** will implement the application based on the approved architecture and this design system.

---

## 12. Credits

- **shadcn/ui:** Component library used under [MIT license](https://github.com/shadcn-ui/ui/blob/main/LICENSE.md)
- **Unsplash:** Placeholder images used under [Unsplash License](https://unsplash.com/license)

---

*Phase 4 Design System Summary v1.0 | Deep-Sea Project | February 2, 2026*
