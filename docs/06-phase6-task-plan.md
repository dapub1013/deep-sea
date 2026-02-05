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

### Task 4: Add Bottom Navigation Bar

**Scope:** Create bottom navigation with 4 tabs (Home, Browse, Collections, History).

**Files to Create:**
- `ui/components/bottom_nav.py`

**What to Build:**
```python
# ui/components/bottom_nav.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class BottomNav(QWidget):
    tab_changed = pyqtSignal(str)  # Emits tab name
    
    def __init__(self):
        super().__init__()
        self.setObjectName("bottom-nav")
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        tabs = ["Home", "Browse", "Collections", "History"]
        for tab in tabs:
            btn = QPushButton(tab)
            btn.setObjectName("nav-tab")
            btn.clicked.connect(lambda checked, t=tab: self.tab_changed.emit(t))
            layout.addWidget(btn)
```

**Files to Modify:**
- `main.py` (add bottom nav to window)

```python
# In DeepSeaApp.__init__:
from ui.components.bottom_nav import BottomNav

self.bottom_nav = BottomNav()
self.bottom_nav.tab_changed.connect(self.on_tab_changed)

# Add to layout (use QVBoxLayout)
# ... (replace setCentralWidget with layout)

def on_tab_changed(self, tab_name):
    print(f"Tab clicked: {tab_name}")  # Console output only
```

**Acceptance Criteria:**
- [ ] Bottom nav appears at bottom of window
- [ ] 4 buttons visible: Home, Browse, Collections, History
- [ ] Clicking each button prints tab name to console
- [ ] No screen switching yet (just console output)

**Manual Test:**
```bash
python main.py
# Click each tab button
# Verify console prints: "Tab clicked: Home", etc.
```

**Stop Conditions:**
- DO NOT create screen classes yet
- DO NOT implement screen switching
- DO NOT add icons to buttons

---

### Task 5: Add Welcome Screen (Dummy)

**Scope:** Create minimal Welcome screen that displays when app opens.

**Files to Create:**
- `ui/screens/welcome.py`

**What to Build:**
```python
# ui/screens/welcome.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class WelcomeScreen(QWidget):
    play_random_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        title = QLabel("Welcome to Deep-Sea")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Stream Phish concerts from phish.in")
        subtitle.setObjectName("caption")
        subtitle.setAlignment(Qt.AlignCenter)
        
        play_btn = QPushButton("Play Random Show")
        play_btn.setObjectName("primary")
        play_btn.clicked.connect(self.play_random_clicked.emit)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(32)
        layout.addWidget(play_btn)
        layout.addStretch()
```

**Files to Modify:**
- `main.py` (add screen container and show Welcome)

```python
# In DeepSeaApp.__init__:
from ui.screens.welcome import WelcomeScreen
from PyQt5.QtWidgets import QVBoxLayout, QWidget

# Create central widget with layout
central = QWidget()
main_layout = QVBoxLayout(central)
main_layout.setContentsMargins(0, 0, 0, 0)

# Add screen container
self.screen_container = QWidget()
screen_layout = QVBoxLayout(self.screen_container)
self.current_screen = WelcomeScreen()
self.current_screen.play_random_clicked.connect(
    lambda: print("Play Random clicked")
)
screen_layout.addWidget(self.current_screen)

# Add to main layout
main_layout.addWidget(self.screen_container)
main_layout.addWidget(self.bottom_nav)

self.setCentralWidget(central)
```

**Acceptance Criteria:**
- [ ] Welcome screen displays on app launch
- [ ] Title and subtitle visible and centered
- [ ] "Play Random Show" button visible
- [ ] Clicking button prints "Play Random clicked" to console
- [ ] Bottom nav still visible below screen

**Manual Test:**
```bash
python main.py
# Verify Welcome screen appears
# Click "Play Random Show" button
# Verify console output
```

**Stop Conditions:**
- DO NOT implement actual random show selection
- DO NOT add API calls
- DO NOT create other screens yet

**Milestone 1 Complete:** You now have a working PyQt5 app with gradient background, QSS loaded, bottom nav, and one screen. App runs without errors. Commit and get approval before Milestone 2.

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

**Scope:** Display list of shows from API with basic info.

**Files to Create:**
- `ui/screens/browse.py`

