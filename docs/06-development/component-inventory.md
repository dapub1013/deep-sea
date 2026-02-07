# Phase 4 Component Inventory

**Document Purpose:** Comprehensive extraction of all React components from Phase 4 UI/UX design files to guide PyQt5 implementation.

**Generated:** 2026-02-07
**Source:** docs/04-ui-ux-design/src/app/

---

## Executive Summary

### Total Component Count

| Category | Count | Status |
|----------|-------|--------|
| **Custom Components** | 13 | Ready for Qt translation |
| **Screens** | 6 | Ready for Qt translation |
| **Layout Components** | 2 | Ready for Qt translation |
| **UI Library (shadcn/ui)** | ~50 | Reference only (use Qt equivalents) |
| **Total Custom/Screens** | **21** | **Implementation targets** |

### Component Complexity Distribution

- **Simple (< 50 lines):** 7 components (PrimaryButton, ProgressBar, ShowCard, TourCard, ImageWithFallback, TopNav, VolumeControl)
- **Medium (50-150 lines):** 8 components (Equalizer, PlayerControls, TrackList, Layout, WelcomeScreen, TourDetailScreen, HistoryScreen, CollectionsScreen)
- **Complex (> 150 lines):** 6 components (TouchDatePicker, NowPlayingBar, PlayerScreen, BrowseScreen, App, plus navigation logic)

---

## Components by Category

### 1. Navigation Components

| Component | File Path | Purpose | Layout | Dependencies | Complexity |
|-----------|-----------|---------|--------|--------------|------------|
| **TopNav** | `components/TopNav.tsx` | Top navigation bar with 2 icon buttons (Collections, History) | `flex-row` (horizontal) | lucide-react (Heart, Clock), react-router | Simple |
| **BottomNav** | `components/BottomNav.tsx` | **DEPRECATED** - Re-exports TopNav (legacy compatibility) | N/A | TopNav | N/A |
| **NowPlayingBar** | `components/NowPlayingBar.tsx` | Persistent bottom bar showing current playback, hideable with expand/collapse | `flex-row` main, `flex-col` for stacking | Equalizer, PlayerControls, motion/react (animations) | Complex |

**Key Patterns:**
- TopNav uses fixed positioning (`fixed top-0`)
- NowPlayingBar uses fixed bottom positioning with AnimatePresence for slide-in/out
- Both have backdrop-blur and shadow effects

---

### 2. Media/Player Components

| Component | File Path | Purpose | Layout | Dependencies | Complexity |
|-----------|-----------|---------|--------|--------------|------------|
| **Equalizer** | `components/Equalizer.tsx` | 5-bar animated purple gradient equalizer (compact 40px / large 120px) | `flex-row` (horizontal bars) | motion/react (animations) | Medium |
| **PlayerControls** | `components/PlayerControls.tsx` | Play/pause, previous, next, skip/rewind buttons (compact/large sizes) | `flex-row` (horizontal buttons) | lucide-react (Play, Pause, SkipBack, SkipForward, RotateCcw, RotateCw) | Medium |
| **ProgressBar** | `components/ProgressBar.tsx` | Seekable progress bar with time labels | `flex-col` (bar + time labels) | None | Simple |
| **VolumeControl** | `components/VolumeControl.tsx` | Volume slider with mute button | `flex-row` (button + slider) | lucide-react (Volume2, VolumeX), Slider (shadcn/ui) | Simple |
| **TrackList** | `components/TrackList.tsx` | Scrollable track list with play indicators, duration, jamchart badges | `flex-col` (vertical list) | lucide-react (Play) | Medium |

**Key Patterns:**
- Equalizer uses CSS custom properties for gradient colors (`--equalizer-dark`, `--equalizer-mid`, `--equalizer-light`)
- PlayerControls adapt sizing based on `size` prop
- ProgressBar handles click-to-seek interaction
- TrackList shows active track with pulsing indicator

---

### 3. Content/Display Components

| Component | File Path | Purpose | Layout | Dependencies | Complexity |
|-----------|-----------|---------|--------|--------------|------------|
| **ShowCard** | `components/ShowCard.tsx` | Display show metadata (date, venue, tour, rating, tags) | `flex-col` (vertical stack) | None | Simple |
| **TourCard** | `components/TourCard.tsx` | Display tour info (name, show count, date range) with chevron | `flex-row` (left content + right chevron) | lucide-react (ChevronRight) | Simple |

**Key Patterns:**
- Both cards use rounded corners (`rounded-xl`)
- Cards have backdrop-blur, borders, shadows
- Cards have active states (`active:scale-[0.98]`)
- Cards display badges/tags for metadata

---

### 4. Input Components

| Component | File Path | Purpose | Layout | Dependencies | Complexity |
|-----------|-----------|---------|--------|--------------|------------|
| **PrimaryButton** | `components/PrimaryButton.tsx` | Primary/secondary button variants with 44px min-height | Inline button | None | Simple |
| **TouchDatePicker** | `components/TouchDatePicker.tsx` | Touch-optimized calendar picker with month/year quick selection | `grid` (7-column calendar) + `flex-col` for month/year pickers | lucide-react (ChevronLeft, ChevronRight, Calendar) | Complex |

**Key Patterns:**
- PrimaryButton enforces 44px minimum touch target
- TouchDatePicker has 3 views: calendar, month picker, year picker
- TouchDatePicker disables unavailable dates

---

### 5. Utility Components

| Component | File Path | Purpose | Layout | Dependencies | Complexity |
|-----------|-----------|---------|--------|--------------|------------|
| **ImageWithFallback** | `components/figma/ImageWithFallback.tsx` | Image component with automatic error fallback to placeholder | Inline img | React (useState) | Simple |

**Key Patterns:**
- Uses base64-encoded SVG as fallback placeholder
- Stores original URL in data attribute for debugging

---

### 6. Screen Components

