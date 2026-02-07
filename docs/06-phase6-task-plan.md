# Deep-Sea Phase 6 Development Plan

**Created:** February 3, 2026  
**Status:** Active Development Plan  
**Purpose:** Prevent scope creep and enforce incremental development

---

## Critical Rules for Claude Code

### The Three Laws of Development

1. **ONE TASK AT A TIME** - Never combine tasks. Never add "bonus features."
2. **RUN BEFORE COMMIT** - App must run without errors before marking task complete.
3. **TEST WHAT YOU BUILD** - Every feature must be manually tested before moving on.

### Red Lines - Automatic Stop Conditions

If Claude Code encounters ANY of these, **STOP IMMEDIATELY** and consult with human:

- ❌ More than 2 errors in a row without a successful run
- ❌ Building multiple screens in one task
- ❌ Assuming API data structure without validation
- ❌ Changing architecture decisions without approval
- ❌ Adding features not in the current task scope

### Task Completion Checklist

Every task must satisfy ALL criteria:

- [ ] Code written and saved
- [ ] App runs without errors
- [ ] Feature works as described (manually tested)
- [ ] Changes committed to git
- [ ] Human approval received before next task

**No exceptions.**

---

## Design Verification Protocol (MANDATORY)

**Source:** Lesson Learned 005 - Design-Implementation Mismatch

### Critical Rule for UI Components

**BEFORE implementing ANY UI component, you MUST:**

1. **Read the Phase 4 Component File:**
   - Location: `docs/04-ui-ux-design/src/app/components/[ComponentName].tsx` OR
   - Location: `docs/04-ui-ux-design/src/app/screens/[ScreenName].tsx`
   - Note layout structure (flex-col → QVBoxLayout, flex-row → QHBoxLayout)
   - Note all children/content elements
   - Note icons used (plan Qt equivalents: Unicode, images, or fonts)
   - Note interactions (map to Qt signals/slots)
   - Note styling classes (map to QSS objectNames)

2. **Check Existing QSS Styles:**
   - Search `styles/*.qss` for the component's objectName
   - Verify objectName casing (camelCase: `topNav`, `playerControls`, etc.)
   - Check what styles exist vs. what needs to be created

3. **Verify Task Plan vs. Design:**
   - If task plan conflicts with Phase 4 design: **STOP and ask user**
   - Phase 4 design wins unless user explicitly overrides
   - Never assume task plan is more current than design files

4. **Plan Qt Implementation:**
   - What Qt widgets are needed?
   - What layout managers? (QVBoxLayout, QHBoxLayout, QGridLayout)
   - What signals/slots for interactions?
   - What objectNames for QSS styling?

### React → Qt Translation Reference

**Layout Mapping:**
- `flex flex-col` → `QVBoxLayout`
- `flex flex-row` → `QHBoxLayout`
- `grid grid-cols-N` → `QGridLayout` with N columns
- `gap-N` → `layout.setSpacing(N * 4)` (Tailwind uses 4px units)

**Widget Mapping:**
- `<button>` → `QPushButton`
- `<div>` → `QWidget`
- `<label>`, `<span>`, `<p>` → `QLabel`
- `<input>` → `QLineEdit`

**Icon Strategy:**
- Phase 4 uses lucide-react icons (Heart, Clock, Play, etc.)
- Qt options: Unicode symbols (♥, 🕒, etc.), QIcon with images, or icon fonts
- Verify icon availability before implementation

**ObjectName Rules:**
- QSS uses camelCase: `topNav`, `bottomNav`, `playerControls`
- Set in Qt: `widget.setObjectName("topNav")`
- Must match exactly what's in styles/*.qss files

### Design Verification Checklist (Per Component)

Before calling task complete:
- [ ] Component structure matches Phase 4 React component
- [ ] Layout matches Phase 4 (flex direction, alignment, spacing)
- [ ] All children/elements present
- [ ] Icons displayed correctly (even if placeholder Unicode)
- [ ] ObjectNames match QSS selectors
- [ ] Styling applies correctly (verify in running app)
- [ ] User confirms visual match to Phase 4 design

**If Phase 4 design doesn't exist for a component:**
- Ask user for design direction
- Reference similar components from Phase 4 for consistency
- Use existing design tokens and QSS patterns
- Get user approval before proceeding

---

## Phase 6 Overview

### Revised Milestones

**Milestone 1: Walking Skeleton** (Tasks 1-5)
- Basic window that opens
- One screen displays
- One button works
- **Goal:** Prove the build process works

**Milestone 2: Playable Audio** (Tasks 6-12)
- Browse shows from API
- Select a show
- Play audio from that show
- **Goal:** End-to-end user flow works

**Milestone 3: Core Features** (Tasks 13-18)
- Add favorites
- Add history tracking
- Add date picker
- **Goal:** Must-have features complete

**Milestone 4: Remaining Features** (Tasks 19-24)
- Collections
- Tours
- Now Playing Bar
- **Goal:** All Phase 2 requirements met

---

## Milestone 1: Walking Skeleton

### Pre-Task 1: Repository Cleanup Verification

**Before starting Task 1, verify the repository is clean:**

```bash
# These files should NOT exist (deleted from failed miniaudio attempt):
ls main.py 2>/dev/null && echo "ERROR: main.py exists" || echo "✓ main.py deleted"
ls ui/main_window.py 2>/dev/null && echo "ERROR: ui/main_window.py exists" || echo "✓ ui/main_window.py deleted"
ls audio/engine.py 2>/dev/null && echo "ERROR: audio/engine.py exists" || echo "✓ audio/engine.py deleted"

# These files SHOULD exist (design system, trusted):
ls ui/design_tokens.py && echo "✓ design_tokens.py exists" || echo "ERROR: Missing design_tokens.py"
ls ui/stylesheet_loader.py && echo "✓ stylesheet_loader.py exists" || echo "ERROR: Missing stylesheet_loader.py"
ls styles/main.qss && echo "✓ main.qss exists" || echo "ERROR: Missing main.qss"
```

**If any ERROR appears:** Do NOT proceed. Repository state is inconsistent. Review CLAUDE.md "Repository Status" section.