**What to Build:**
```python
# ui/screens/browse.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QListWidget, 
                              QListWidgetItem, QLabel, QPushButton)
from PyQt5.QtCore import pyqtSignal, Qt
from data import PhishInAPI
import logging

logger = logging.getLogger(__name__)

class BrowseScreen(QWidget):
    show_selected = pyqtSignal(str)  # Emits show date
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_shows()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Browse Shows")
        title.setObjectName("h2")
        layout.addWidget(title)
        
        # Shows list
        self.shows_list = QListWidget()
        self.shows_list.setObjectName("shows-list")
        self.shows_list.itemClicked.connect(self.on_show_clicked)
        layout.addWidget(self.shows_list)
    
    def load_shows(self):
        """Load recent shows from API."""
        try:
            # Get shows from 1997 (known good data)
            shows = PhishInAPI.get_shows(year=1997, audio_status='complete')
            
            for show in shows[:20]:  # Limit to 20 for now
                # Format: "1997-12-31 - MSG, New York, NY"
                date = show['date']
                venue = show.get('venue', {})
                if isinstance(venue, dict):
                    venue_name = venue.get('name', 'Unknown Venue')
                    venue_location = f"{venue.get('city', '')}, {venue.get('state', '')}"
                else:
                    venue_name = str(venue)
                    venue_location = ""
                
                item_text = f"{date} - {venue_name}"
                if venue_location:
                    item_text += f", {venue_location}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, date)  # Store date for selection
                self.shows_list.addItem(item)
            
            logger.info(f"Loaded {len(shows)} shows")
            
        except Exception as e:
            logger.error(f"Failed to load shows: {e}")
            error_item = QListWidgetItem(f"Error loading shows: {e}")
            self.shows_list.addItem(error_item)
    
    def on_show_clicked(self, item):
        """Handle show selection."""
        show_date = item.data(Qt.UserRole)
        if show_date:
            logger.info(f"Show selected: {show_date}")
            self.show_selected.emit(show_date)
```

**Files to Modify:**
- `main.py` (add Browse screen to tab switching)

```python
# In DeepSeaApp, modify on_tab_changed:
def on_tab_changed(self, tab_name):
    # Clear current screen
    layout = self.screen_container.layout()
    if layout.count() > 0:
        old_screen = layout.itemAt(0).widget()
        layout.removeWidget(old_screen)
        old_screen.deleteLater()
    
    # Add new screen
    if tab_name == "Home":
        screen = WelcomeScreen()
        screen.play_random_clicked.connect(
            lambda: print("Play Random clicked")
        )
    elif tab_name == "Browse":
        from ui.screens.browse import BrowseScreen
        screen = BrowseScreen()
        screen.show_selected.connect(
            lambda date: print(f"Show selected: {date}")
        )
    else:
        screen = QLabel(f"{tab_name} Screen\n(Coming Soon)")
        screen.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(screen)
    self.current_screen = screen
```

**Acceptance Criteria:**
- [ ] Browse tab displays list of shows
- [ ] Each item shows: date, venue, location
- [ ] Clicking a show prints date to console
- [ ] No crashes when switching between Home and Browse tabs
- [ ] API errors display in list (don't crash app)

**Manual Test:**
```bash
python main.py
# Click Browse tab
# Verify shows load
# Click a show
# Verify console prints: "Show selected: 1997-12-31"
```

**Stop Conditions:**
- DO NOT create Player screen yet
- DO NOT load full show details
- DO NOT play audio yet

---

### Task 9: Create Player Screen (Dummy)

**Scope:** Create Player screen layout WITHOUT audio integration.

**Files to Create:**
- `ui/screens/player.py`

**What to Build:**
```python
# ui/screens/player.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QPushButton)
from PyQt5.QtCore import Qt

class PlayerScreen(QWidget):
    def __init__(self, show_data):
        super().__init__()
        self.show_data = show_data
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left column: Metadata
        left_column = QVBoxLayout()
        
        # Show date
        date_label = QLabel(self.show_data['date'])
        date_label.setObjectName("h2")
        left_column.addWidget(date_label)
        
        # Venue
        venue = self.show_data.get('venue', {})
        if isinstance(venue, dict):
            venue_text = venue.get('name', 'Unknown Venue')
        else:
            venue_text = str(venue)
        venue_label = QLabel(venue_text)
        venue_label.setObjectName("caption")
        left_column.addWidget(venue_label)
        
        # Track list
        tracks_label = QLabel("Tracks:")
        tracks_label.setObjectName("h4")
        left_column.addWidget(tracks_label)
        
        for track in self.show_data.get('tracks', []):
            track_title = track.get('title', 'Unknown')
            track_label = QLabel(f"• {track_title}")
            left_column.addWidget(track_label)
        
        left_column.addStretch()
        
        # Right column: Controls (placeholder)
        right_column = QVBoxLayout()
        
        now_playing = QLabel("Now Playing")
        now_playing.setObjectName("h3")
        now_playing.setAlignment(Qt.AlignCenter)
        right_column.addWidget(now_playing)
        
        play_btn = QPushButton("▶ Play")
        play_btn.setObjectName("primary")
        right_column.addWidget(play_btn)
        
        next_btn = QPushButton("⏭ Next")
        next_btn.setObjectName("secondary")
        right_column.addWidget(next_btn)
        
        right_column.addStretch()
        
        # Add columns to main layout
        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(right_column, 1)
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
- [ ] Player displays show date and venue
- [ ] Player displays track list
- [ ] Play and Next buttons visible (no functionality yet)
- [ ] No crashes when loading Player

**Manual Test:**
```bash
python main.py
# Click Browse tab
# Click a show
# Verify Player screen appears with show info
```

**Stop Conditions:**
- DO NOT implement audio playback yet
- DO NOT add Equalizer yet
- DO NOT add progress bar yet

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
track_urls = [track['mp3_url'] for track in self.show_data['tracks']]
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

**Scope:** Display favorited shows in Collections screen.

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

**Scope:** Add simple date selection to Browse screen.

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