| Component | File Path | Purpose | Layout | Child Components | Complexity |
|-----------|-----------|---------|--------|------------------|------------|
| **WelcomeScreen** | `screens/WelcomeScreen.tsx` | Landing page with logo and 3 action buttons | `flex-col` centered | PrimaryButton | Medium |
| **PlayerScreen** | `screens/PlayerScreen.tsx` | Two-column player view: metadata/tracklist (left) + now playing/controls (right) | `grid grid-cols-2` | Equalizer, PlayerControls, ProgressBar, VolumeControl, TrackList, ScrollArea | Complex |
| **BrowseScreen** | `screens/BrowseScreen.tsx` | Tabbed interface (Calendar / Tours / Recent) for show discovery | `flex-col` with Tabs | TouchDatePicker, ShowCard, TourCard, Tabs, ScrollArea | Complex |
| **TourDetailScreen** | `screens/TourDetailScreen.tsx` | Grid of shows for a specific tour (3-column layout) | `grid grid-cols-3` | ShowCard | Medium |
| **CollectionsScreen** | `screens/CollectionsScreen.tsx` | User collections management (favorites, custom playlists) | `flex-col` with sections | ShowCard, ScrollArea | Medium |
| **HistoryScreen** | `screens/HistoryScreen.tsx` | Listening history with timestamps | `flex-col` | ShowCard, ScrollArea | Medium |

**Key Patterns:**
- All screens have sticky header with back button (ChevronLeft)
- All screens use `pb-32` (bottom padding) to avoid NowPlayingBar overlap
- PlayerScreen uses two-column grid layout
- BrowseScreen uses shadcn/ui Tabs component
- TourDetailScreen uses 3-column grid
- Screens with long content use ScrollArea

---

### 7. Layout/App Components

| Component | File Path | Purpose | Layout | Child Components | Complexity |
|-----------|-----------|---------|--------|------------------|------------|
| **Layout** | `Layout.tsx` | Main app wrapper with gradient background, conditional TopNav, persistent NowPlayingBar | `flex-col` | TopNav, NowPlayingBar, Outlet (react-router) | Medium |
| **App** | `App.tsx` | Root component providing RouterProvider | N/A | RouterProvider | Simple |

**Key Patterns:**
- Layout applies gradient background: `linear-gradient(180deg, #1a0b2e 0%, #2d1b4e 50%, #4c1d95 100%)`
- TopNav only shows on WelcomeScreen (`pathname === "/"`)
- NowPlayingBar is persistent across all screens

---

## Detailed Component Analysis

### Navigation Components

#### TopNav (TopNav.tsx)
```tsx
Structure: <nav> (fixed top)
  └─ <div flex-row> (container)
      └─ [2 buttons] (Collections, History)
           ├─ Icon (flex-col)
           └─ Label

Layout: QHBoxLayout
Widgets: QLabel (icons via Unicode/images), QLabel (text)
Icons: Heart (Collections), Clock (History)
Interactions: onClick → navigate to /collections or /history
Active State: Changes text color based on current route
ObjectName: "topNav"
```

**Qt Translation:**
- Container: QWidget with QHBoxLayout
- Buttons: QPushButton (2x) with QVBoxLayout inside (icon above text)
- Icons: QLabel with Unicode emoji or icon images
- Active state: Update QSS class on route change

**Notes:**
- BottomNav.tsx is deprecated and just re-exports TopNav
- Original design had bottom navigation; now uses top navigation

---

#### NowPlayingBar (NowPlayingBar.tsx)
```tsx
Structure: <motion.div> (fixed bottom, animated)
  ├─ <div flex-row> (main bar - clickable to expand)
  │   ├─ <button> Close (X)
  │   ├─ <div flex-col> Track info
  │   ├─ <Equalizer> (compact)
  │   └─ <PlayerControls> (compact)
  └─ <button> Hide/show toggle (ChevronDown)

When hidden: Floating button (bottom-right) with ChevronUp

Layout: QVBoxLayout (main) with QHBoxLayout for bar content
Widgets: QPushButton (close, toggle), QLabel (track info), Equalizer widget, PlayerControls widget
Animations: Slide in/out from bottom (Qt animations or fade in/out)
Icons: X, ChevronDown, ChevronUp
Interactions:
  - Click bar → navigate to /player
  - Click X → stop playback, hide bar
  - Click toggle → hide/show bar
  - Click controls → play/pause, previous, next
ObjectName: "nowPlayingBar"
```

**Qt Translation:**
- Main widget: QWidget with fixed bottom positioning
- Use QPropertyAnimation for slide-in/out effect
- Stacking: QVBoxLayout with bar + toggle button
- Bar content: QHBoxLayout (close | info | equalizer | controls)

**Complexity Notes:**
- Handles 3 states: visible, hidden, not-playing
- Animation transitions
- Propagates click events (bar vs. controls)
- Conditional rendering based on route (hide on /player)

---

### Media/Player Components

#### Equalizer (Equalizer.tsx)
```tsx
Structure: <div flex-row> (container)
  └─ [5 motion.div bars] (animated heights)

Sizes:
  - compact: 40x40px container, 5px bars, 3px gap, 32px max-height
  - large: 120x120px container, 16px bars, 8px gap, 96px max-height

Colors: 3-step gradient (--equalizer-dark → --equalizer-mid → --equalizer-light)
Animation: Each bar animates independently (200-600ms intervals)
Heights: Random 0.3-1.0 scale when playing, 0.3 when paused

Layout: QHBoxLayout with 5 QWidget bars
Widgets: 5 custom painted QWidgets or QLabels with gradient backgrounds
Animation: QTimer updating heights + QPropertyAnimation for smooth transitions
ObjectName: "equalizer"
```

**Qt Translation:**
- Container: QWidget with QHBoxLayout
- Bars: 5 QWidget with custom paintEvent for gradient (or use QSS gradient)
- Animation: QTimer (200-600ms staggered) updating height property
- Use QPropertyAnimation for smooth height changes (150ms easeOut)

**Implementation Notes:**
- Existing `ui/components/equalizer.py` already implemented (signature Phase 4 component)
- Verify bar count (5), colors, and sizing match Phase 4 specs

---