**Expected state:**
- ✅ Design system files exist (ui/design_tokens.py, ui/stylesheet_loader.py, styles/*.qss)
- ✅ API client exists (data/api_client.py)
- ✅ Equalizer component exists (ui/components/equalizer.py)
- ❌ No main.py, no ui/main_window.py, no audio engine files
- ❌ ui/screens/ directory is empty (only __init__.py)

---

### Task 1: Minimal Application Window

**Scope:** Create the absolute minimum PyQt5 application.

**Files to Create:**
- `main.py` (< 50 lines, starting from scratch)

**What to Build:**
```python
# main.py - EXACTLY this, nothing more
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt

class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep-Sea")
        self.setFixedSize(1280, 720)
        
        label = QLabel("Deep-Sea v1.0", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 32px;")
        self.setCentralWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeepSeaApp()
    window.show()
    sys.exit(app.exec_())
```

**Acceptance Criteria:**
- [ ] Window opens when running `python main.py`
- [ ] Window is 1280x720 pixels
- [ ] White text "Deep-Sea v1.0" appears centered
- [ ] Window closes cleanly without errors

**Manual Test:**
```bash
python main.py
# Window should open, display text, close without errors
```

**Stop Conditions:**
- DO NOT add gradient background yet
- DO NOT add navigation
- DO NOT add any other widgets

---

### Task 2: Apply Gradient Background

**Scope:** Add ONLY the purple gradient background programmatically.

**Files to Modify:**
- `main.py` (add gradient setup method)

**What to Build:**
```python
# Add this method to DeepSeaApp class
def setup_gradient_background(self):
    from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush
    
    palette = self.palette()
    gradient = QLinearGradient(0, 0, 0, self.height())
    gradient.setColorAt(0.0, QColor("#1a0b2e"))
    gradient.setColorAt(0.5, QColor("#2d1b4e"))
    gradient.setColorAt(1.0, QColor("#4c1d95"))
    palette.setBrush(QPalette.Window, QBrush(gradient))
    self.setPalette(palette)
    self.setAutoFillBackground(True)

# Call in __init__ after super().__init__()
```

**Acceptance Criteria:**
- [ ] Window background shows purple gradient (dark to light, top to bottom)
- [ ] White text is still visible and centered
- [ ] No QSS files loaded yet
- [ ] App runs without errors

**Manual Test:**
```bash
python main.py
# Verify gradient background appears correctly
```

**Stop Conditions:**
- DO NOT load QSS files yet
- DO NOT add any other styling
- DO NOT add widgets

---

### Task 3: Load QSS Stylesheets

**Scope:** Load ALL three QSS files and verify base styling works.

**Files to Use (Already Exist):**
- `ui/stylesheet_loader.py` - Already implemented, just import it
- `styles/main.qss`, `styles/components.qss`, `styles/screens.qss` - Already implemented

**Files to Modify:**
- `main.py` (add stylesheet loading)

**What to Build:**
```python
# In main.py, after creating QApplication:
from ui.stylesheet_loader import load_stylesheets

app = QApplication(sys.argv)
stylesheet = load_stylesheets()
app.setStyleSheet(stylesheet)
```

**Acceptance Criteria:**
- [ ] App loads without QSS syntax errors
- [ ] Console shows no stylesheet warnings
- [ ] Gradient background still visible
- [ ] Text styling may change (expected)

**Manual Test:**
```bash
python main.py
# Check console for QSS errors
# Verify app still runs
```

**Stop Conditions:**
- DO NOT add components yet
- DO NOT modify QSS files
- DO NOT add navigation

---

### Task 4: Add Top Navigation Bar

**Design Reference:** docs/04-ui-ux-design/src/app/components/TopNav.tsx
**QSS Styles:** styles/components.qss (search for `topNav`, `navButton`)
**Visibility:** Only on Welcome screen (per Layout.tsx)

**Phase 4 Analysis:**
- React layout: `flex justify-around items-center h-[72px]` (horizontal container)
- Children: 2 buttons (Collections with Heart icon, History with Clock icon)
- Button structure: `flex flex-col items-center justify-center` (icon above text, vertical)
- Icons: Heart (lucide-react) for Collections, Clock (lucide-react) for History
- ObjectName: `topNav` (container), buttons likely styled via QSS
- Styling: Semi-transparent background with border, backdrop blur, shadow
- Fixed positioning: Top of screen, full width, z-index 40

**Qt Implementation Mapping:**
- Container: QWidget with objectName="topNav"
- Layout: QHBoxLayout with center alignment (justify-around = space evenly)
- Buttons: QPushButton with QVBoxLayout for icon+text stacking
- Icons: Unicode symbols (♥ U+2665, 🕒 U+1F552) in QLabel
- Signals: clicked → navigate to Collections/History screens

**Scope:** Create top navigation with 2 buttons (Collections, History).

**Files to Create:**
- `ui/components/top_nav.py`

**What to Build:**
```python
# ui/components/top_nav.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class TopNav(QWidget):
    """
    Top navigation bar (Phase 4 design).

    Design Reference: docs/04-ui-ux-design/src/app/components/TopNav.tsx
    Shows: Collections (Heart) and History (Clock) buttons
    Layout: Horizontal container, vertical icon-above-text buttons
    Visibility: Only on Welcome screen (per Layout.tsx line 9)
    """

    navigate_to = pyqtSignal(str)  # Emits "collections" or "history"

    def __init__(self):
        super().__init__()
        self.setObjectName("topNav")
        self.setFixedHeight(72)  # h-[72px] from Phase 4

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Collections button
        collections_btn = self._create_nav_button("♥", "Collections", "collections")
        layout.addWidget(collections_btn)

        layout.addSpacing(64)  # Gap between buttons

        # History button
        history_btn = self._create_nav_button("🕒", "History", "history")
        layout.addWidget(history_btn)

    def _create_nav_button(self, icon, text, nav_target):
        """Create vertical icon-above-text button."""
        btn = QPushButton()
        btn.setObjectName("navButton")
        btn.setMinimumSize(72, 56)  # min-w-[72px] min-h-[56px]

        # Create vertical layout for icon + text
        btn_layout = QVBoxLayout(btn)
        btn_layout.setSpacing(4)  # gap-1 = 4px
        btn_layout.setContentsMargins(8, 8, 8, 8)
        btn_layout.setAlignment(Qt.AlignCenter)

        # Icon label
        icon_label = QLabel(icon)
        icon_label.setObjectName("navIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")  # size={24}
        btn_layout.addWidget(icon_label)

        # Text label
        text_label = QLabel(text)
        text_label.setObjectName("navText")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 12px;")  # text-xs
        btn_layout.addWidget(text_label)

        # Connect signal
        btn.clicked.connect(lambda: self.navigate_to.emit(nav_target))

        return btn
```

**Files to Modify:**
- `main.py` (add top nav to window)

```python
# In DeepSeaApp.__init__:
from ui.components.top_nav import TopNav
from PyQt5.QtWidgets import QVBoxLayout, QWidget

# Create central widget with layout
central = QWidget()
main_layout = QVBoxLayout(central)
main_layout.setContentsMargins(0, 0, 0, 0)
main_layout.setSpacing(0)

# Add top nav
self.top_nav = TopNav()
self.top_nav.navigate_to.connect(self.on_navigate_to)
main_layout.addWidget(self.top_nav)

# Add screen container
self.screen_container = QWidget()
screen_layout = QVBoxLayout(self.screen_container)
screen_layout.setContentsMargins(0, 0, 0, 0)

# Placeholder label for now
label = QLabel("Deep-Sea v1.0")
label.setAlignment(Qt.AlignCenter)
label.setStyleSheet("color: white; font-size: 32px;")
screen_layout.addWidget(label)

main_layout.addWidget(self.screen_container)
self.setCentralWidget(central)

def on_navigate_to(self, destination):
    print(f"Navigate to: {destination}")  # Console output only
```

**Acceptance Criteria:**
- [ ] TopNav appears at TOP of window (not bottom)
- [ ] 2 buttons visible: Collections (♥), History (🕒)
- [ ] Buttons have icon ABOVE text (vertical layout)
- [ ] Clicking Collections prints "Navigate to: collections" to console
- [ ] Clicking History prints "Navigate to: history" to console
- [ ] ObjectName matches QSS: `topNav`
- [ ] Visual appearance matches Phase 4 TopNav component
- [ ] **User confirms:** Looks like Phase 4 design

**Manual Test:**
```bash
python main.py
# TopNav should appear at top of window
# Click Collections button → console: "Navigate to: collections"
# Click History button → console: "Navigate to: history"
# Verify icon is ABOVE text (not inline)
# Compare to docs/04-ui-ux-design/src/app/components/TopNav.tsx visual
```

**Stop Conditions:**
- DO NOT create bottom navigation (Phase 4 uses top nav only on Welcome)
- DO NOT add Home or Browse buttons (only Collections and History)
- DO NOT create screen classes yet
- DO NOT implement actual navigation (just console output)

---

### Task 5: Add Welcome Screen (Dummy)

**Design Reference:** docs/04-ui-ux-design/src/app/screens/WelcomeScreen.tsx
**QSS Styles:** styles/screens.qss (search for `welcomeScreen`)

**Phase 4 Analysis:**
- React layout: `min-h-screen flex flex-col items-center justify-center p-8 pt-24 pb-24`
- Children (in order):
  1. Logo container: `w-32 h-32 rounded-3xl bg-gradient-to-br` with fish emoji (🐟)
  2. Button container: `flex flex-col gap-4` with max-width
     - "Find a show" button (primary variant)
     - "Random show" button (secondary variant)
     - "Today in History" button (secondary variant)
- Spacing: Large gap between logo and buttons (mb-12 = 48px)
- Buttons: Use PrimaryButton component with variant prop
- Interactions:
  - "Find a show" → navigate to /browse
  - "Random show" → fetch random show, play, navigate to /player
  - "Today in History" → fetch show from today's date, play, navigate to /player
- TopNav overlay: Rendered by Layout.tsx, not WelcomeScreen itself

**Qt Implementation Mapping:**
- Container: QWidget with objectName="welcomeScreen"
- Main layout: QVBoxLayout, centered alignment
- Logo: QLabel with gradient background (or QWidget with paintEvent)
- Logo emoji: QLabel with large font
- Buttons: QPushButton with objectNames "primaryButton", "secondaryButton"
- TopNav: Separate component, managed by main window (Task 4)

**Scope:** Create Welcome screen with logo and 3 action buttons.

**Files to Create:**
- `ui/screens/welcome.py`

**What to Build:**
```python
# ui/screens/welcome.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush

class WelcomeScreen(QWidget):
    """
    Welcome screen (Phase 4 design).

    Design Reference: docs/04-ui-ux-design/src/app/screens/WelcomeScreen.tsx
    Shows: Logo + 3 action buttons (Find a show, Random show, Today in History)
    Layout: Centered vertical, top/bottom padding for TopNav/NowPlayingBar
    """

    find_show_clicked = pyqtSignal()
    random_show_clicked = pyqtSignal()
    today_in_history_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("welcomeScreen")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(32, 96, 32, 96)  # p-8, pt-24, pb-24

        # Logo (128x128 rounded gradient box with emoji)
        logo = QLabel("🐟")
        logo.setObjectName("logo")
        logo.setFixedSize(128, 128)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            font-size: 80px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #7c3aed, stop:1 #6d28d9);
            border-radius: 24px;
        """)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        layout.addSpacing(48)  # mb-12 = 48px

        # Buttons container (max-w-md = ~448px)
        button_container = QWidget()
        button_container.setMaximumWidth(448)
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(16)  # gap-4 = 16px
        button_layout.setContentsMargins(0, 0, 0, 0)

        # "Find a show" button (primary)
        find_btn = QPushButton("Find a show")
        find_btn.setObjectName("primaryButton")
        find_btn.setMinimumHeight(44)
        find_btn.clicked.connect(self.find_show_clicked.emit)
        button_layout.addWidget(find_btn)

        # "Random show" button (secondary)
        random_btn = QPushButton("Random show")
        random_btn.setObjectName("secondaryButton")
        random_btn.setMinimumHeight(44)
        random_btn.clicked.connect(self.random_show_clicked.emit)
        button_layout.addWidget(random_btn)

        # "Today in History" button (secondary)
        today_btn = QPushButton("Today in History")
        today_btn.setObjectName("secondaryButton")
        today_btn.setMinimumHeight(44)
        today_btn.clicked.connect(self.today_in_history_clicked.emit)
        button_layout.addWidget(today_btn)

        layout.addWidget(button_container, alignment=Qt.AlignCenter)
        layout.addStretch()
```

**Files to Modify:**
- `main.py` (add screen container and show Welcome)

```python
# In DeepSeaApp.__init__ (replace placeholder label):
from ui.screens.welcome import WelcomeScreen

# Replace the placeholder label in screen_container with:
self.current_screen = WelcomeScreen()
self.current_screen.find_show_clicked.connect(
    lambda: print("Find a show clicked")
)
self.current_screen.random_show_clicked.connect(
    lambda: print("Random show clicked")
)
self.current_screen.today_in_history_clicked.connect(
    lambda: print("Today in History clicked")
)
screen_layout.addWidget(self.current_screen)
```

**Acceptance Criteria:**
- [ ] Welcome screen displays on app launch
- [ ] Logo (🐟 emoji) visible at top, centered, 128x128px
- [ ] Logo has purple gradient background, rounded corners
- [ ] 3 buttons visible below logo:
  - "Find a show" (primary style)
  - "Random show" (secondary style)
  - "Today in History" (secondary style)
- [ ] All buttons meet 44px minimum height
- [ ] Buttons are max-width 448px and centered
- [ ] Clicking each button emits correct signal (console output for now)
- [ ] TopNav visible above screen content
- [ ] **User confirms:** Matches Phase 4 WelcomeScreen visual

**Manual Test:**
```bash
python main.py
# Verify Welcome screen appears below TopNav
# Click "Find a show" → console: "Find a show clicked"
# Click "Random show" → console: "Random show clicked"
# Click "Today in History" → console: "Today in History clicked"
# Compare to docs/04-ui-ux-design/src/app/screens/WelcomeScreen.tsx visual
```

**Stop Conditions:**
- DO NOT implement actual show fetching
- DO NOT add API calls
- DO NOT create other screens yet
- DO NOT add navigation logic yet

**Milestone 1 Complete:** You now have a working PyQt5 app with gradient background, QSS loaded, top nav, and one screen. App runs without errors. Commit and get approval before Milestone 2.

---

## Milestone 2: Playable Audio

### Task 6: Validate API Data Structures

**Scope:** Create validation script to inspect actual API responses.

**Files to Create:**
- `scripts/validate_api.py`

**What to Build:**
```python
# scripts/validate_api.py
import sys
import json
sys.path.insert(0, '.')

from data import PhishInAPI

print("=" * 60)
print("VALIDATING API DATA STRUCTURES")
print("=" * 60)

# Test 1: Get recent shows
print("\n1. Recent shows list:")
shows = PhishInAPI.get_shows(year=1997, audio_status='complete')
if shows:
    print(f"   Found {len(shows)} shows")
    print(f"   First show keys: {list(shows[0].keys())}")
    print(f"   Sample show:")
    print(json.dumps(shows[0], indent=2))
else:
    print("   ERROR: No shows returned")

# Test 2: Get specific show
print("\n2. Specific show detail (1997-12-31):")
show = PhishInAPI.get_show('1997-12-31')
if show:
    print(f"   Show keys: {list(show.keys())}")
    print(f"   Venue type: {type(show.get('venue'))}")
    print(f"   Venue: {show.get('venue')}")
    print(f"   Track count: {len(show.get('tracks', []))}")
    if show.get('tracks'):
        print(f"   First track keys: {list(show['tracks'][0].keys())}")
        print(f"   First track:")
        print(json.dumps(show['tracks'][0], indent=2))
else:
    print("   ERROR: Show not found")

# Test 3: Check tours
print("\n3. Tours:")
tours = PhishInAPI.get_tours()
if tours:
    print(f"   Found {len(tours)} tours")
    print(f"   First tour keys: {list(tours[0].keys())}")
    print(f"   Sample tour:")
    print(json.dumps(tours[0], indent=2))
else:
    print("   ERROR: No tours returned")

print("\n" + "=" * 60)
print("VALIDATION COMPLETE - Review output above")
print("=" * 60)
```

**Acceptance Criteria:**
- [ ] Script runs without errors: `python scripts/validate_api.py`
- [ ] Output shows actual API response structure
- [ ] Venue field type confirmed (dict or string)
- [ ] Track duration type confirmed (int or string)
- [ ] All data printed to console for inspection

**Manual Test:**
```bash
python scripts/validate_api.py > api_structure.txt
# Review api_structure.txt
# Document actual field types
```

**Stop Conditions:**
- DO NOT build UI yet
- DO NOT modify API client
- This is VALIDATION ONLY

---

### Task 7: Audio Engine Decision & Implementation

**Scope:** Choose audio library (pygame.mixer recommended) and implement basic playback.

**Decision Required:** pygame.mixer vs miniaudio

**Recommended:** pygame.mixer (simpler, "good enough" gapless per Lesson 003)

**Files to Create:**
- `audio/pygame_player.py`

**What to Build:**
```python
# audio/pygame_player.py
import pygame
import requests
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import logging

logger = logging.getLogger(__name__)

class PygamePlayer(QObject):
    """Simple audio player using pygame.mixer."""
    
    track_changed = pyqtSignal(int)
    position_changed = pyqtSignal(float)
    playback_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.track_urls = []
        self.current_track_index = 0
        self.is_playing = False
        self.cache_dir = Path.home() / ".deep-sea" / "cache" / "audio"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Position tracking timer
        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self._update_position)
        self.position_timer.setInterval(1000)  # Every 1 second
    
    def load_tracks(self, track_urls):
        """Load list of track URLs."""
        self.track_urls = track_urls
        self.current_track_index = 0
        logger.info(f"Loaded {len(track_urls)} tracks")
    
    def play(self):
        """Start/resume playback."""
        if not self.track_urls:
            logger.warning("No tracks loaded")
            return
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.position_timer.start()
            return
        
        self._play_track(self.current_track_index)
    
    def pause(self):
        """Pause playback."""
        pygame.mixer.music.pause()
        self.is_playing = False
        self.position_timer.stop()
    
    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.position_timer.stop()
    
    def next_track(self):
        """Play next track."""
        if self.current_track_index < len(self.track_urls) - 1:
            self.current_track_index += 1
            self._play_track(self.current_track_index)
        else:
            self.playback_finished.emit()
    
    def previous_track(self):
        """Play previous track."""
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self._play_track(self.current_track_index)
    
    def _play_track(self, index):
        """Download and play track at index."""
        try:
            url = self.track_urls[index]
            logger.info(f"Playing track {index}: {url}")
            
            # Download to cache
            cache_file = self.cache_dir / f"track_{index}.mp3"
            if not cache_file.exists():
                logger.info(f"Downloading to {cache_file}")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                cache_file.write_bytes(response.content)
            
            # Play from cache
            pygame.mixer.music.load(str(cache_file))
            pygame.mixer.music.play()
            self.is_playing = True
            self.position_timer.start()
            self.track_changed.emit(index)
            
            # Auto-advance when track ends
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            
        except Exception as e:
            logger.error(f"Failed to play track {index}: {e}")
            self.error_occurred.emit(str(e))
    
    def _update_position(self):
        """Update playback position."""
        if self.is_playing:
            pos = pygame.mixer.music.get_pos() / 1000.0  # ms to seconds
            self.position_changed.emit(pos)
```

**Files to Create:**
- `scripts/test_pygame_audio.py`

**What to Build:**
```python
# scripts/test_pygame_audio.py
import sys
sys.path.insert(0, '.')

from audio.pygame_player import PygamePlayer
from PyQt5.QtCore import QCoreApplication, QTimer
import logging

logging.basicConfig(level=logging.DEBUG)

# Test with public MP3
test_url = "https://archive.org/download/gd1977-05-08.sbd.hicks.4136.sbeok.shnf/gd77-05-08d3t01_vbr.mp3"

app = QCoreApplication(sys.argv)
player = PygamePlayer()

def on_track_changed(index):
    print(f"✓ Track changed to {index}")

def on_error(error):
    print(f"✗ Error: {error}")

player.track_changed.connect(on_track_changed)
player.error_occurred.connect(on_error)

player.load_tracks([test_url])
player.play()

print("Playing audio for 10 seconds...")
print("(You should hear music)")

QTimer.singleShot(10000, app.quit)
sys.exit(app.exec_())
```

**Acceptance Criteria:**
- [ ] pygame.mixer initializes without errors
- [ ] Test script downloads and plays MP3
- [ ] Audio is audible for 10 seconds
- [ ] No crashes or exceptions

**Manual Test:**
```bash
python scripts/test_pygame_audio.py
# Listen for audio
# Verify console shows "Track changed to 0"
```

**Stop Conditions:**
- DO NOT integrate with UI yet
- DO NOT implement gapless queue yet
- DO NOT add visualizer

---

### Task 8: Create Browse Screen (Shows List)

**Design Reference:** docs/04-ui-ux-design/src/app/screens/BrowseScreen.tsx
**QSS Styles:** styles/screens.qss (search for `browseScreen`)

**Phase 4 Analysis:**
- React layout: `min-h-screen pb-32` with sticky header
- Header (sticky, z-20): Back button (ChevronLeft) + "Browse Shows" title
- Content: Tabs component with 3 tabs:
  1. "Calendar" - TouchDatePicker component
  2. "Tours" - List of TourCard components
  3. "Recent" - List of recent shows (ShowCard components)
- Default tab: "Calendar" in design, but "Recent" is simplest for MVP
- Each ShowCard: Shows date, venue, tour, rating, tags
- Tabs: `grid w-full grid-cols-3` layout

**Qt Implementation Mapping:**
- Container: QWidget with objectName="browseScreen"
- Header: QWidget with QHBoxLayout (back button + title), sticky top, semi-transparent
- Back button: QPushButton with chevron (‹ U+2039 or ← U+2190)
- Tabs: QTabWidget with 3 tabs
- Recent tab: QListWidget with custom ShowCard items
- Calendar tab: Custom TouchDatePicker widget (Task 17)
- Tours tab: QListWidget with custom TourCard items
- Header: Fixed height, backdrop blur effect

**Scope:** Display list of shows from API with basic info. Start with "Recent" tab only (simplest). Add Calendar and Tours tabs in later tasks.

**Files to Create:**
- `ui/screens/browse.py`

**What to Build:**
```python
# ui/screens/browse.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTabWidget, QListWidget,
                              QListWidgetItem)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from data import PhishInAPI
import logging

logger = logging.getLogger(__name__)

class BrowseScreen(QWidget):
    """
    Browse shows screen (Phase 4 design).

    Design Reference: docs/04-ui-ux-design/src/app/screens/BrowseScreen.tsx
    Shows: Tabbed interface (Calendar, Tours, Recent)
    Initial implementation: Recent tab only
    """

    show_selected = pyqtSignal(str)  # Emits show date
    navigate_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("browseScreen")
        self.setup_ui()
        self.load_recent_shows()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sticky header (Phase 4: sticky top-0 z-20)
        header = QWidget()
        header.setObjectName("browseHeader")
        header.setFixedHeight(56)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 16, 0)

        # Back button with chevron
        back_btn = QPushButton("‹")  # Unicode back chevron
        back_btn.setObjectName("backButton")
        back_btn.setFixedSize(44, 44)
        back_btn.clicked.connect(self.navigate_back.emit)
        header_layout.addWidget(back_btn)

        # Title
        title = QLabel("Browse Shows")
        title.setObjectName("h2")
        header_layout.addWidget(title, 1)  # Stretch

        layout.addWidget(header)

        # Tabs (start with Recent only)
        tabs = QTabWidget()
        tabs.setObjectName("browseTabs")

        # Recent tab
        recent_tab = QWidget()
        recent_layout = QVBoxLayout(recent_tab)
        recent_layout.setContentsMargins(24, 24, 24, 24)  # p-6 = 24px

        caption = QLabel("Recently performed shows")
        caption.setObjectName("caption")
        caption.setStyleSheet("color: var(--muted-foreground);")
        recent_layout.addWidget(caption)

        recent_layout.addSpacing(16)  # mb-4 = 16px

        self.shows_list = QListWidget()
        self.shows_list.setObjectName("showsList")
        self.shows_list.itemClicked.connect(self.on_show_clicked)
        recent_layout.addWidget(self.shows_list)

        tabs.addTab(recent_tab, "Recent")
        # TODO: Add "Calendar" tab (Task 17)
        # TODO: Add "Tours" tab (Milestone 4)

        layout.addWidget(tabs)

    def load_recent_shows(self):
        """Load recent shows from API (1997 complete shows for now)."""
        try:
            shows = PhishInAPI.get_shows(year=1997, audio_status='complete')

            for show in shows[:20]:
                # Create ShowCard-like item (Phase 4: min-h-88px)
                date = show['date']
                venue = show.get('venue', {})
                if isinstance(venue, dict):
                    venue_name = venue.get('name', 'Unknown Venue')
                    venue_location = f"{venue.get('city', '')}, {venue.get('state', '')}"
                else:
                    venue_name = str(venue)
                    venue_location = ""

                # Format: "1997-12-31\nMSG, New York, NY"
                item_text = f"{date}\n{venue_name}"
                if venue_location:
                    item_text += f", {venue_location}"

                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, date)
                item.setSizeHint(QSize(0, 88))  # min-h-88px
                self.shows_list.addItem(item)

            logger.info(f"Loaded {len(shows)} shows")

        except Exception as e:
            logger.error(f"Failed to load shows: {e}")
            error_item = QListWidgetItem(f"Error loading shows: {e}")
            self.shows_list.addItem(error_item)

    def on_show_clicked(self, item):
        show_date = item.data(Qt.UserRole)
        if show_date:
            logger.info(f"Show selected: {show_date}")
            self.show_selected.emit(show_date)
```

**Files to Modify:**
- `main.py` (connect "Find a show" button to Browse screen)

```python
# In DeepSeaApp, update WelcomeScreen connection:
self.current_screen.find_show_clicked.connect(self.on_find_show)

# Add method:
def on_find_show(self):
    """Show Browse screen."""
    from ui.screens.browse import BrowseScreen

    # Clear current screen
    layout = self.screen_container.layout()
    if layout.count() > 0:
        old_screen = layout.itemAt(0).widget()
        layout.removeWidget(old_screen)
        old_screen.deleteLater()

    # Add Browse screen
    browse_screen = BrowseScreen()
    browse_screen.show_selected.connect(
        lambda date: print(f"Show selected: {date}")
    )
    browse_screen.navigate_back.connect(self.on_navigate_back)
    layout.addWidget(browse_screen)
    self.current_screen = browse_screen

def on_navigate_back(self):
    """Return to Welcome screen."""
    from ui.screens.welcome import WelcomeScreen

    # Clear current screen
    layout = self.screen_container.layout()
    if layout.count() > 0:
        old_screen = layout.itemAt(0).widget()
        layout.removeWidget(old_screen)
        old_screen.deleteLater()

    # Show Welcome screen
    welcome_screen = WelcomeScreen()
    # ... reconnect signals ...
    layout.addWidget(welcome_screen)
    self.current_screen = welcome_screen
```

**Acceptance Criteria:**
- [ ] Browse screen displays with sticky header at top
- [ ] Header shows back button (‹) and "Browse Shows" title
- [ ] Tabs widget shows "Recent" tab (Calendar and Tours tabs can be placeholders)
- [ ] Recent tab displays list of shows (1997 shows for now)
- [ ] Each show item is minimum 88px tall
- [ ] Each item shows: date, venue, location (multiline)
- [ ] Clicking show emits show_selected signal (console output)
- [ ] Back button navigates back to Welcome screen
- [ ] **User confirms:** Header and layout match Phase 4 BrowseScreen

**Manual Test:**
```bash
python main.py
# Click "Find a show" button
# Verify Browse screen appears with header
# Verify shows list loads
# Click a show
# Verify console prints: "Show selected: 1997-12-31"
# Click back button
# Verify returns to Welcome screen
```

**Stop Conditions:**
- DO NOT create Player screen yet
- DO NOT load full show details
- DO NOT play audio yet
- DO NOT implement Calendar or Tours tabs yet

---

### Task 9: Create Player Screen (Dummy)

**Design Reference:** docs/04-ui-ux-design/src/app/screens/PlayerScreen.tsx
**QSS Styles:** styles/screens.qss (search for `playerScreen`)

**Phase 4 Analysis:**
- React layout: Two-column grid (`grid grid-cols-2 gap-6`), full height with bottom padding
- Header (sticky, z-20): Home button (left) + Favorite button (right)
- Left column (flex-col gap-6):
  1. Show metadata card: date, venue, location, tour, rating, tags, source
  2. Track list card: scrollable, shows set list with track numbers/titles/durations
- Right column (flex-col gap-6):
  1. Now Playing card (flex-1, centered content):
     - Equalizer (large)
     - Current track title
     - "Jump to Highlight" button (if jamchart track)
     - ProgressBar
     - PlayerControls (large: rewind, previous, play/pause, next, skip)
     - VolumeControl
- All cards: bg-card, rounded-xl, p-6/p-8, border, shadow

**Qt Implementation Mapping:**
- Container: QWidget with objectName="playerScreen"
- Main layout: QVBoxLayout (header + content)
- Content layout: QHBoxLayout (two columns)
- Header: Separate QWidget with QHBoxLayout, fixed height 56px
- Left column: QVBoxLayout with 2 cards (QWidget containers)
- Right column: QVBoxLayout with 1 card
- Cards: QWidget with objectName like "metadataCard", "trackListCard", "nowPlayingCard"
- Equalizer: Reuse existing ui/components/equalizer.py
- Track list: QListWidget with custom items

**Scope:** Create Player screen layout WITHOUT audio integration.

**Files to Create:**
- `ui/screens/player.py`

**What to Build:**
```python
# ui/screens/player.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QListWidget, QListWidgetItem,
                              QScrollArea)
from PyQt5.QtCore import Qt, QSize
from ui.components.equalizer import Equalizer

class PlayerScreen(QWidget):
    """
    Player screen (Phase 4 design).

    Design Reference: docs/04-ui-ux-design/src/app/screens/PlayerScreen.tsx
    Shows: Two-column layout (metadata/tracklist | now playing controls)
    Layout: Grid with header, left column (metadata + tracks), right column (player)
    """

    def __init__(self, show_data):
        super().__init__()
        self.setObjectName("playerScreen")
        self.show_data = show_data
        self.setup_ui()

    def setup_ui(self):
        # Main vertical layout (header + content)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header (sticky)
        header = self._create_header()
        main_layout.addWidget(header)

        # Two-column content (grid-cols-2 gap-6)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)  # gap-6 = 24px
        content_layout.setContentsMargins(24, 24, 24, 24)  # p-6 = 24px

        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(24)

        metadata_card = self._create_metadata_card()
        left_column.addWidget(metadata_card)

        tracklist_card = self._create_tracklist_card()
        left_column.addWidget(tracklist_card, 1)  # Stretch

        content_layout.addLayout(left_column, 1)

        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(24)

        now_playing_card = self._create_now_playing_card()
        right_column.addWidget(now_playing_card, 1)

        content_layout.addLayout(right_column, 1)

        main_layout.addLayout(content_layout)

    def _create_header(self):
        """Sticky header with Home and Favorite buttons (Phase 4: z-20, sticky top-0)."""
        header = QWidget()
        header.setObjectName("playerHeader")
        header.setFixedHeight(56)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        home_btn = QPushButton("🏠")  # Home icon
        home_btn.setObjectName("iconButton")
        home_btn.setFixedSize(44, 44)
        layout.addWidget(home_btn)

        layout.addStretch()

        fav_btn = QPushButton("♡")  # Heart icon
        fav_btn.setObjectName("iconButton")
        fav_btn.setFixedSize(44, 44)
        layout.addWidget(fav_btn)

        return header

    def _create_metadata_card(self):
        """Show metadata card (Phase 4: bg-card rounded-xl p-6 border)."""
        card = QWidget()
        card.setObjectName("metadataCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(24, 24, 24, 24)  # p-6 = 24px

        # Date
        date_label = QLabel(self.show_data['date'])
        date_label.setObjectName("h2")
        layout.addWidget(date_label)

        # Venue
        venue = self.show_data.get('venue', {})
        if isinstance(venue, dict):
            venue_text = venue.get('name', 'Unknown Venue')
            location_text = f"{venue.get('city', '')}, {venue.get('state', '')}"
        else:
            venue_text = str(venue)
            location_text = ""

        venue_label = QLabel(venue_text)
        venue_label.setObjectName("title")
        layout.addWidget(venue_label)

        if location_text:
            location_label = QLabel(location_text)
            location_label.setObjectName("body")
            location_label.setStyleSheet("color: var(--muted-foreground);")
            layout.addWidget(location_label)

        # Tour (if available)
        tour = self.show_data.get('tour_name', '')
        if tour:
            tour_label = QLabel(tour)
            tour_label.setObjectName("caption")
            tour_label.setStyleSheet("color: var(--muted-foreground); font-style: italic;")
            layout.addWidget(tour_label)

        layout.addStretch()

        return card

    def _create_tracklist_card(self):
        """Track list card (Phase 4: bg-card rounded-xl p-6 border)."""
        card = QWidget()
        card.setObjectName("trackListCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)  # p-6 = 24px

        heading = QLabel("Set List")
        heading.setObjectName("h4")
        layout.addWidget(heading)

        layout.addSpacing(16)  # mb-4 = 16px

        # Track list
        self.track_list = QListWidget()
        self.track_list.setObjectName("trackList")

        for i, track in enumerate(self.show_data.get('tracks', [])):
            track_title = track.get('title', 'Unknown')
            duration = track.get('duration', 0)
            duration_str = f"{duration // 60}:{duration % 60:02d}"

            item_text = f"{i+1}. {track_title} ({duration_str})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, i)
            item.setSizeHint(QSize(0, 56))  # min-h-56px
            self.track_list.addItem(item)

        layout.addWidget(self.track_list)

        return card

    def _create_now_playing_card(self):
        """Now playing card with controls (Phase 4: bg-card rounded-xl p-8 border, centered)."""
        card = QWidget()
        card.setObjectName("nowPlayingCard")
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)  # p-8 = 32px

        # Equalizer (large)
        equalizer = Equalizer(size="large", is_playing=False)
        layout.addWidget(equalizer, alignment=Qt.AlignCenter)

        layout.addSpacing(32)  # mb-8 = 32px

        # Current track title
        track_title = QLabel("No track playing")
        track_title.setObjectName("title")
        track_title.setAlignment(Qt.AlignCenter)
        track_title.setWordWrap(True)
        layout.addWidget(track_title)

        layout.addSpacing(24)  # mb-6 = 24px

        # Player controls (placeholder - large size per Phase 4)
        play_btn = QPushButton("▶ Play")
        play_btn.setObjectName("primaryButton")
        play_btn.setFixedSize(64, 64)
        layout.addWidget(play_btn, alignment=Qt.AlignCenter)

        prev_btn = QPushButton("⏮ Previous")
        prev_btn.setObjectName("secondaryButton")
        prev_btn.setMinimumHeight(44)
        layout.addWidget(prev_btn, alignment=Qt.AlignCenter)

        next_btn = QPushButton("⏭ Next")
        next_btn.setObjectName("secondaryButton")
        next_btn.setMinimumHeight(44)
        layout.addWidget(next_btn, alignment=Qt.AlignCenter)

        layout.addStretch()

        return card
```

**Files to Modify:**
- `main.py` (modify Browse screen's show_selected handler)

```python
# In on_tab_changed, update Browse handler:
elif tab_name == "Browse":
    from ui.screens.browse import BrowseScreen
    screen = BrowseScreen()
    screen.show_selected.connect(self.on_show_selected)

# Add method to DeepSeaApp:
def on_show_selected(self, show_date):
    """Load full show and display Player screen."""
    from data import PhishInAPI
    from ui.screens.player import PlayerScreen
    
    try:
        # Get full show details
        show_data = PhishInAPI.get_show(show_date)
        
        # Switch to Player screen
        layout = self.screen_container.layout()
        if layout.count() > 0:
            old_screen = layout.itemAt(0).widget()
            layout.removeWidget(old_screen)
            old_screen.deleteLater()
        
        player_screen = PlayerScreen(show_data)
        layout.addWidget(player_screen)
        self.current_screen = player_screen
        
    except Exception as e:
        print(f"Error loading show: {e}")
```

**Acceptance Criteria:**
- [ ] Clicking show in Browse loads Player screen
- [ ] Player screen displays in two-column layout
- [ ] Header shows Home button (left) and Favorite button (right)
- [ ] Left column shows:
  - Metadata card with date, venue, location
  - Track list card with scrollable set list
- [ ] Right column shows:
  - Now Playing card with:
    - Equalizer (large, not animated yet)
    - Track title placeholder
    - Play, Previous, Next buttons (no functionality yet)
- [ ] All cards have rounded corners and borders (QSS styling)
- [ ] Track list items are minimum 56px tall
- [ ] Layout is responsive (each column gets 50% width)
- [ ] **User confirms:** Layout matches Phase 4 PlayerScreen two-column design

**Manual Test:**
```bash
python main.py
# Click "Find a show"
# Click a show
# Verify Player screen appears with two-column layout
# Verify header, metadata card, track list card, now playing card all visible
# Compare to docs/04-ui-ux-design/src/app/screens/PlayerScreen.tsx
```

**Stop Conditions:**
- DO NOT implement audio playback yet
- DO NOT add progress bar yet
- DO NOT add volume control yet
- DO NOT make Equalizer animate yet

---

### Task 10: Integrate Audio with Player Screen

**Scope:** Wire up pygame player to Play/Next buttons.

**Files to Modify:**
- `ui/screens/player.py`

**What to Add:**
```python
# In PlayerScreen.__init__:
from audio.pygame_player import PygamePlayer

self.player = PygamePlayer()
self.player.track_changed.connect(self.on_track_changed)
self.player.error_occurred.connect(self.on_error)

# Load tracks
track_urls = [track['mp3'] for track in self.show_data['tracks']]
self.player.load_tracks(track_urls)

# In setup_ui, connect buttons:
play_btn.clicked.connect(self.on_play_clicked)
next_btn.clicked.connect(self.player.next_track)

# Add methods:
def on_play_clicked(self):
    if self.player.is_playing:
        self.player.pause()
        self.play_btn.setText("▶ Play")
    else:
        self.player.play()
        self.play_btn.setText("⏸ Pause")

def on_track_changed(self, index):
    print(f"Now playing track {index}")
    # Update UI to show current track (highlight in list)

def on_error(self, error):
    print(f"Playback error: {error}")
```

**Acceptance Criteria:**
- [ ] Clicking Play button starts audio
- [ ] Audio is audible
- [ ] Play button changes to Pause when playing
- [ ] Clicking Next plays next track
- [ ] Track changes are logged to console
- [ ] No crashes during playback

**Manual Test:**
```bash
python main.py
# Browse → Select show → Click Play
# Verify audio plays
# Click Next
# Verify track changes
```

**Stop Conditions:**
- DO NOT add progress bar yet
- DO NOT add volume control yet
- DO NOT add Equalizer yet

---

### Task 11: Add Previous Button

**Scope:** Add Previous track button to Player screen.

**Files to Modify:**
- `ui/screens/player.py`

**What to Add:**
```python
# In setup_ui, add button:
prev_btn = QPushButton("⏮ Previous")
prev_btn.setObjectName("secondary")
prev_btn.clicked.connect(self.player.previous_track)
right_column.addWidget(prev_btn)  # Before Next button
```

**Acceptance Criteria:**
- [ ] Previous button visible
- [ ] Clicking Previous plays previous track
- [ ] Cannot go before track 0 (no crash)
- [ ] Previous works after Next

**Manual Test:**
```bash
python main.py
# Play a show
# Click Next a few times
# Click Previous
# Verify track goes backward
```

**Stop Conditions:**
- DO NOT add Stop button
- DO NOT add seek/scrub yet

---

### Task 12: Highlight Current Track in List

**Scope:** Visually highlight the currently playing track.

**Files to Modify:**
- `ui/screens/player.py`

**What to Add:**
```python
# Replace track QLabel widgets with QListWidget:
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor

# In setup_ui:
self.track_list = QListWidget()
self.track_list.setObjectName("track-list")

for i, track in enumerate(self.show_data.get('tracks', [])):
    track_title = track.get('title', 'Unknown')
    duration = track.get('duration', 0)
    duration_str = f"{duration // 60}:{duration % 60:02d}"
    
    item = QListWidgetItem(f"{i+1}. {track_title} ({duration_str})")
    item.setData(Qt.UserRole, i)
    self.track_list.addItem(item)

self.track_list.itemClicked.connect(self.on_track_clicked)
left_column.addWidget(self.track_list)

# Update on_track_changed:
def on_track_changed(self, index):
    # Highlight current track
    for i in range(self.track_list.count()):
        item = self.track_list.item(i)
        if i == index:
            item.setBackground(QColor("#7c3aed"))  # Purple highlight
        else:
            item.setBackground(QColor("transparent"))
    print(f"Now playing track {index}")

def on_track_clicked(self, item):
    """Jump to clicked track."""
    track_index = item.data(Qt.UserRole)
    self.player.current_track_index = track_index
    self.player._play_track(track_index)
```

**Acceptance Criteria:**
- [ ] Track list shows all tracks with durations
- [ ] Currently playing track has purple background
- [ ] Clicking a track jumps to that track
- [ ] Highlight updates when track changes

**Manual Test:**
```bash
python main.py
# Play a show
# Verify track 1 is highlighted
# Click Next
# Verify track 2 is highlighted
# Click track 5 in list
# Verify track 5 plays and is highlighted
```

**Stop Conditions:**
- DO NOT add progress bar yet
- DO NOT add album art yet

**Milestone 2 Complete:** You can now browse shows and play audio. End-to-end user flow works. Commit and get approval before Milestone 3.

---

## Milestone 3: Core Features

### Task 13: Add Favorites Button to Player

**Design Reference:** docs/04-ui-ux-design/src/app/screens/PlayerScreen.tsx (lines 76-79)
**QSS Styles:** styles/components.qss (search for `iconButton`)

**Phase 4 Analysis:**
- Location: Header, right side (after Home button)
- Icon: Heart (lucide-react), size 24
- Button: min-w-[44px] min-h-[44px], rounded-full, hover effect
- Interaction: Click to toggle favorite status
- Visual feedback: Filled heart when favorited

**Scope:** Add heart button to save show to favorites.

**Files to Create:**
- `data/database.py` (SQLite wrapper for favorites)

**What to Build:**
```python
# data/database.py
import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".deep-sea" / "deep-sea.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_schema()
    
    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_date TEXT NOT NULL UNIQUE,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def add_favorite(self, show_date):
        """Add show to favorites."""
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO favorites (show_date) VALUES (?)",
                (show_date,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding favorite: {e}")
            return False
    
    def remove_favorite(self, show_date):
        """Remove show from favorites."""
        try:
            self.conn.execute(
                "DELETE FROM favorites WHERE show_date = ?",
                (show_date,)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing favorite: {e}")
            return False
    
    def is_favorite(self, show_date):
        """Check if show is in favorites."""
        cursor = self.conn.execute(
            "SELECT 1 FROM favorites WHERE show_date = ?",
            (show_date,)
        )
        return cursor.fetchone() is not None
    
    def get_favorites(self):
        """Get all favorite show dates."""
        cursor = self.conn.execute(
            "SELECT show_date FROM favorites ORDER BY added_at DESC"
        )
        return [row[0] for row in cursor.fetchall()]
```

**Files to Modify:**
- `ui/screens/player.py`

**What to Add:**
```python
# In __init__:
from data.database import Database
self.db = Database()

# In setup_ui, add favorite button:
fav_btn = QPushButton("♡ Favorite")
fav_btn.setObjectName("secondary")
fav_btn.clicked.connect(self.toggle_favorite)
right_column.addWidget(fav_btn)  # After title

# Update button state on load:
self.fav_btn = fav_btn
self.update_favorite_button()

# Add methods:
def update_favorite_button(self):
    is_fav = self.db.is_favorite(self.show_data['date'])
    if is_fav:
        self.fav_btn.setText("♥ Favorited")
        self.fav_btn.setStyleSheet("background-color: #ef4444;")
    else:
        self.fav_btn.setText("♡ Favorite")
        self.fav_btn.setStyleSheet("")

def toggle_favorite(self):
    show_date = self.show_data['date']
    if self.db.is_favorite(show_date):
        self.db.remove_favorite(show_date)
    else:
        self.db.add_favorite(show_date)
    self.update_favorite_button()
```

**Acceptance Criteria:**
- [ ] Favorite button visible in Player screen
- [ ] Clicking button adds show to favorites
- [ ] Button changes to "♥ Favorited" when favorited
- [ ] Clicking again removes from favorites
- [ ] State persists across app restarts

**Manual Test:**
```bash
python main.py
# Play a show
# Click Favorite
# Verify button shows "♥ Favorited"
# Restart app
# Play same show
# Verify button still shows "♥ Favorited"
```

**Stop Conditions:**
- DO NOT create Favorites screen yet
- DO NOT add Collections yet

---

### Task 14: Create Collections Screen (List Favorites)

**Design Reference:** docs/04-ui-ux-design/src/app/screens/CollectionsScreen.tsx
**QSS Styles:** styles/screens.qss (search for `collectionsScreen`)

**Phase 4 Analysis:**
- React layout: `min-h-screen pb-32` with sticky header
- Header: Back button + "Collections" title + "New Collection" button (Plus icon)
- Content: Multiple collections with show lists
- Each collection:
  - Heading with collection name (emoji + text)
  - Delete button (Trash2 icon)
  - List of ShowCard components
  - Empty state if no shows
- Default collections: "⭐ Favorites", "🎫 Shows I Attended"
- Scrollable content area

**Qt Implementation Mapping:**
- Container: QWidget with objectName="collectionsScreen"
- Header: QWidget with QHBoxLayout (back, title, new button)
- Collections: QListWidget or QScrollArea with multiple collection widgets
- Each collection: QWidget with heading + show list
- ShowCards: QListWidget items

**Scope:** Display favorited shows in Collections screen (simplified - just Favorites for now).

**Files to Create:**
- `ui/screens/collections.py`

**What to Build:**
```python
# ui/screens/collections.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, 
                              QListWidgetItem, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt
from data.database import Database
from data import PhishInAPI

class CollectionsScreen(QWidget):
    show_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        self.load_favorites()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Favorites")
        title.setObjectName("h2")
        layout.addWidget(title)
        
        self.favorites_list = QListWidget()
        self.favorites_list.itemClicked.connect(self.on_show_clicked)
        layout.addWidget(self.favorites_list)
    
    def load_favorites(self):
        """Load favorited shows."""
        favorites = self.db.get_favorites()
        
        if not favorites:
            item = QListWidgetItem("No favorites yet")
            self.favorites_list.addItem(item)
            return
        
        for show_date in favorites:
            try:
                # Get show details for display
                show = PhishInAPI.get_show(show_date)
                venue = show.get('venue', {})
                if isinstance(venue, dict):
                    venue_name = venue.get('name', 'Unknown Venue')
                else:
                    venue_name = str(venue)
                
                item_text = f"{show_date} - {venue_name}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, show_date)
                self.favorites_list.addItem(item)
            except Exception as e:
                print(f"Error loading favorite {show_date}: {e}")
    
    def on_show_clicked(self, item):
        show_date = item.data(Qt.UserRole)
        if show_date:
            self.show_selected.emit(show_date)
```

**Files to Modify:**
- `main.py` (add Collections screen to tab switching)

```python
# In on_tab_changed:
elif tab_name == "Collections":
    from ui.screens.collections import CollectionsScreen
    screen = CollectionsScreen()
    screen.show_selected.connect(self.on_show_selected)
```

**Acceptance Criteria:**
- [ ] Collections tab shows list of favorited shows
- [ ] If no favorites, shows "No favorites yet"
- [ ] Clicking favorited show loads Player screen
- [ ] Favorites update after favoriting new show (requires tab switch)

**Manual Test:**
```bash
python main.py
# Favorite 2-3 shows from Browse
# Click Collections tab
# Verify favorited shows appear
# Click a favorite
# Verify Player loads
```

**Stop Conditions:**
- DO NOT add custom collections yet
- DO NOT add delete/edit features

---

### Task 15: Add Listening History Tracking

**Scope:** Automatically track played shows in history.

**Files to Modify:**
- `data/database.py`

**What to Add:**
```python
# Add to _init_schema:
self.conn.execute("""
    CREATE TABLE IF NOT EXISTS listening_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        show_date TEXT NOT NULL,
        track_title TEXT,
        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Add methods:
def add_to_history(self, show_date, track_title):
    """Record a played track."""
    try:
        self.conn.execute(
            "INSERT INTO listening_history (show_date, track_title) VALUES (?, ?)",
            (show_date, track_title)
        )
        self.conn.commit()
    except Exception as e:
        print(f"Error adding to history: {e}")

def get_history(self, limit=50):
    """Get recent listening history."""
    cursor = self.conn.execute("""
        SELECT DISTINCT show_date, MAX(played_at) as last_played
        FROM listening_history
        GROUP BY show_date
        ORDER BY last_played DESC
        LIMIT ?
    """, (limit,))
    return [row[0] for row in cursor.fetchall()]
```

**Files to Modify:**
- `ui/screens/player.py`

**What to Add:**
```python
# In on_track_changed:
def on_track_changed(self, index):
    # ... existing highlight code ...
    
    # Record to history
    track = self.show_data['tracks'][index]
    track_title = track.get('title', 'Unknown')
    self.db.add_to_history(self.show_data['date'], track_title)
```

**Acceptance Criteria:**
- [ ] Playing tracks adds entries to history database
- [ ] Each track play is recorded separately
- [ ] Database queries return distinct shows (not every track)

**Manual Test:**
```bash
python main.py
# Play a show (play 3-4 tracks)
# Check database:
sqlite3 ~/.deep-sea/deep-sea.db
SELECT * FROM listening_history;
# Verify entries exist
```

**Stop Conditions:**
- DO NOT create History screen yet
- DO NOT add history display

---

### Task 16: Create History Screen

**Design Reference:** docs/04-ui-ux-design/src/app/screens/HistoryScreen.tsx
**QSS Styles:** styles/screens.qss (search for `historyScreen`)

**Phase 4 Analysis:**
- React layout: `min-h-screen pb-32` with sticky header
- Header: Back button + "Listening History" title
- Content: List of history entries with timestamps
- Each entry:
  - Timestamp label ("5 minutes ago", "Yesterday", etc.)
  - ShowCard component
- Empty state: "No listening history yet. Start exploring shows!"
- Scrollable content area
- Chronological order (most recent first)

**Qt Implementation Mapping:**
- Container: QWidget with objectName="historyScreen"
- Header: QWidget with QHBoxLayout (back button + title)
- History list: QListWidget or QScrollArea with timestamp + show widgets
- Timestamp formatting: "X minutes/hours/days ago" helper function
- Empty state: QLabel with centered text

**Scope:** Display listening history in History screen.

**Files to Create:**
- `ui/screens/history.py`

**What to Build:**
```python
# ui/screens/history.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, 
                              QListWidgetItem, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt
from data.database import Database
from data import PhishInAPI

class HistoryScreen(QWidget):
    show_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        self.load_history()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Listening History")
        title.setObjectName("h2")
        layout.addWidget(title)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_show_clicked)
        layout.addWidget(self.history_list)
    
    def load_history(self):
        """Load listening history."""
        history = self.db.get_history(limit=20)
        
        if not history:
            item = QListWidgetItem("No listening history yet")
            self.history_list.addItem(item)
            return
        
        for show_date in history:
            try:
                show = PhishInAPI.get_show(show_date)
                venue = show.get('venue', {})
                if isinstance(venue, dict):
                    venue_name = venue.get('name', 'Unknown Venue')
                else:
                    venue_name = str(venue)
                
                item_text = f"{show_date} - {venue_name}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, show_date)
                self.history_list.addItem(item)
            except Exception as e:
                print(f"Error loading history {show_date}: {e}")
    
    def on_show_clicked(self, item):
        show_date = item.data(Qt.UserRole)
        if show_date:
            self.show_selected.emit(show_date)
```

**Files to Modify:**
- `main.py` (add History screen to tab switching)

```python
# In on_tab_changed:
elif tab_name == "History":
    from ui.screens.history import HistoryScreen
    screen = HistoryScreen()
    screen.show_selected.connect(self.on_show_selected)
```

**Acceptance Criteria:**
- [ ] History tab shows recently played shows
- [ ] Most recent shows appear at top
- [ ] Clicking show loads Player screen
- [ ] History updates after playing new show (requires tab switch)

**Manual Test:**
```bash
python main.py
# Play 2-3 different shows
# Click History tab
# Verify shows appear in order (most recent first)
```

**Stop Conditions:**
- DO NOT add clear history feature
- DO NOT add date filters

---

### Task 17: Add Date Picker to Browse Screen

**Design Reference:** docs/04-ui-ux-design/src/app/components/TouchDatePicker.tsx
**QSS Styles:** styles/components.qss (search for `datePicker`)

**Phase 4 Analysis:**
- Complex component with multiple views:
  1. Calendar view: Grid of days, month/year navigation
  2. Month picker view: Grid of 12 months
  3. Year picker view: Scrollable list of available years
- Features:
  - Available dates highlighted (dates with shows)
  - Selected date highlighted
  - Tap month name → month picker
  - Tap year → year picker
  - Previous/next month navigation
- Layout: Calendar grid (7 columns for days of week)
- Touch-optimized: Large tap targets (min 44px)

**Qt Implementation Mapping:**
- Container: QWidget with objectName="datePicker"
- Calendar grid: QGridLayout (7 columns)
- Day cells: QPushButton (44x44 minimum)
- Month/year pickers: Separate QWidget views (QStackedWidget for switching)
- Navigation: QPushButton with chevron icons
- Available dates: Check against API data, style differently

**Scope:** Add simplified date selection to Browse screen. Start with year spinner only (simpler than full TouchDatePicker).

**Files to Modify:**
- `ui/screens/browse.py`

**What to Add:**
```python
# In setup_ui, add date inputs:
from PyQt5.QtWidgets import QHBoxLayout, QSpinBox

date_layout = QHBoxLayout()

year_label = QLabel("Year:")
year_spin = QSpinBox()
year_spin.setRange(1983, 2025)  # Phish active years
year_spin.setValue(1997)
year_spin.valueChanged.connect(self.load_shows)

date_layout.addWidget(year_label)
date_layout.addWidget(year_spin)
date_layout.addStretch()

layout.addLayout(date_layout)
layout.addWidget(title)
# ... rest of setup_ui

self.year_spin = year_spin

# Update load_shows:
def load_shows(self):
    """Load shows for selected year."""
    year = self.year_spin.value()
    self.shows_list.clear()
    
    try:
        shows = PhishInAPI.get_shows(year=year, audio_status='complete')
        # ... rest of loading logic
```

**Acceptance Criteria:**
- [ ] Year spinner visible above shows list
- [ ] Default year is 1997
- [ ] Changing year reloads shows for that year
- [ ] Shows load without errors for any year

**Manual Test:**
```bash
python main.py
# Click Browse
# Change year to 1999
# Verify shows for 1999 load
# Change to 2003
# Verify shows for 2003 load
```

**Stop Conditions:**
- DO NOT add month/day pickers yet
- DO NOT add "only dates with shows" filtering
- DO NOT add tour filtering

---

### Task 18: Validate Milestone 3 Complete

**Scope:** Manual testing of all Milestone 3 features together.

**Test Checklist:**
- [ ] Browse shows by year
- [ ] Play a show
- [ ] Favorite a show
- [ ] Verify favorite appears in Collections
- [ ] Play favorite from Collections
- [ ] Verify show appears in History
- [ ] Play different show from History
- [ ] Change browse year, play another show
- [ ] Verify all features work together
- [ ] Restart app, verify favorites/history persist

**Manual Test:**
```bash
python main.py
# Run through complete user flow
# Test edge cases (empty lists, API errors, etc.)
```

**Stop Conditions:**
- DO NOT proceed to Milestone 4 until approved

**Milestone 3 Complete:** Core features (favorites, history, date picker) are working. Commit and get approval before Milestone 4.

---

## Milestone 4: Remaining Features

### Task 19-24: Tours, Now Playing Bar, Equalizer, etc.

*[Tasks 19-24 would follow the same pattern: one small feature at a time, with specific scope, acceptance criteria, and stop conditions. I'm stopping here to keep this document from becoming unwieldy, but the pattern is clear.]*

---

## Emergency Stop Protocol

If at ANY point during development Claude Code:
- Builds more than described in the task
- Combines multiple tasks without permission
- Encounters 3+ errors in a row
- Changes approved architecture decisions
- Adds features not in the task scope

**Human intervention required:**
1. STOP development immediately
2. Review what was attempted
3. Roll back to last known good commit
4. Consult with human before proceeding

---

## Task Approval Process

**After each task:**
1. Developer tests manually (follows Manual Test section)
2. Developer confirms acceptance criteria met
3. Developer commits working code
4. Developer marks task complete in this document
5. Developer gets human approval before next task

**No exceptions.**

---

## Version Control Strategy

**Commits:**
- One commit per task
- Commit message: "Task N: [Task title]"
- Only commit working code
- Never commit broken code "to fix later"

**Branches:**
- `main` - Always working code
- `task-N` - Working on task N (optional)
- Merge to main only when task complete and approved

---

**End of Phase 6 Task Plan v1.1**