#### PlayerControls (PlayerControls.tsx)
```tsx
Structure: <div flex-row> (horizontal button row)
  ├─ [Optional] <button> Rewind (-30s)
  ├─ <button> Previous
  ├─ <button> Play/Pause (primary styled)
  ├─ <button> Next
  └─ [Optional] <button> Skip (+30s)

Sizes:
  - compact: 20px icons, 44px buttons, 44px play button
  - large: 28px icons, 56px buttons, 64px play button

Icons: RotateCcw, SkipBack, Play/Pause, SkipForward, RotateCw
Button styles:
  - Play/Pause: bg-primary (purple), circular
  - Others: transparent, circular, hover:bg-accent

Layout: QHBoxLayout
Widgets: 3-5 QPushButton (depends on optional rewind/skip)
Icons: QIcon from Unicode, images, or icon font
ObjectName: "playerControls"
```

**Qt Translation:**
- Container: QWidget with QHBoxLayout
- Buttons: QPushButton (circular with QSS)
- Play/Pause: Toggles icon between Play and Pause
- Connect signals: clicked() → onPlayPause, onPrevious, onNext, etc.

**Size Variants:**
- Compact: 44x44px buttons, smaller icons
- Large: 56x56px buttons (64x64px for play), larger icons

---

#### ProgressBar (ProgressBar.tsx)
```tsx
Structure: <div flex-col>
  ├─ <div> Progress bar (clickable)
  │   └─ <div> Filled portion
  └─ <div flex-row> Time labels
      ├─ <span> Current time
      └─ <span> Duration

Height: 8px bar
Colors: bg-muted (track), bg-primary (fill)
Interaction: Click to seek (calculate position percentage)

Layout: QVBoxLayout
Widgets: QSlider (for progress + seek), 2 QLabel (time labels)
ObjectName: "progressBar"
```

**Qt Translation:**
- Use QSlider (horizontal) with custom QSS styling
- Time labels: QHBoxLayout with 2 QLabel (left: current, right: duration)
- Connect valueChanged signal for seeking
- Format time as MM:SS

**Implementation Notes:**
- QSlider handles click-to-seek automatically
- Style slider groove (track) and handle (thumb) with QSS

---

#### VolumeControl (VolumeControl.tsx)
```tsx
Structure: <div flex-row>
  ├─ <button> Mute/Unmute icon
  └─ <Slider> Volume slider (0-100)

Icons: Volume2 (unmuted), VolumeX (muted)
Max width: 200px
Button: 44x44px touch target

Layout: QHBoxLayout
Widgets: QPushButton (mute toggle), QSlider (horizontal)
ObjectName: "volumeControl"
```

**Qt Translation:**
- Container: QWidget with QHBoxLayout
- Mute button: QPushButton toggling icon
- Volume slider: QSlider (0-100 range)
- Connect button clicked() → toggle mute
- Connect slider valueChanged() → update volume

---

#### TrackList (TrackList.tsx)
```tsx
Structure: <div flex-col> (vertical list)
  └─ [Track buttons]
      ├─ <div> Play icon or active indicator
      ├─ <div flex-col> Track title + badges
      └─ <div> Duration

Track button: 56px min-height
Active state: bg-accent, pulsing dot indicator
Jamchart badge: "🔥 Jamchart" (primary colored)

Layout: QVBoxLayout (scrollable)
Widgets: QPushButton per track
ObjectName: "trackList"
```

**Qt Translation:**
- Container: QScrollArea with QWidget + QVBoxLayout
- Track items: QPushButton with custom layout (icon | title | duration)
- Active track: Update QSS class, show pulsing animation (QPropertyAnimation)
- Badges: QLabel with styled background

**Implementation Notes:**
- Need to handle dynamic track loading
- Active track indicator uses CSS animation (translate to Qt animation)

---

### Content/Display Components

#### ShowCard (ShowCard.tsx)
```tsx
Structure: <button flex-col> (vertical stack)
  ├─ <div> Date (large text)
  ├─ <div> Venue (caption)
  ├─ [Optional] <div> Tour (italic caption)
  └─ [Optional] <div flex-row> Badges (rating, tags)

Min-height: 88px
Border: border-border
Background: backdrop-blur
Shadow: var(--shadow-md)
Active state: scale-[0.98]

Layout: QVBoxLayout
Widgets: QPushButton with QLabel children
ObjectName: "showCard"
```

**Qt Translation:**
- Base: QPushButton (clickable card)
- Content: QVBoxLayout with QLabel for each text element
- Badges: QHBoxLayout with styled QLabel widgets
- Use QSS for borders, shadows, rounded corners

**Display Fields:**
- Date: Large text (text-body font-medium)
- Venue: Caption text (text-caption)
- Tour: Italic caption (optional)
- Rating: Badge with ⭐ emoji
- Tags: Multiple badges (e.g., "SBD", "AUD")

---

#### TourCard (TourCard.tsx)
```tsx
Structure: <button flex-row> (horizontal layout)
  ├─ <div flex-col> (left - tour info)
  │   ├─ <div> Tour name
  │   └─ <div> Show count + date range
  └─ <ChevronRight> (right arrow)

Background: bg-card, backdrop-blur
Border: border-border
Shadow: var(--shadow-md)
Active state: scale-[0.98]

Layout: QHBoxLayout
Widgets: QPushButton with QLabel children + icon
ObjectName: "tourCard"
```

**Qt Translation:**
- Base: QPushButton
- Layout: QHBoxLayout (content | chevron)
- Content: QVBoxLayout with 2 QLabel
- Chevron: QLabel with Unicode arrow (→) or image

**Display Fields:**
- Tour name: Large text
- Show count: "X shows"
- Date range: "YYYY" or "YYYY-YYYY"

---

### Input Components

#### PrimaryButton (PrimaryButton.tsx)
```tsx
Structure: <button>

Variants:
  - primary: bg-primary, text-primary-foreground
  - secondary: bg-secondary, text-secondary-foreground

Min-height: 44px
Padding: 16px horizontal, 12px vertical
Border radius: 12px (rounded-xl)
Active state: scale-95
Shadow: var(--shadow-md)

Layout: N/A (standard button)
Widget: QPushButton
ObjectName: "primaryButton" (add variant as class)
```

**Qt Translation:**
- Standard QPushButton
- Use QSS for variants: `QPushButton[variant="primary"]` vs `QPushButton[variant="secondary"]`
- Set `variant` as Qt property for QSS targeting

**QSS Classes:**
- `.primaryButton.primary` → purple background
- `.primaryButton.secondary` → darker background

---

#### TouchDatePicker (TouchDatePicker.tsx)
```tsx
Structure: 3 views (calendar, month picker, year picker)

Calendar View:
  ├─ <div flex-row> Month navigation (prev | month year | next)
  ├─ <div grid-cols-7> Day labels (Su, Mo, Tu, We, Th, Fr, Sa)
  └─ <div grid-cols-7> Date buttons (blanks + dates)

Month Picker View:
  ├─ <div flex-row> Header (title | close button)
  └─ <div grid-cols-3> Month buttons (Jan-Dec)

Year Picker View:
  ├─ <div flex-row> Header (title | close button)
  └─ <div grid-cols-3> Year buttons (scrollable)

Button sizes: 44x44px (touch targets)
Available dates: Enabled styling
Selected date: bg-primary
Unavailable dates: Disabled, dimmed

Layout: QStackedWidget (switching between 3 views)
Widgets: Multiple QGridLayout (7-col calendar, 3-col month/year)
ObjectName: "touchDatePicker"
```

**Qt Translation:**
- Use QStackedWidget for 3 views
- Calendar view: QGridLayout (7 columns)
- Month/Year views: QGridLayout (3 columns)
- Navigation: QPushButton with ChevronLeft/Right icons
- Date buttons: QPushButton (44x44px) with enabled/disabled states
- Selected date: Highlight with QSS

**Complexity Notes:**
- Calculate calendar grid (first day of month, days in month)
- Filter available dates (enable/disable buttons)
- Handle month/year navigation
- Switching between 3 views

**Alternative:** Could use QCalendarWidget as base and customize styling

---

### Utility Components

#### ImageWithFallback (ImageWithFallback.tsx)
```tsx
Structure: <img> or <div> with fallback SVG

Behavior:
  - Loads image from src prop
  - On error: Shows base64-encoded placeholder SVG
  - Stores original URL in data-original-url attribute

Layout: Inline image
Widget: QLabel with QPixmap
ObjectName: "imageWithFallback"
```

**Qt Translation:**
- QLabel with QPixmap
- Use QNetworkAccessManager to load image from URL
- On error: Load placeholder from base64 or embedded resource
- Store original URL as Qt property for debugging

**Use Cases:**
- Album artwork (if added later)
- Band photos
- Venue images

---

### Screen Components

#### WelcomeScreen (WelcomeScreen.tsx)
```tsx
Structure: <div flex-col centered>
  ├─ <div> Logo (placeholder fish emoji in gradient box)
  └─ <div flex-col> 3 buttons
      ├─ PrimaryButton "Find a show" (primary)
      ├─ PrimaryButton "Random show" (secondary)
      └─ PrimaryButton "Today in History" (secondary)

Padding: p-8, pt-24 (top padding for nav), pb-24 (bottom padding)
Background: Inherited gradient from Layout
Max-width: md (768px)

Layout: QVBoxLayout (centered)
Widgets: QLabel (logo), 3 QPushButton
ObjectName: "welcomeScreen"
```

**Qt Translation:**
- Container: QWidget with QVBoxLayout
- Center items: Use layout alignment (AlignCenter)
- Logo: QLabel with styled background (gradient) + emoji or image
- Buttons: 3 QPushButton (1 primary variant, 2 secondary)

**Interactions:**
- "Find a show" → Navigate to BrowseScreen
- "Random show" → Load random show, navigate to PlayerScreen
- "Today in History" → Load today's historical show, navigate to PlayerScreen

**Implementation Notes:**
- Requires mockData or API client to fetch shows
- Need navigation/routing system (QStackedWidget?)

---

#### PlayerScreen (PlayerScreen.tsx)
```tsx
Structure: <div flex-col>
  ├─ <div flex-row> Header (home button | favorite button)
  └─ <div grid-cols-2> Two columns
      ├─ Left Column (flex-col)
      │   ├─ Show metadata card (date, venue, tour, rating, tags)
      │   └─ Track list card (scrollable)
      └─ Right Column (flex-col)
          └─ Now playing card (centered)
              ├─ Equalizer (large)
              ├─ Track title + jamchart button
              ├─ ProgressBar
              ├─ PlayerControls (large with rewind/skip)
              └─ VolumeControl

Header: Sticky, backdrop-blur
Bottom padding: pb-32 (for NowPlayingBar)
Grid: 50/50 split (grid-cols-2)

Layout: QGridLayout (2 columns) or QSplitter
Widgets: All previously defined components
ObjectName: "playerScreen"
```

**Qt Translation:**
- Main layout: QSplitter (2 columns, resizable) or QGridLayout
- Left column: QVBoxLayout with 2 cards (metadata + tracklist)
- Right column: QVBoxLayout with now-playing card
- Header: QWidget with QHBoxLayout (home button | spacer | favorite button)
- Use QScrollArea for track list

**Child Components:**
- Header: 2 QPushButton (Home, Heart)
- Metadata card: Multiple QLabel in QVBoxLayout
- Track list: TrackList widget in QScrollArea
- Now playing card: Equalizer, QLabel (title), ProgressBar, PlayerControls, VolumeControl

**Complexity Notes:**
- Requires state management (current show, track, playback state)
- Time progression simulation (QTimer updating progress)
- Auto-advance to next track on completion

---

#### BrowseScreen (BrowseScreen.tsx)
```tsx
Structure: <div flex-col>
  ├─ Header (back button | title)
  └─ <Tabs>
      ├─ TabsList (Calendar | Tours | Recent)
      └─ TabsContent
          ├─ Calendar: TouchDatePicker + instruction text
          ├─ Tours: ScrollArea with TourCard list
          └─ Recent: ShowCard list

Header: Sticky, backdrop-blur
Bottom padding: pb-32

Layout: QVBoxLayout
Widgets: QTabWidget, TouchDatePicker, TourCard, ShowCard
ObjectName: "browseScreen"
```

**Qt Translation:**
- Main: QWidget with QVBoxLayout
- Header: QWidget with QHBoxLayout (back button | title)
- Tabs: QTabWidget with 3 tabs
- Tab 1 (Calendar): TouchDatePicker widget
- Tab 2 (Tours): QScrollArea with QVBoxLayout of TourCard widgets
- Tab 3 (Recent): QVBoxLayout of ShowCard widgets

**Tab Content:**
1. **Calendar:** TouchDatePicker + QLabel (instructions)
2. **Tours:** List of TourCard (scrollable)
3. **Recent:** List of recent ShowCard (3 shows)

**Interactions:**
- Date selected → Load show, navigate to PlayerScreen
- Tour selected → Navigate to TourDetailScreen
- Show selected → Load show, navigate to PlayerScreen

---

#### TourDetailScreen (TourDetailScreen.tsx)
```tsx
Structure: <div flex-col>
  ├─ Header (back button | tour name)
  └─ <div grid-cols-3> Show cards (3 columns)

Header: Sticky, backdrop-blur
Bottom padding: pb-32
Grid: 3 equal columns

Layout: QVBoxLayout + QGridLayout
Widgets: ShowCard
ObjectName: "tourDetailScreen"
```

**Qt Translation:**
- Main: QWidget with QVBoxLayout
- Header: QWidget with QHBoxLayout (back button | title)
- Grid: QScrollArea with QGridLayout (3 columns)
- Populate with ShowCard widgets

**Interactions:**
- Back button → Navigate to previous screen
- Show card clicked → Load show, navigate to PlayerScreen

**Data:**
- Filter shows by tour slug (from URL/route parameter)
- Display show count: "X shows"

---

#### CollectionsScreen (CollectionsScreen.tsx)
```tsx
Structure: <div flex-col>
  ├─ Header (back button | title | add button)
  └─ ScrollArea
      └─ [Collection sections]
          ├─ <div flex-row> Collection header (name | delete button)
          └─ [ShowCard list or empty state]

Header: Sticky, backdrop-blur
Bottom padding: pb-32
Scrollable: Full content area

Layout: QVBoxLayout
Widgets: ShowCard, QPushButton (add, delete)
ObjectName: "collectionsScreen"
```

**Qt Translation:**
- Main: QWidget with QVBoxLayout
- Header: QWidget with QHBoxLayout (back | title | add button)
- Content: QScrollArea with QVBoxLayout
- Each collection: QGroupBox or QWidget section
  - Header: QHBoxLayout (name | delete button)
  - Content: QVBoxLayout of ShowCard or empty state QLabel

**Interactions:**
- Add button → Show dialog to create new collection
- Delete button → Confirm and delete collection
- Show card → Load show, navigate to PlayerScreen

**Data:**
- Collections stored locally (SQLite)
- Each collection has: id, name, list of show IDs

---

#### HistoryScreen (HistoryScreen.tsx)
```tsx
Structure: <div flex-col>
  ├─ Header (back button | title)
  └─ ScrollArea
      └─ [History entries]
          ├─ <div> Timestamp label
          └─ ShowCard

Header: Sticky, backdrop-blur
Bottom padding: pb-32
Scrollable: Full content area

Layout: QVBoxLayout
Widgets: ShowCard, QLabel (timestamps)
ObjectName: "historyScreen"
```

**Qt Translation:**
- Main: QWidget with QVBoxLayout
- Header: QWidget with QHBoxLayout (back button | title)
- Content: QScrollArea with QVBoxLayout
- Each entry: QVBoxLayout (timestamp label + ShowCard)

**Interactions:**
- Show card → Load show, navigate to PlayerScreen

**Data:**
- History stored locally (SQLite)
- Each entry: show ID, played timestamp
- Timestamps formatted as relative time ("2 hours ago", "Yesterday", etc.)

**Empty State:**
- Show message: "No listening history yet. Start exploring shows!"

---

### Layout/App Components

#### Layout (Layout.tsx)
```tsx
Structure: <div> (gradient background)
  ├─ [Conditional] <TopNav>
  ├─ <Outlet> (router content)
  └─ <NowPlayingBar>

Background: linear-gradient(180deg, #1a0b2e 0%, #2d1b4e 50%, #4c1d95 100%)
Min-height: 100vh
TopNav visible: Only on WelcomeScreen (pathname === "/")

Layout: QVBoxLayout
Widgets: TopNav, QStackedWidget (screens), NowPlayingBar
ObjectName: "mainLayout"
```

**Qt Translation:**
- Main window: QMainWindow or QWidget
- Background: Apply gradient via QSS or custom paintEvent
- Layout: QVBoxLayout
  - TopNav widget (conditional visibility)
  - QStackedWidget for screen content
  - NowPlayingBar widget (fixed bottom)

**Conditional TopNav:**
- Show TopNav only when WelcomeScreen is active
- Use signal/slot to update visibility on screen change

**Gradient Background:**
- Option 1: QSS `background: qlineargradient(...)`
- Option 2: Custom paintEvent on main widget

---

#### App (App.tsx)
```tsx
Structure: <RouterProvider>

Purpose: Root component providing React Router
Routes defined elsewhere (likely src/app/routes.tsx)

Layout: N/A (routing logic)
Widget: Main application entry point
```

**Qt Translation:**
- Not a visual component
- Equivalent: Main application window with QStackedWidget for screens
- Routing: Implement navigation system (signal/slot based)

**Routing System:**
- Use QStackedWidget to switch between screens
- Emit signals for navigation: `navigate(screenName, params)`
- Connect signals in main window to change current widget

**Route Map:**
```
/ → WelcomeScreen
/player → PlayerScreen
/browse → BrowseScreen
/tour/:slug → TourDetailScreen
/collections → CollectionsScreen
/history → HistoryScreen
```

---

## Dependency Tree

### Visual Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                           App (Root)                             │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │       Layout            │
                    │  - TopNav (conditional) │
                    │  - Outlet (screens)     │
                    │  - NowPlayingBar        │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    [TopNav]              [NowPlayingBar]          [Screens]
         │                       │                       │
         └─ (no deps)            ├─ Equalizer           ├─ WelcomeScreen
                                 └─ PlayerControls      │    └─ PrimaryButton
                                                        │
                                                        ├─ PlayerScreen
                                                        │    ├─ Equalizer
                                                        │    ├─ PlayerControls
                                                        │    ├─ ProgressBar
                                                        │    ├─ VolumeControl
                                                        │    ├─ TrackList
                                                        │    └─ ScrollArea*
                                                        │
                                                        ├─ BrowseScreen
                                                        │    ├─ TouchDatePicker
                                                        │    ├─ TourCard
                                                        │    ├─ ShowCard
                                                        │    ├─ Tabs*
                                                        │    └─ ScrollArea*
                                                        │
                                                        ├─ TourDetailScreen
                                                        │    └─ ShowCard
                                                        │
                                                        ├─ CollectionsScreen
                                                        │    ├─ ShowCard
                                                        │    └─ ScrollArea*
                                                        │
                                                        └─ HistoryScreen
                                                             ├─ ShowCard
                                                             └─ ScrollArea*

* = shadcn/ui component (use Qt equivalents: QScrollArea, QTabWidget)
```

### Dependency Tiers

**Tier 1 - No Dependencies (Build First):**
- PrimaryButton
- ShowCard
- TourCard
- ProgressBar
- ImageWithFallback

**Tier 2 - Basic Dependencies (Build Second):**
- Equalizer (self-contained, animated)
- PlayerControls (lucide icons only)
- VolumeControl (depends on Slider → QSlider)
- TrackList (depends on ScrollArea → QScrollArea)

**Tier 3 - Compound Components (Build Third):**
- TouchDatePicker (complex logic, no component deps)
- TopNav (navigation logic, icons)
- NowPlayingBar (depends on Equalizer, PlayerControls)

**Tier 4 - Screens (Build Last):**
- WelcomeScreen (depends on PrimaryButton)
- TourDetailScreen (depends on ShowCard)
- HistoryScreen (depends on ShowCard)
- CollectionsScreen (depends on ShowCard)
- BrowseScreen (depends on TouchDatePicker, TourCard, ShowCard)
- PlayerScreen (depends on Equalizer, PlayerControls, ProgressBar, VolumeControl, TrackList)

**Tier 5 - Layout (Build Final):**
- Layout (depends on TopNav, NowPlayingBar, all screens)
- App (routing system, depends on Layout)

---

## Build Order Recommendation

### Phase 1: Foundation Components (Tier 1)

**Task Priority: Build these first**

1. **PrimaryButton** - Simplest, used everywhere
   - File: `ui/components/primary_button.py`
   - Estimated lines: 30-40
   - Blockers: None

2. **ShowCard** - Used in 5 screens
   - File: `ui/components/show_card.py`
   - Estimated lines: 60-80
   - Blockers: None

3. **TourCard** - Used in BrowseScreen
   - File: `ui/components/tour_card.py`
   - Estimated lines: 40-50
   - Blockers: None

4. **ProgressBar** - Simple, self-contained
   - File: `ui/components/progress_bar.py`
   - Estimated lines: 50-60
   - Blockers: None

5. **ImageWithFallback** - Nice-to-have utility
   - File: `ui/components/image_with_fallback.py`
   - Estimated lines: 40-50
   - Blockers: None

---

### Phase 2: Media Components (Tier 2)

**Task Priority: Build after foundation**

6. **Equalizer** - Already exists! Verify implementation
   - File: `ui/components/equalizer.py` (EXISTING)
   - Action: Verify against Phase 4 specs
   - Check: Bar count (5), colors, sizing (compact vs. large)

7. **PlayerControls** - Core playback UI
   - File: `ui/components/player_controls.py`
   - Estimated lines: 80-100
   - Blockers: None (icons from Qt)

8. **VolumeControl** - Simple slider + button
   - File: `ui/components/volume_control.py`
   - Estimated lines: 40-50
   - Blockers: None

9. **TrackList** - Scrollable track listing
   - File: `ui/components/track_list.py`
   - Estimated lines: 100-120
   - Blockers: None (uses QScrollArea)

---

### Phase 3: Complex Components (Tier 3)

**Task Priority: Build after media components**

10. **TouchDatePicker** - Complex calendar logic
    - File: `ui/components/touch_date_picker.py`
    - Estimated lines: 200-250
    - Blockers: None (self-contained logic)
    - Alternative: Use/customize QCalendarWidget

11. **TopNav** - Simple navigation bar
    - File: `ui/components/top_nav.py`
    - Estimated lines: 50-60
    - Blockers: Navigation system (route signals)

12. **NowPlayingBar** - Persistent playback bar
    - File: `ui/components/now_playing_bar.py`
    - Estimated lines: 150-180
    - Blockers: Equalizer, PlayerControls, navigation system

---

### Phase 4: Screen Components (Tier 4)

**Task Priority: Build after all components exist**

13. **WelcomeScreen** - Simplest screen
    - File: `ui/screens/welcome_screen.py`
    - Estimated lines: 80-100
    - Blockers: PrimaryButton, navigation system

14. **TourDetailScreen** - Simple grid layout
    - File: `ui/screens/tour_detail_screen.py`
    - Estimated lines: 80-100
    - Blockers: ShowCard, navigation system

15. **HistoryScreen** - Simple list layout
    - File: `ui/screens/history_screen.py`
    - Estimated lines: 100-120
    - Blockers: ShowCard, database/history storage

16. **CollectionsScreen** - List with add/delete
    - File: `ui/screens/collections_screen.py`
    - Estimated lines: 120-150
    - Blockers: ShowCard, database/collections storage

17. **BrowseScreen** - Tabbed interface
    - File: `ui/screens/browse_screen.py`
    - Estimated lines: 150-180
    - Blockers: TouchDatePicker, TourCard, ShowCard, QTabWidget

18. **PlayerScreen** - Most complex screen (two-column)
    - File: `ui/screens/player_screen.py`
    - Estimated lines: 200-250
    - Blockers: All media components, navigation system

---

### Phase 5: Layout & Integration (Tier 5)

**Task Priority: Build last, after all screens**

19. **Layout Component** - Main app wrapper
    - File: `ui/main_window.py` or `ui/layout.py`
    - Estimated lines: 100-120
    - Blockers: TopNav, NowPlayingBar, all screens

20. **App/Router System** - Navigation logic
    - File: `ui/router.py` or integrate into main_window.py
    - Estimated lines: 80-100
    - Blockers: All screens, Layout

21. **Main Application Entry** - Tie it all together
    - File: `main.py`
    - Estimated lines: 40-60
    - Blockers: Layout, router, all components

---

## Gaps and Questions

### 1. Missing Component Files

**Question:** Are there any components referenced in screens that don't have corresponding .tsx files?

**Findings:**
- All components are accounted for
- BottomNav.tsx is deprecated (re-exports TopNav)
- UI library components (shadcn/ui) are used but don't need custom implementation (use Qt equivalents)

**Action:** None required.

---

### 2. UI Library Components (shadcn/ui)

**Question:** Which shadcn/ui components are used and what are their Qt equivalents?

**Findings:**

| shadcn/ui Component | Used In | Qt Equivalent | Notes |
|---------------------|---------|---------------|-------|
| **ScrollArea** | PlayerScreen, BrowseScreen, CollectionsScreen, HistoryScreen | QScrollArea | Direct equivalent |
| **Tabs** / TabsList / TabsContent / TabsTrigger | BrowseScreen | QTabWidget | Direct equivalent |
| **Slider** | VolumeControl | QSlider | Direct equivalent |
| **Dialog** | (Not used yet) | QDialog | For future features |
| **Button** | (Not used - custom PrimaryButton) | QPushButton | Already have PrimaryButton |
| **Card** | (Not used - custom ShowCard/TourCard) | QWidget | Already have custom cards |

**Action:** Use standard Qt widgets listed above. No custom implementation needed.

---

### 3. Icon System

**Question:** How should lucide-react icons be translated to Qt?

**Findings:**

| Icon | Usage | Suggested Qt Approach |
|------|-------|----------------------|
| Heart | TopNav, PlayerScreen | Unicode: ♥ (U+2665) or QIcon from image |
| Clock | TopNav | Unicode: ⏰ (U+23F0) or QIcon |
| Play/Pause | PlayerControls | Unicode: ▶ (U+25B6) / ⏸ (U+23F8) or QIcon |
| SkipBack/Forward | PlayerControls | Unicode: ⏮ (U+23EE) / ⏭ (U+23ED) or QIcon |
| RotateCcw/Cw | PlayerControls | Unicode: ↶ (U+21B6) / ↷ (U+21B7) or QIcon |
| Volume2/VolumeX | VolumeControl | Unicode: 🔊 (U+1F50A) / 🔇 (U+1F507) or QIcon |
| ChevronLeft/Right/Down/Up | Navigation, DatePicker, NowPlayingBar | Unicode: ‹ › ˅ ˄ or QIcon |
| Plus | CollectionsScreen | Unicode: + or QIcon |
| Trash2 | CollectionsScreen | Unicode: 🗑 (U+1F5D1) or QIcon |
| X | NowPlayingBar | Unicode: × (U+00D7) or QIcon |
| Home | PlayerScreen | Unicode: 🏠 (U+1F3E0) or QIcon |
| Calendar | TouchDatePicker | Unicode: 📅 (U+1F4C5) or QIcon |

**Recommendation:**
- **Option 1:** Use Unicode symbols for quick implementation (may vary by platform)
- **Option 2:** Use icon font (e.g., Font Awesome for Qt)
- **Option 3:** Create QIcon from SVG/PNG images

**Action:** Decide icon approach before implementing components.

---

### 4. Animation System

**Question:** How should motion/react animations be translated to Qt?

**Findings:**

| Animation | Component | React Implementation | Qt Equivalent |
|-----------|-----------|---------------------|---------------|
| Equalizer bar height | Equalizer | framer-motion + setInterval | QPropertyAnimation (height) + QTimer |
| Slide in/out | NowPlayingBar | AnimatePresence + motion.div | QPropertyAnimation (pos or opacity) |
| Active track pulse | TrackList | CSS animation (@keyframes) | QPropertyAnimation (opacity pulse) |
| Button scale | All buttons | active:scale-95 | QPropertyAnimation (scale) or CSS :pressed |
| Hover effects | All buttons | hover:bg-accent | QSS :hover pseudo-state |

**Recommendation:**
- Use QPropertyAnimation for position/opacity/size changes
- Use QSS pseudo-states (:hover, :pressed) for simple state changes
- Use QTimer for ongoing animations (Equalizer)

**Action:** Implement animation helper utilities if needed.

---

### 5. State Management

**Question:** How is app state managed in React, and what's the Qt equivalent?

**Findings:**

**React Approach:**
- Uses `usePlayerStore` (likely Zustand or custom hook)
- Global state includes: currentShow, currentTrack, isPlaying, currentTime, volume
- Components subscribe to state changes

**Qt Approach:**
- **Option 1:** Qt Signals/Slots (recommended in Phase 5 architecture)
- **Option 2:** Central state object (PlayerState class) with signals
- **Option 3:** QSettings for persistent state

**State Properties Needed:**
```python
class PlayerState:
    currentShow: Show | None
    currentTrack: Track | None
    isPlaying: bool
    currentTime: int (seconds)
    volume: float (0.0-1.0)

    # Signals
    showChanged = pyqtSignal(object)  # Show
    trackChanged = pyqtSignal(object)  # Track
    playingStateChanged = pyqtSignal(bool)
    timeChanged = pyqtSignal(int)
    volumeChanged = pyqtSignal(float)
```

**Action:** Design state management system early (before building screens).

---

### 6. Navigation/Routing System

**Question:** How should React Router navigation be implemented in Qt?

**Findings:**

**React Approach:**
- Uses react-router with `useNavigate()` hook
- Routes: /, /player, /browse, /tour/:slug, /collections, /history

**Qt Approach:**
- Use QStackedWidget for screen switching
- Emit signals for navigation: `navigate(screenName: str, params: dict)`
- Main window connects signal to `setCurrentWidget()`

**Navigation Pattern:**
```python
class Router(QObject):
    navigate = pyqtSignal(str, dict)  # (screen_name, params)

    def __init__(self, stacked_widget: QStackedWidget):
        self.stack = stacked_widget
        self.screens = {}  # name -> widget
        self.navigate.connect(self._handle_navigation)

    def _handle_navigation(self, screen_name: str, params: dict):
        widget = self.screens[screen_name]
        # Pass params to widget (if needed)
        widget.load_params(params)
        self.stack.setCurrentWidget(widget)
```

**Routes Needed:**
- "/" → WelcomeScreen
- "/player" → PlayerScreen
- "/browse" → BrowseScreen
- "/tour/:slug" → TourDetailScreen (with tour slug param)
- "/collections" → CollectionsScreen
- "/history" → HistoryScreen

**Action:** Implement Router utility class before building screens.

---

### 7. Data Layer

**Question:** What data sources are used and what needs to be implemented?

**Findings:**

**React Prototype Uses:**
- `mockData.ts` - Hardcoded show/track data
- `playerStore.ts` - In-memory state
- No persistent storage in prototype

**Production App Needs:**
- **API Client:** `data/api_client.py` (EXISTING - verified working)
- **Database:** `data/database.py` (stub - needs implementation for collections, history)
- **Cache:** `data/cache.py` (stub - needs implementation for images, show data)

**Required Database Tables:**
- `collections` (id, name, created_at)
- `collection_shows` (collection_id, show_id)
- `history` (show_id, played_at, track_id, position)
- `favorites` (show_id, added_at)

**Action:** Implement database schema before building CollectionsScreen/HistoryScreen.

---

### 8. Audio Engine Integration

**Question:** How do UI components interact with pygame audio engine?

**Findings:**

**Components Needing Audio Integration:**
- PlayerControls → play/pause, skip, previous, rewind, seek
- ProgressBar → current time, duration, seek
- VolumeControl → volume level, mute
- Equalizer → playing state (animate when playing)
- TrackList → play track
- PlayerScreen → time progression

**Audio Signals Needed:**
```python
class AudioPlayer:
    # Emitted signals
    playbackStarted = pyqtSignal()
    playbackPaused = pyqtSignal()
    playbackStopped = pyqtSignal()
    trackChanged = pyqtSignal(object)  # Track
    timeUpdated = pyqtSignal(int, int)  # (current, duration)

    # Control methods
    play()
    pause()
    stop()
    seek(time: int)
    set_volume(level: float)
    next_track()
    previous_track()
```

**Action:** Design audio interface before implementing PlayerScreen.

---

### 9. Touch Optimization

**Question:** Are there touch-specific considerations for Raspberry Pi touchscreen?

**Findings:**

**Design Specs:**
- 44px minimum touch targets (buttons, interactive elements)
- 7" screen @ 1280x720 resolution
- Touch-optimized components (TouchDatePicker, large buttons)

**Qt Considerations:**
- Enable touch events: `QApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)`
- Test on target hardware (Raspberry Pi with 7" touchscreen)
- Consider larger hit areas than visual size (Qt handles this)

**Components with Touch Focus:**
- TouchDatePicker (44x44px date buttons)
- All buttons (min 44px)
- Slider controls (VolumeControl, ProgressBar)
- TrackList items (56px height)

**Action:** Test touch interactions on target hardware during Phase 7.

---

### 10. Design Token Verification

**Question:** Do existing design tokens match Phase 4 specs?

**Findings:**

**Files to Verify:**
- `ui/design_tokens.py` - Python design token values
- `ui/styles/*.qss` - QSS stylesheets

**Design Tokens Needed (from Phase 4):**

**Colors:**
- Background gradient: #1a0b2e → #2d1b4e → #4c1d95
- Primary: Purple (#7c3aed or similar)
- Accent: Lighter purple
- Muted: Gray tones
- Equalizer: 3-step purple gradient

**Typography:**
- text-title: Larger heading
- text-body: Standard body text
- text-caption: Smaller captions
- Font: System default or custom

**Spacing:**
- 8pt grid: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Touch targets: 44px minimum
- Card padding: 16px (p-4)

**Shadows:**
- var(--shadow-sm): Subtle shadow
- var(--shadow-md): Medium shadow
- var(--shadow-lg): Large shadow

**Border Radius:**
- rounded-xl: 12px
- rounded-lg: 8px
- rounded-md: 6px
- rounded-full: 50%

**Action:** Cross-reference `ui/design_tokens.py` with Phase 4 specs (docs/04-phase4-design-summary.md).

---

## Summary & Next Steps

### Key Findings

1. **21 custom components/screens** need Qt implementation
2. **Clear dependency tiers** enable incremental build approach
3. **Existing Equalizer component** already implemented (verify against specs)
4. **Design tokens and QSS** already exist (verify against Phase 4)
5. **No missing components** - inventory is complete

### Critical Prerequisites (Before Building)

1. **Router/Navigation System** - Needed by all screens
2. **State Management** - PlayerState class with signals
3. **Audio Interface** - pygame player signals/methods
4. **Icon System Decision** - Unicode vs. icon font vs. images
5. **Database Schema** - For collections and history

### Recommended Build Sequence

**Week 1: Foundation**
- Implement Router system
- Implement PlayerState
- Build Tier 1 components (PrimaryButton, ShowCard, TourCard, ProgressBar)

**Week 2: Media Components**
- Verify Equalizer
- Build PlayerControls, VolumeControl, TrackList

**Week 3: Complex Components**
- Build TouchDatePicker
- Build TopNav
- Build NowPlayingBar

**Week 4: Simple Screens**
- Build WelcomeScreen
- Build TourDetailScreen
- Build HistoryScreen

**Week 5: Complex Screens**
- Build CollectionsScreen
- Build BrowseScreen
- Build PlayerScreen

**Week 6: Integration**
- Build Layout/main_window
- Integrate audio engine
- Test end-to-end

### Questions for Human Review

1. **Icon System:** Unicode symbols, icon font, or PNG/SVG images?
2. **TouchDatePicker:** Custom implementation or customize QCalendarWidget?
3. **Animation Priority:** Which animations are critical vs. nice-to-have?
4. **State Management:** Confirm Qt Signals/Slots approach vs. alternatives?
5. **Database:** Implement SQLite schema now or defer to later phase?

---

**End of Inventory**
