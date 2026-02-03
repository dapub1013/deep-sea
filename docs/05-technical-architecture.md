# Deep-Sea — Technical Architecture Decision

**Phase 5 Deliverable | February 2, 2026**

---

## 1. Executive Summary

This document defines the complete technical architecture for Deep-Sea v1. The architecture leverages proven technologies (PyQt5, miniaudio) with a design-first implementation approach to deliver a modern, polished desktop music streaming application.

**Key Decisions:**
- **UI Framework:** PyQt5 6.x with QSS styling
- **Audio Engine:** miniaudio (pyminiaudio Python wrapper)
- **Design Implementation:** Phase 4 specifications translated to PyQt5/QSS
- **Target Platforms:** macOS (development) + Raspberry Pi 4 (production)

This architecture prioritizes simplicity, proven patterns, and direct reusability for the future Grateful Dead app refactor.

---

## 2. Technology Stack

### 2.1 Core Technologies

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **UI Framework** | PyQt5 | 6.x | Proven for music streaming apps, native desktop feel, works on RPi |
| **Styling** | QSS (Qt Style Sheets) | — | CSS-like declarative styling, implements Phase 4 design tokens |
| **Audio Engine** | pyminiaudio | 1.61+ | Gapless HTTP streaming, PCM frame access, cross-platform |
| **HTTP Client** | requests | 2.31+ | Simple, reliable API integration with phish.in |
| **Data Persistence** | SQLite | 3.x (built-in) | Local storage for favorites, history, collections |
| **State Management** | Qt Signals/Slots | — | Built-in event system, proven pattern |
| **Build Tool (macOS)** | PyInstaller | 6.x | Single-file app bundle with dependencies |
| **Python Runtime** | Python | 3.11+ | Modern Python with performance improvements |

### 2.2 Development Dependencies

| Package | Purpose |
|---------|---------|
| **pyminiaudio** | Audio playback engine (MP3 decoding, PCM streaming) |
| **PyQt5** | UI framework and widgets |
| **requests** | HTTP client for phish.in API calls |
| **Pillow** | Image loading and caching (album art, waveforms) |
| **PyInstaller** | Application bundling for macOS distribution |

### 2.3 Runtime Dependencies (Raspberry Pi)

| Package | Purpose |
|---------|---------|
| **Python 3.11+** | Runtime environment |
| **PyQt5** | UI framework (install via apt: `python3-pyqt5`) |
| **pyminiaudio** | Audio engine (pre-built wheel available on PiWheels) |
| **ALSA** | Audio subsystem for IQAudio DAC |

---

## 3. Architecture Overview

### 3.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Deep-Sea Application                     │
│                        (Python Process)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │   UI Layer       │          │  Audio Engine    │         │
│  │   (PyQt5)        │◄────────►│  (miniaudio)     │         │
│  │                  │  Signals │                  │         │
│  │  - Screens       │  & Slots │  - Playback      │         │
│  │  - Components    │          │  - Streaming     │         │
│  │  - QSS Styling   │          │  - PCM Frames    │         │
│  └──────────────────┘          └──────────────────┘         │
│           │                             │                    │
│           │                             │                    │
│           ▼                             ▼                    │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │  State Manager   │          │  HTTP Streamer   │         │
│  │  (Python Models) │          │  (Adapter)       │         │
│  │                  │          │                  │         │
│  │  - Player State  │          │  - MP3 Download  │         │
│  │  - Current Show  │          │  - Buffer Mgmt   │         │
│  │  - Track Queue   │          │  - Gapless Queue │         │
│  └──────────────────┘          └──────────────────┘         │
│           │                             │                    │
│           │                             │                    │
│           ▼                             ▼                    │
│  ┌─────────────────────────────────────────────────┐        │
│  │              Data Layer                         │        │
│  │                                                  │        │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────┐ │        │
│  │  │ API Client  │  │ Local Cache  │  │ SQLite │ │        │
│  │  │ (requests)  │  │ (Disk)       │  │ (DB)   │ │        │
│  │  └─────────────┘  └──────────────┘  └────────┘ │        │
│  └─────────────────────────────────────────────────┘        │
│           │                    │              │              │
└───────────┼────────────────────┼──────────────┼──────────────┘
            │                    │              │
            ▼                    ▼              ▼
    ┌──────────────┐    ┌──────────────┐  ┌─────────┐
    │  phish.in    │    │  File System │  │  Local  │
    │  API         │    │  (Images)    │  │  Data   │
    └──────────────┘    └──────────────┘  └─────────┘
```

### 3.2 Component Responsibilities

#### UI Layer (PyQt5)
- **Screens:** Full-screen views (Welcome, Player, Browse, Collections, History, Tour Detail)
- **Components:** Reusable widgets (Equalizer, PlayerControls, TrackList, NowPlayingBar, etc.)
- **QSS Styling:** Design token implementation (colors, spacing, typography from Phase 4)
- **User Input:** Touch and mouse event handling, validation

#### Audio Engine (miniaudio)
- **Playback Control:** Play, pause, stop, seek, volume
- **Streaming:** HTTP MP3 download and decode via custom `StreamableSource` adapter
- **Gapless Playback:** Continuous PCM buffer feeding via Python generator
- **Frame Access:** PCM data callbacks for future visualizer (Nice-to-Have)

#### State Manager (Python Data Models)
- **Player State:** Current track, playback position, volume, play/pause status
- **Show State:** Current show metadata, track list, source info
- **Queue State:** Track queue, history, next/previous logic
- **Persistence:** Save/restore state across sessions (resume on reconnect)

#### Data Layer
- **API Client:** RESTful calls to phish.in (shows, tours, tracks, metadata)
- **Cache Manager:** Disk cache for album art, waveforms, API responses
- **Database:** SQLite for favorites, collections, listening history

---

## 4. Implementation Strategy

### 4.1 Phase 4 Design → PyQt5 Translation

The Phase 4 prototype provides exact specifications that must be implemented pixel-perfect in PyQt5. The translation process:

#### 4.1.1 Design Tokens → QSS Variables

**Phase 4 CSS Variables:**
```css
--purple-400: #a78bfa;
--purple-600: #7c3aed;
--purple-800: #5b21b6;
--spacing-4: 16px;
--radius: 12px;
--touch-target: 44px;
```

**PyQt5 QSS Implementation:**
```css
/* Global Style Sheet (styles/main.qss) */

/* Color Palette */
QWidget {
    --purple-50:  #f5f3ff;
    --purple-400: #a78bfa;
    --purple-600: #7c3aed;
    --purple-800: #5b21b6;
    --deep-purple-start: #1a0b2e;
    --deep-purple-mid: #2d1b4e;
    --deep-purple-end: #4c1d95;
}

/* Typography will be set programmatically via QFont */
/* Spacing will use consistent px values matching 8pt grid */
```

**Note:** QSS does not support CSS custom properties (variables) natively. We'll use a Python-based token system that generates QSS with hardcoded values, or use string replacement to inject variables.

#### 4.1.2 Component Mapping

| Phase 4 Component | PyQt5 Implementation |
|-------------------|---------------------|
| **Equalizer** | Custom `QWidget` with `paintEvent()` for animated bars |
| **PlayerControls** | `QWidget` with `QPushButton` children, QSS styled |
| **ProgressBar** | `QSlider` with custom QSS and scrubbing logic |
| **VolumeControl** | `QSlider` (vertical/horizontal) with mute toggle |
| **TrackList** | `QListWidget` with custom item delegates for styling |
| **NowPlayingBar** | `QWidget` with horizontal layout, show/hide animation |
| **TouchDatePicker** | Custom `QWidget` with `QSpinBox` or custom scroll wheels |
| **ShowCard** | Custom `QWidget` with `QLabel` children, QSS card styling |
| **TourCard** | Custom `QWidget` with `QLabel` children, QSS card styling |
| **TopNav** | `QWidget` with title `QLabel` and action buttons |
| **BottomNav** | `QTabWidget` or custom `QWidget` with tab-like buttons |
| **PrimaryButton** | `QPushButton` with custom QSS (44px min, rounded, purple) |

#### 4.1.3 Screen Implementation

Each screen is a `QWidget` subclass that composes components:

```python
class PlayerScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Two-column layout (Phase 4 spec)
        layout = QHBoxLayout(self)
        
        # Left column: metadata + track list
        left_column = QVBoxLayout()
        self.metadata_widget = ShowMetadataWidget()
        self.track_list = TrackListWidget()
        left_column.addWidget(self.metadata_widget)
        left_column.addWidget(self.track_list)
        
        # Right column: now playing card
        right_column = QVBoxLayout()
        self.now_playing_card = NowPlayingCardWidget()
        right_column.addWidget(self.now_playing_card)
        
        layout.addLayout(left_column, 1)  # 50% width
        layout.addLayout(right_column, 1)  # 50% width
```

### 4.2 QSS Styling Approach

**Global Stylesheet Structure:**

```
styles/
├── main.qss              # Global styles, color palette, base widgets
├── components.qss        # Component-specific styles (buttons, cards, etc.)
├── screens.qss           # Screen-specific layout adjustments
└── animations.qss        # Transition and animation definitions (if supported)
```

**Loading Stylesheets:**

```python
def load_stylesheet(app):
    """Load and apply QSS stylesheets to application."""
    qss_files = [
        'styles/main.qss',
        'styles/components.qss',
        'styles/screens.qss',
    ]
    
    stylesheet = ""
    for qss_file in qss_files:
        with open(qss_file, 'r') as f:
            stylesheet += f.read() + "\n"
    
    app.setStyleSheet(stylesheet)
```

**Example: Gradient Background Implementation**

QSS does not support `linear-gradient()` like CSS. We'll use `QPalette` and `QLinearGradient` programmatically:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_gradient_background()
    
    def set_gradient_background(self):
        """Apply Phase 4 purple gradient background."""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#1a0b2e"))  # Deep purple start
        gradient.setColorAt(0.5, QColor("#2d1b4e"))  # Deep purple mid
        gradient.setColorAt(1.0, QColor("#4c1d95"))  # Deep purple end
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
```

**Example: Card Component Styling**

```css
/* components.qss */

QWidget#card {
    background-color: rgba(139, 92, 246, 38);  /* Purple-500 at 15% opacity */
    border-radius: 12px;
    padding: 16px;
}

QWidget#card QLabel#title {
    font-size: 20px;
    font-weight: 500;
    color: #f0f0f0;
}

QWidget#card QLabel#caption {
    font-size: 14px;
    color: rgba(240, 240, 240, 0.7);
}
```

**Blur Effects (Phase 4 `backdrop-blur`):**

QSS does not support `backdrop-filter`. We'll use `QGraphicsBlurEffect`:

```python
class CardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        
        # Apply blur effect for frosted glass appearance
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(20)
        self.setGraphicsEffect(blur)
```

### 4.3 Custom Component Examples

#### 4.3.1 Equalizer Component

The Equalizer is a signature visual element (Must-Have). The exact styling is deferred until the developer provides the animation example from the Grateful Dead application. The implementation below demonstrates the general pattern (5-bar animated equalizer), but the visual appearance will be refined based on the proven GD app animation.

```python
class EqualizerWidget(QWidget):
    """Animated 5-bar equalizer matching Phase 4 design."""
    
    def __init__(self, size="compact", parent=None):
        super().__init__(parent)
        self.size = size  # "compact" (40px) or "large" (120px)
        self.bar_heights = [0.3, 0.6, 0.8, 0.5, 0.4]  # Normalized heights
        self.is_playing = False
        
        # Set fixed size based on variant
        if size == "compact":
            self.setFixedSize(40, 40)
        else:  # large
            self.setFixedSize(120, 120)
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_bars)
    
    def start(self):
        """Start animation."""
        self.is_playing = True
        self.timer.start(100)  # Update every 100ms
    
    def stop(self):
        """Stop animation."""
        self.is_playing = False
        self.timer.stop()
        self.update()
    
    def animate_bars(self):
        """Animate bar heights randomly."""
        import random
        self.bar_heights = [random.uniform(0.2, 1.0) for _ in range(5)]
        self.update()
    
    def paintEvent(self, event):
        """Draw 5 animated bars with purple gradient."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        bar_width = width / 7  # 5 bars + 4 gaps
        gap = bar_width / 2
        
        # Define gradient (dark to light purple)
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor("#5b21b6"))  # Purple-800 (dark)
        gradient.setColorAt(0.5, QColor("#7c3aed"))  # Purple-600 (mid)
        gradient.setColorAt(1.0, QColor("#a78bfa"))  # Purple-400 (light)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        
        # Draw 5 bars
        for i in range(5):
            x = i * (bar_width + gap)
            bar_height = height * self.bar_heights[i] if self.is_playing else height * 0.1
            y = height - bar_height
            
            # Rounded rectangle for each bar
            painter.drawRoundedRect(
                int(x), int(y), int(bar_width), int(bar_height),
                4, 4  # Corner radius
            )
```

**Usage:**
```python
# Compact equalizer in Now Playing Bar
equalizer_compact = EqualizerWidget(size="compact")
equalizer_compact.start()  # Start animation when playing

# Large equalizer in Player Screen
equalizer_large = EqualizerWidget(size="large")
equalizer_large.start()
```

#### 4.3.2 Touch-Optimized Button

All buttons must meet 44px minimum touch target (Phase 4 requirement).

```python
class TouchButton(QPushButton):
    """Touch-optimized button with 44px minimum size."""
    
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(text, parent)
        
        # Set minimum size for touch targets
        self.setMinimumSize(44, 44)
        
        # Apply icon if provided
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))
```

**QSS Styling:**
```css
TouchButton {
    background-color: #a78bfa;  /* Purple-400 */
    color: #1a0b2e;  /* Dark text on light button */
    border-radius: 12px;
    font-size: 16px;
    font-weight: 500;
    padding: 12px 24px;
}

TouchButton:hover {
    background-color: #c4b5fd;  /* Purple-300 */
}

TouchButton:pressed {
    background-color: #8b5cf6;  /* Purple-500 */
}
```

### 4.4 State Management Pattern

Qt's built-in **signals and slots** system handles state propagation. No external state library needed.

#### State Flow Example: Play Button Click

```python
# Component: PlayerControls
class PlayerControls(QWidget):
    # Define signal
    play_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.play_button = TouchButton("Play")
        self.play_button.clicked.connect(self.on_play_clicked)
    
    def on_play_clicked(self):
        # Emit signal to audio engine
        if self.is_playing:
            self.pause_requested.emit()
        else:
            self.play_requested.emit()

# Audio Engine: AudioPlayer
class AudioPlayer(QObject):
    # Define signals
    playback_started = pyqtSignal()
    playback_paused = pyqtSignal()
    position_changed = pyqtSignal(float)  # Emit current position in seconds
    
    def __init__(self):
        super().__init__()
        self.device = None
        self.is_playing = False
    
    def play(self):
        """Start playback."""
        # miniaudio playback logic here
        self.is_playing = True
        self.playback_started.emit()
    
    def pause(self):
        """Pause playback."""
        # miniaudio pause logic here
        self.is_playing = False
        self.playback_paused.emit()

# Main application: wire signals
class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.audio_player = AudioPlayer()
        self.player_controls = PlayerControls()
        
        # Connect UI signals to audio engine
        self.player_controls.play_requested.connect(self.audio_player.play)
        self.player_controls.pause_requested.connect(self.audio_player.pause)
        
        # Connect audio engine signals to UI updates
        self.audio_player.playback_started.connect(self.on_playback_started)
        self.audio_player.playback_paused.connect(self.on_playback_paused)
    
    def on_playback_started(self):
        """Update UI when playback starts."""
        self.equalizer.start()
        self.player_controls.update_button_state("pause")
    
    def on_playback_paused(self):
        """Update UI when playback pauses."""
        self.equalizer.stop()
        self.player_controls.update_button_state("play")
```

**Benefits of Signals/Slots:**
- Decoupled components (UI doesn't directly call audio engine)
- Type-safe event passing
- Automatic threading support (cross-thread signals)
- Built into PyQt5 (no external dependency)

---

## 5. Audio Engine Integration

### 5.1 miniaudio Architecture

The audio engine uses **pyminiaudio** with a custom HTTP streaming adapter to achieve gapless playback.

#### 5.1.1 HTTP Streaming Adapter

phish.in serves MP3 files via direct URLs. miniaudio requires a `StreamableSource` subclass to handle network streams.

```python
import miniaudio
import requests
from io import BytesIO

class HTTPStreamSource(miniaudio.StreamableSource):
    """Custom StreamableSource for HTTP MP3 streaming."""
    
    def __init__(self, url):
        self.url = url
        self.response = None
        self.buffer = BytesIO()
        self.position = 0
        
        # Start streaming download
        self.response = requests.get(url, stream=True)
        self.response.raise_for_status()
    
    def read(self, num_bytes):
        """Read bytes from HTTP stream."""
        # Download chunks on-demand
        chunk = self.response.raw.read(num_bytes)
        if not chunk:
            return b''  # EOF
        self.buffer.write(chunk)
        self.position += len(chunk)
        return chunk
    
    def seek(self, offset, origin):
        """Seek is not supported for HTTP streams."""
        raise NotImplementedError("Seeking not supported for HTTP streams")
```

#### 5.1.2 Gapless Playback with Python Generator

The key to gapless playback is feeding the `PlaybackDevice` a continuous stream of PCM frames from a Python generator that switches tracks seamlessly.

```python
import miniaudio

class GaplessPlayer:
    """Gapless audio player using miniaudio."""
    
    def __init__(self):
        self.device = None
        self.current_track_index = 0
        self.track_urls = []
        self.is_playing = False
    
    def load_show(self, track_urls):
        """Load a show's track URLs into the queue."""
        self.track_urls = track_urls
        self.current_track_index = 0
    
    def play(self):
        """Start gapless playback."""
        if not self.track_urls:
            return
        
        # Create generator that yields PCM frames across tracks
        def audio_generator():
            for i, url in enumerate(self.track_urls):
                if not self.is_playing:
                    break
                
                # Decode MP3 to PCM
                stream_source = HTTPStreamSource(url)
                decoder = miniaudio.decode(stream_source, output_format=miniaudio.SampleFormat.SIGNED16)
                
                # Yield all frames from this track
                for frame in decoder:
                    if not self.is_playing:
                        break
                    yield frame
                
                # No gap - immediately start next track
        
        # Start playback device with generator
        self.is_playing = True
        self.device = miniaudio.PlaybackDevice()
        self.device.start(audio_generator())
    
    def pause(self):
        """Pause playback."""
        self.is_playing = False
        if self.device:
            self.device.stop()
    
    def stop(self):
        """Stop playback and reset."""
        self.pause()
        self.current_track_index = 0
```

**How Gapless Works:**
1. Python generator yields PCM frames from track 1
2. When track 1 decoder exhausts, generator immediately yields frames from track 2
3. `PlaybackDevice` callback never starves - continuous PCM stream
4. No silence gap between tracks

#### 5.1.3 Playback State Tracking

Track when the current track changes for UI updates:

```python
class GaplessPlayer(QObject):
    # Signals for UI
    track_changed = pyqtSignal(int)  # Emit track index
    position_changed = pyqtSignal(float)  # Emit position in seconds
    
    def audio_generator(self):
        """Generator with track change notifications."""
        for i, url in enumerate(self.track_urls):
            if not self.is_playing:
                break
            
            # Notify UI of track change
            self.track_changed.emit(i)
            
            stream_source = HTTPStreamSource(url)
            decoder = miniaudio.decode(stream_source)
            
            frame_count = 0
            for frame in decoder:
                if not self.is_playing:
                    break
                yield frame
                
                # Emit position updates (every N frames)
                frame_count += 1
                if frame_count % 100 == 0:  # Every 100 frames
                    position_seconds = frame_count / decoder.sample_rate
                    self.position_changed.emit(position_seconds)
```

### 5.2 Audio Engine API

The audio engine exposes a clean Python API that the UI layer calls:

```python
class AudioEngine(QObject):
    """High-level audio engine API."""
    
    # Signals
    playback_started = pyqtSignal()
    playback_paused = pyqtSignal()
    playback_stopped = pyqtSignal()
    track_changed = pyqtSignal(int)  # Track index
    position_changed = pyqtSignal(float)  # Position in seconds
    volume_changed = pyqtSignal(int)  # Volume 0-100
    
    def __init__(self):
        super().__init__()
        self.player = GaplessPlayer()
        self.current_show = None
        self.volume = 80  # Default volume
    
    def load_show(self, show_data):
        """Load a show for playback."""
        self.current_show = show_data
        track_urls = [track['mp3_url'] for track in show_data['tracks']]
        self.player.load_show(track_urls)
    
    def play(self):
        """Start playback."""
        self.player.play()
        self.playback_started.emit()
    
    def pause(self):
        """Pause playback."""
        self.player.pause()
        self.playback_paused.emit()
    
    def stop(self):
        """Stop playback."""
        self.player.stop()
        self.playback_stopped.emit()
    
    def jump_to_track(self, track_index):
        """Jump to a specific track in the current show."""
        self.player.current_track_index = track_index
        self.player.play()
        self.track_changed.emit(track_index)
    
    def set_volume(self, volume):
        """Set volume (0-100)."""
        self.volume = volume
        # miniaudio volume control logic here
        self.volume_changed.emit(volume)
    
    def seek(self, position_seconds):
        """Seek to position (not supported in v1 for HTTP streams)."""
        raise NotImplementedError("Seeking not supported for HTTP streams")
```

**UI Integration:**
```python
# Main app
self.audio_engine = AudioEngine()

# Connect signals
self.audio_engine.track_changed.connect(self.on_track_changed)
self.audio_engine.position_changed.connect(self.update_progress_bar)

# User clicks play button
self.audio_engine.play()

# User jumps to track 5
self.audio_engine.jump_to_track(5)
```

---

## 6. Data Layer Architecture

### 6.1 API Client

Simple wrapper around `requests` for phish.in API calls.

```python
import requests
from typing import List, Dict, Optional

class PhishInAPI:
    """Client for phish.in API."""
    
    BASE_URL = "https://phish.in/api/v1"
    
    @staticmethod
    def get_shows(year: Optional[int] = None, audio_status: str = "complete") -> List[Dict]:
        """Get shows, optionally filtered by year and audio status."""
        url = f"{PhishInAPI.BASE_URL}/shows"
        params = {"audio_status": audio_status}
        if year:
            params["year"] = year
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['data']
    
    @staticmethod
    def get_show(show_date: str) -> Dict:
        """Get a specific show by date (YYYY-MM-DD)."""
        url = f"{PhishInAPI.BASE_URL}/shows/{show_date}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['data']
    
    @staticmethod
    def get_tours() -> List[Dict]:
        """Get all tours."""
        url = f"{PhishInAPI.BASE_URL}/tours"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['data']
    
    @staticmethod
    def get_tour(tour_slug: str) -> Dict:
        """Get a specific tour by slug."""
        url = f"{PhishInAPI.BASE_URL}/tours/{tour_slug}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['data']
```

### 6.2 Cache Manager

Disk cache for album art, waveforms, and API responses to reduce network calls.

```python
import os
import json
import hashlib
from pathlib import Path
from typing import Optional

class CacheManager:
    """Disk-based cache for API responses and images."""
    
    def __init__(self, cache_dir: str = "~/.deep-sea/cache"):
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.images_dir = self.cache_dir / "images"
        self.api_dir = self.cache_dir / "api"
        self.images_dir.mkdir(exist_ok=True)
        self.api_dir.mkdir(exist_ok=True)
    
    def get_image(self, url: str) -> Optional[Path]:
        """Get cached image path, or None if not cached."""
        filename = hashlib.md5(url.encode()).hexdigest() + ".png"
        filepath = self.images_dir / filename
        return filepath if filepath.exists() else None
    
    def cache_image(self, url: str, image_data: bytes) -> Path:
        """Cache image data and return filepath."""
        filename = hashlib.md5(url.encode()).hexdigest() + ".png"
        filepath = self.images_dir / filename
        filepath.write_bytes(image_data)
        return filepath
    
    def get_api_response(self, key: str) -> Optional[Dict]:
        """Get cached API response, or None if not cached."""
        filepath = self.api_dir / f"{key}.json"
        if filepath.exists():
            return json.loads(filepath.read_text())
        return None
    
    def cache_api_response(self, key: str, data: Dict):
        """Cache API response."""
        filepath = self.api_dir / f"{key}.json"
        filepath.write_text(json.dumps(data, indent=2))
```

**Usage:**
```python
cache = CacheManager()

# Check for cached album art
cached_path = cache.get_image(show['cover_art_urls']['large'])
if cached_path:
    pixmap = QPixmap(str(cached_path))
else:
    # Download and cache
    response = requests.get(show['cover_art_urls']['large'])
    cached_path = cache.cache_image(show['cover_art_urls']['large'], response.content)
    pixmap = QPixmap(str(cached_path))
```

### 6.3 Local Database (SQLite)

Store user data: favorites, collections, listening history.

**Schema:**

```sql
-- favorites.db

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_date TEXT NOT NULL UNIQUE,  -- YYYY-MM-DD
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE collection_shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id INTEGER NOT NULL,
    show_date TEXT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
);

CREATE TABLE listening_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_date TEXT NOT NULL,
    track_title TEXT,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE app_state (
    key TEXT PRIMARY KEY,
    value TEXT  -- JSON-encoded state
);
```

**Python Wrapper:**

```python
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    """SQLite database for user data."""
    
    def __init__(self, db_path: str = "~/.deep-sea/deep-sea.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Return rows as dicts
        self._init_schema()
    
    def _init_schema(self):
        """Create tables if they don't exist."""
        with open('schema.sql', 'r') as f:
            self.conn.executescript(f.read())
    
    # Favorites
    def add_favorite(self, show_date: str):
        """Add a show to favorites."""
        self.conn.execute("INSERT OR IGNORE INTO favorites (show_date) VALUES (?)", (show_date,))
        self.conn.commit()
    
    def remove_favorite(self, show_date: str):
        """Remove a show from favorites."""
        self.conn.execute("DELETE FROM favorites WHERE show_date = ?", (show_date,))
        self.conn.commit()
    
    def get_favorites(self) -> List[str]:
        """Get all favorite show dates."""
        cursor = self.conn.execute("SELECT show_date FROM favorites ORDER BY added_at DESC")
        return [row['show_date'] for row in cursor.fetchall()]
    
    # Collections
    def create_collection(self, name: str, description: str = "") -> int:
        """Create a new collection and return its ID."""
        cursor = self.conn.execute(
            "INSERT INTO collections (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def add_to_collection(self, collection_id: int, show_date: str):
        """Add a show to a collection."""
        self.conn.execute(
            "INSERT OR IGNORE INTO collection_shows (collection_id, show_date) VALUES (?, ?)",
            (collection_id, show_date)
        )
        self.conn.commit()
    
    # Listening history
    def add_to_history(self, show_date: str, track_title: str):
        """Record a played track in history."""
        self.conn.execute(
            "INSERT INTO listening_history (show_date, track_title) VALUES (?, ?)",
            (show_date, track_title)
        )
        self.conn.commit()
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Get recent listening history."""
        cursor = self.conn.execute(
            "SELECT show_date, track_title, played_at FROM listening_history "
            "ORDER BY played_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    # App state persistence
    def save_state(self, key: str, value: Dict):
        """Save app state (e.g., last played show, volume)."""
        self.conn.execute(
            "INSERT OR REPLACE INTO app_state (key, value) VALUES (?, ?)",
            (key, json.dumps(value))
        )
        self.conn.commit()
    
    def load_state(self, key: str) -> Optional[Dict]:
        """Load app state."""
        cursor = self.conn.execute("SELECT value FROM app_state WHERE key = ?", (key,))
        row = cursor.fetchone()
        return json.loads(row['value']) if row else None
```

**Resume on Reconnect Implementation:**

```python
# On app startup
db = Database()
last_state = db.load_state("player_state")

if last_state:
    # Restore playback state
    audio_engine.load_show(last_state['show_date'])
    audio_engine.jump_to_track(last_state['track_index'])
    audio_engine.seek(last_state['position_seconds'])  # If seek supported
    audio_engine.set_volume(last_state['volume'])

# On playback state change
def save_player_state():
    state = {
        'show_date': current_show_date,
        'track_index': audio_engine.current_track_index,
        'position_seconds': audio_engine.current_position,
        'volume': audio_engine.volume,
    }
    db.save_state("player_state", state)

# Call save_player_state() periodically or on app close
```

---

## 7. Build & Deployment Strategy

### 7.1 Development Environment Setup

**macOS Setup:**

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install PyQt5 pyminiaudio requests Pillow PyInstaller

# Verify installations
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import miniaudio; print('miniaudio OK')"
```

**Raspberry Pi Setup:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ (if not available, build from source or use deadsnakes PPA)
sudo apt install python3.11 python3.11-venv python3-pip

# Install system dependencies
sudo apt install python3-pyqt5 python3-pyqt5.qtmultimedia

# Install Python packages
pip3 install --break-system-packages pyminiaudio requests Pillow

# Verify miniaudio wheel from PiWheels
pip3 show pyminiaudio
```

### 7.2 Application Structure

```
deep-sea/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── schema.sql              # Database schema
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # QMainWindow subclass
│   ├── screens/            # Screen widgets
│   │   ├── welcome.py
│   │   ├── player.py
│   │   ├── browse.py
│   │   ├── collections.py
│   │   ├── history.py
│   │   └── tour_detail.py
│   └── components/         # Reusable widgets
│       ├── equalizer.py
│       ├── player_controls.py
│       ├── track_list.py
│       ├── now_playing_bar.py
│       └── ...
├── audio/
│   ├── __init__.py
│   ├── engine.py           # AudioEngine class
│   ├── gapless_player.py   # GaplessPlayer implementation
│   └── http_source.py      # HTTPStreamSource adapter
├── data/
│   ├── __init__.py
│   ├── api_client.py       # PhishInAPI class
│   ├── cache.py            # CacheManager class
│   └── database.py         # Database class
├── styles/
│   ├── main.qss            # Global styles
│   ├── components.qss      # Component styles
│   └── screens.qss         # Screen-specific styles
├── assets/
│   └── icons/              # Application icons
└── tests/                  # Unit tests (optional for v1)
```

### 7.3 macOS Packaging (PyInstaller)

**Build Script:**

```bash
# build_macos.sh

#!/bin/bash

# Clean previous builds
rm -rf build dist

# Build single-file app bundle
pyinstaller \
    --name "Deep-Sea" \
    --windowed \
    --onefile \
    --icon assets/icon.icns \
    --add-data "styles:styles" \
    --add-data "schema.sql:." \
    --hidden-import PyQt5 \
    --hidden-import miniaudio \
    main.py

echo "Build complete: dist/Deep-Sea.app"
```

**Post-Build:**
- App bundle is at `dist/Deep-Sea.app`
- Double-click to run (no terminal needed)
- Can be distributed as `.dmg` for easy installation

### 7.4 Raspberry Pi Deployment

**No packaging needed** - run directly from Python:

```bash
# Clone repository
git clone https://github.com/yourusername/deep-sea.git
cd deep-sea

# Install dependencies
pip3 install --break-system-packages -r requirements.txt

# Run application
python3 main.py
```

**Auto-Start on Boot (systemd service):**

```ini
# /etc/systemd/system/deep-sea.service

[Unit]
Description=Deep-Sea Phish Streaming Player
After=graphical.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
WorkingDirectory=/home/pi/deep-sea
ExecStart=/usr/bin/python3 /home/pi/deep-sea/main.py
Restart=on-failure

[Install]
WantedBy=graphical.target
```

**Enable auto-start:**

```bash
sudo systemctl enable deep-sea.service
sudo systemctl start deep-sea.service
```

**Kiosk Mode (Fullscreen on 7" Touchscreen):**

```python
# main.py

class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Detect if running on Raspberry Pi
        if self.is_raspberry_pi():
            self.showFullScreen()  # Fullscreen on RPi
        else:
            self.resize(1280, 720)  # Windowed on macOS
```

---

## 8. Security & Privacy Considerations

### 8.1 Data Privacy

**User Data Storage:**
- All user data (favorites, collections, history) stored **locally** in SQLite
- No cloud sync, no user accounts, no external data transmission
- User data never sent to phish.in or any third party

**Network Communications:**
- All API calls to phish.in are read-only (GET requests)
- MP3 streaming via HTTPS (Cloudflare CDN)
- No authentication tokens or credentials stored

**Privacy Principle:**
- Minimize data collection (only what's needed for features)
- Keep all data local by default
- No analytics, tracking, or telemetry

### 8.2 Dependency Security

**Third-Party Libraries:**
- PyQt5: Mature, widely-used, maintained by Riverbank Computing
- pyminiaudio: Thin wrapper around dr-soft/miniaudio (MIT licensed, actively maintained C library)
- requests: Industry-standard HTTP client, actively maintained
- Pillow: Well-maintained image library

**Security Checklist:**
- All dependencies are open-source and auditable
- No known critical vulnerabilities in chosen versions
- MIT/BSD licensing compatible with open-source release
- Regular `pip list --outdated` checks for security updates

### 8.3 Raspberry Pi Security

**Deployment Hardening:**
- Change default `pi` user password
- Disable SSH if not needed (or use key-based auth only)
- Enable automatic security updates: `sudo dpkg-reconfigure --priority=low unattended-upgrades`
- Firewall (ufw) if device is network-accessible: `sudo ufw enable`

**Application Security:**
- No web server exposed to network (local-only UI)
- No remote access features (v1)
- SQLite database has local filesystem permissions only

**Attack Surface:**
- Minimal: application reads from phish.in API, writes to local disk only
- No user input validation concerns (date picker is constrained UI)
- No SQL injection risk (parameterized queries)

### 8.4 Error Handling Architecture

A streaming application depends on external services (phish.in API, CDN) and network connectivity. Robust error handling is essential for reliable operation, especially on Raspberry Pi where users expect a kiosk-like experience.

#### 8.4.1 Error Handling Pattern

**Central Error Manager:**

Use a centralized `ErrorHandler` class that provides consistent error handling across the application. This prevents scattered try/catch blocks and ensures uniform user experience.

```python
class ErrorHandler(QObject):
    """Central error handling and user notification."""
    
    # Signals for UI notifications
    show_error = pyqtSignal(str, str)  # (title, message)
    show_warning = pyqtSignal(str, str)
    show_info = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('ErrorHandler')
    
    def handle_api_error(self, error, context=""):
        """Handle API request failures."""
        self.logger.error(f"API error: {error} (context: {context})")
        
        if isinstance(error, requests.exceptions.ConnectionError):
            self.show_error.emit(
                "Network Error",
                "Unable to connect to phish.in. Check your internet connection."
            )
        elif isinstance(error, requests.exceptions.Timeout):
            self.show_warning.emit(
                "Request Timeout",
                "The server is taking too long to respond. Try again in a moment."
            )
        elif isinstance(error, requests.exceptions.HTTPError):
            if error.response.status_code == 404:
                self.show_error.emit(
                    "Not Found",
                    f"The requested show was not found. {context}"
                )
            elif error.response.status_code >= 500:
                self.show_error.emit(
                    "Server Error",
                    "phish.in is experiencing issues. Try again later."
                )
        else:
            self.show_error.emit(
                "Error",
                f"An unexpected error occurred: {str(error)}"
            )
    
    def handle_stream_error(self, error, track_info):
        """Handle audio streaming failures."""
        self.logger.error(f"Stream error: {error} (track: {track_info})")
        self.show_warning.emit(
            "Playback Issue",
            f"Unable to play {track_info}. Skipping to next track."
        )
    
    def handle_database_error(self, error, operation):
        """Handle database failures."""
        self.logger.error(f"Database error: {error} (operation: {operation})")
        self.show_error.emit(
            "Database Error",
            f"Unable to {operation}. Your data may not be saved."
        )
```

**Usage:**
```python
# In API client
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
except Exception as e:
    error_handler.handle_api_error(e, context=f"fetching show {show_date}")
    return None  # Caller handles None gracefully
```

#### 8.4.2 Retry Logic Strategy

**Automatic Retry for Transient Failures:**

Network requests should retry automatically for transient errors (timeouts, connection errors) but fail fast for permanent errors (404, invalid data).

```python
import time
from functools import wraps

def retry_on_network_error(max_retries=3, backoff_factor=2):
    """Decorator for automatic retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, 
                        requests.exceptions.Timeout) as e:
                    if attempt == max_retries - 1:
                        raise  # Final attempt failed
                    
                    wait_time = backoff_factor ** attempt
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries}). "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
            
        return wrapper
    return decorator

# Usage in API client
@retry_on_network_error(max_retries=3, backoff_factor=2)
def get_show(show_date: str) -> Dict:
    """Get show with automatic retry on network errors."""
    url = f"{PhishInAPI.BASE_URL}/shows/{show_date}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()['data']
```

**Retry Policy:**
- **API calls:** Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- **MP3 streams:** Retry once immediately, then skip to next track
- **Image downloads:** No retry (fail silently, show placeholder)
- **Database operations:** No retry (fail fast, log error)

#### 8.4.3 User Notification Patterns

**Three Notification Levels:**

1. **Error (Modal Dialog)** - Blocks user interaction until acknowledged
   - Used for: Critical failures that prevent core functionality
   - Example: "Cannot initialize audio device"
   
2. **Warning (Toast/Banner)** - Non-blocking, auto-dismisses after 5s
   - Used for: Recoverable issues that user should know about
   - Example: "Unable to load album art"
   
3. **Info (Toast/Banner)** - Non-blocking, auto-dismisses after 3s
   - Used for: Success confirmations, status updates
   - Example: "Added to favorites"

**Implementation:**

```python
class NotificationManager(QObject):
    """Manage user notifications (errors, warnings, info)."""
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
    
    def show_error(self, title, message):
        """Show modal error dialog (blocking)."""
        QMessageBox.critical(self.parent, title, message)
    
    def show_warning(self, title, message):
        """Show warning toast (non-blocking, 5s auto-dismiss)."""
        self._show_toast(title, message, duration=5000, color="#f59e0b")
    
    def show_info(self, title, message):
        """Show info toast (non-blocking, 3s auto-dismiss)."""
        self._show_toast(title, message, duration=3000, color="#10b981")
    
    def _show_toast(self, title, message, duration, color):
        """Create animated toast notification."""
        toast = QWidget(self.parent)
        toast.setStyleSheet(f"""
            background-color: {color};
            border-radius: 8px;
            padding: 12px 16px;
        """)
        
        layout = QVBoxLayout(toast)
        title_label = QLabel(f"<b>{title}</b>")
        message_label = QLabel(message)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        
        # Position at top-right
        toast.move(self.parent.width() - toast.width() - 20, 20)
        toast.show()
        
        # Auto-dismiss after duration
        QTimer.singleShot(duration, toast.deleteLater)
```

#### 8.4.4 Network Failure Recovery

**API Unreachable:**
- Retry with exponential backoff (up to 3 attempts)
- If all retries fail, show cached data (if available)
- User sees warning: "Using cached data. Unable to connect to phish.in."

**Stream Timeout:**
- HTTPStreamSource times out after 30 seconds of no data
- Automatically retry stream download once
- If retry fails, skip to next track with warning notification
- Log error for debugging

**Decode Error (Corrupted MP3):**
- Catch miniaudio decode exceptions
- Skip to next track immediately
- Show warning: "Unable to play [track name]. Skipping."
- Log error with track URL for reporting to phish.in

**Implementation Pattern:**

```python
class GaplessPlayer:
    def audio_generator(self):
        """Generator with automatic error recovery."""
        for i, url in enumerate(self.track_urls):
            if not self.is_playing:
                break
            
            try:
                # Attempt to stream and decode
                stream_source = HTTPStreamSource(url, timeout=30)
                decoder = miniaudio.decode(stream_source)
                
                self.track_changed.emit(i)
                
                for frame in decoder:
                    if not self.is_playing:
                        break
                    yield frame
                    
            except requests.exceptions.Timeout:
                # Stream timeout - retry once
                logger.warning(f"Stream timeout for track {i}. Retrying...")
                try:
                    stream_source = HTTPStreamSource(url, timeout=30)
                    decoder = miniaudio.decode(stream_source)
                    for frame in decoder:
                        if not self.is_playing:
                            break
                        yield frame
                except Exception as retry_error:
                    # Retry failed - skip track
                    logger.error(f"Stream retry failed for track {i}: {retry_error}")
                    self.error_handler.handle_stream_error(retry_error, self.track_urls[i])
                    continue  # Skip to next track
                    
            except miniaudio.DecodeError as e:
                # Corrupted MP3 - skip immediately
                logger.error(f"Decode error for track {i}: {e}")
                self.error_handler.handle_stream_error(e, self.track_urls[i])
                continue  # Skip to next track
                
            except Exception as e:
                # Unknown error - log and skip
                logger.error(f"Unexpected error for track {i}: {e}")
                self.error_handler.handle_stream_error(e, self.track_urls[i])
                continue
```

#### 8.4.5 State Persistence Recovery

**Resume on Reconnect Edge Cases:**

When restoring saved player state, validate all data before use:

```python
def restore_player_state():
    """Restore playback state with validation."""
    logger = logging.getLogger('StateManager')
    
    try:
        saved_state = db.load_state("player_state")
        
        if not saved_state:
            logger.info("No saved state found. Starting fresh.")
            return
        
        # Validate show_date exists
        try:
            show_data = api_client.get_show(saved_state['show_date'])
            if not show_data:
                raise ValueError(f"Show {saved_state['show_date']} not found")
        except Exception as e:
            logger.warning(f"Cannot restore show {saved_state['show_date']}: {e}")
            return  # Skip restoration, start fresh
        
        # Validate track_index is in bounds
        track_index = saved_state.get('track_index', 0)
        if track_index >= len(show_data['tracks']):
            logger.warning(f"Track index {track_index} out of bounds. Resetting to 0.")
            track_index = 0
        
        # Restore state
        audio_engine.load_show(show_data)
        audio_engine.jump_to_track(track_index)
        audio_engine.set_volume(saved_state.get('volume', 80))
        
        logger.info(f"Restored state: {saved_state['show_date']} track {track_index}")
        
    except Exception as e:
        logger.error(f"Failed to restore state: {e}")
        # Fail gracefully - just start fresh
```

**Database Corruption:**
- Catch SQLite errors on startup
- If database is corrupted, rename it and create fresh DB
- User loses local data (favorites, history) but app still works
- Log error and show notification: "Database reset due to corruption. Your favorites have been cleared."

```python
def init_database():
    """Initialize database with corruption recovery."""
    try:
        db = Database()
        db.conn.execute("SELECT 1")  # Test query
        return db
    except sqlite3.DatabaseError as e:
        logger.error(f"Database corrupted: {e}. Creating fresh database.")
        
        # Backup corrupted DB
        corrupted_path = Path("~/.deep-sea/deep-sea.db").expanduser()
        backup_path = corrupted_path.with_suffix('.db.corrupted')
        corrupted_path.rename(backup_path)
        
        # Create fresh database
        db = Database()
        
        error_handler.show_warning(
            "Database Reset",
            "Your database was corrupted and has been reset. Favorites and history have been cleared."
        )
        
        return db
```

#### 8.4.6 Graceful Degradation

When components fail, the application should continue to function with reduced features:

**Cache Miss (No Internet):**
- API calls fail → show cached show list (if available)
- Album art fails → show placeholder image
- User can still browse cached shows and play if previously loaded

**Audio Device Unavailable:**
- miniaudio can't initialize → show error, disable playback controls
- User can still browse shows, manage favorites, view metadata
- Offer "Retry" button to reinitialize audio

**API Rate Limited:**
- Detect 429 status codes
- Pause API requests for 60 seconds
- Show cached data during pause
- Resume API calls after cooldown

### 8.5 Logging Strategy

Comprehensive logging is essential for debugging, performance monitoring, and diagnosing issues on Raspberry Pi where interactive debugging is difficult.

#### 8.5.1 Logging Framework

**Use Python's built-in `logging` module** - no external dependencies, well-understood, highly configurable.

**Logger Hierarchy:**
```
deep-sea (root logger)
├── ui (UI layer)
│   ├── ui.screens.player
│   ├── ui.screens.browse
│   └── ui.components.equalizer
├── audio (Audio engine)
│   ├── audio.engine
│   ├── audio.gapless_player
│   └── audio.http_source
├── data (Data layer)
│   ├── data.api_client
│   ├── data.cache
│   └── data.database
└── main (Application lifecycle)
```

**Setup:**
```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging(log_level=logging.INFO):
    """Configure application-wide logging."""
    
    # Create logs directory
    log_dir = Path.home() / ".deep-sea" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Root logger
    logger = logging.getLogger('deep-sea')
    logger.setLevel(log_level)
    
    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation (for production)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "deep-sea.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5  # Keep 5 old log files
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage in main.py
logger = setup_logging(log_level=logging.DEBUG)  # DEBUG during development
logger.info("Deep-Sea starting...")
```

#### 8.5.2 Log Levels and Usage

**DEBUG** - Detailed diagnostic information
- API request/response details (URLs, response times)
- State transitions (track changed, volume adjusted)
- Cache hits/misses
- Performance timings

```python
logger.debug(f"API GET {url} completed in {elapsed}ms")
logger.debug(f"Cache hit for {show_date}: {cached_path}")
```

**INFO** - Significant application events
- Application startup/shutdown
- Show loaded, playback started/stopped
- User actions (added to favorites, created collection)
- Configuration changes

```python
logger.info(f"Show loaded: {show_date} ({len(tracks)} tracks)")
logger.info(f"Playback started: {show_date} - {track_title}")
```

**WARNING** - Recoverable issues
- API retry attempts
- Stream timeout (with recovery)
- Cache miss (falling back to default)
- Deprecated features used

```python
logger.warning(f"API request failed. Retrying in {wait_time}s...")
logger.warning(f"Album art not found. Using placeholder.")
```

**ERROR** - Operation failures
- API request failed after retries
- Stream download failed
- Database write error
- Invalid data encountered

```python
logger.error(f"Failed to load show {show_date}: {error}")
logger.error(f"Stream failed for track {track_index}: {error}")
```

**CRITICAL** - Application-breaking failures
- Cannot initialize audio device
- Database corruption (before recovery)
- Missing required dependencies

```python
logger.critical(f"Failed to initialize miniaudio: {error}")
logger.critical(f"Database corrupted and recovery failed")
```

#### 8.5.3 What to Log

**Application Lifecycle:**
```python
logger.info("Deep-Sea v1.0 starting...")
logger.info(f"Platform: {platform.system()} {platform.release()}")
logger.info(f"Python: {sys.version}")
logger.info(f"PyQt5: {PyQt5.QtCore.PYQT_VERSION_STR}")
logger.info(f"Audio device initialized: {device_name}")
logger.info("Deep-Sea shutdown complete")
```

**API Interactions:**
```python
logger.debug(f"GET {url}")
logger.debug(f"Response: {response.status_code} ({response.elapsed.total_seconds():.2f}s)")
logger.info(f"Fetched {len(shows)} shows from API")
logger.error(f"API error: {response.status_code} {response.reason}")
```

**Audio Engine:**
```python
logger.info(f"Loading show: {show_date} ({track_count} tracks)")
logger.debug(f"Track changed: {track_index} -> {track_title}")
logger.debug(f"Playback position: {position_seconds:.1f}s / {duration_seconds:.1f}s")
logger.warning(f"Stream timeout for {track_url}. Retrying...")
logger.error(f"Decode error: {error} (track: {track_url})")
```

**User Actions:**
```python
logger.info(f"User added to favorites: {show_date}")
logger.info(f"User created collection: {collection_name}")
logger.debug(f"User navigated to screen: {screen_name}")
```

**Performance Metrics:**
```python
logger.debug(f"Image loaded in {elapsed_ms}ms: {image_url}")
logger.debug(f"Show metadata fetched in {elapsed_ms}ms")
logger.debug(f"Database query completed in {elapsed_ms}ms")
```

#### 8.5.4 Platform-Specific Configuration

**macOS (Development):**
- Log level: `DEBUG` (show everything)
- Console output: Enabled (see logs in terminal)
- File logging: Enabled (for reference)

**Raspberry Pi (Production):**
- Log level: `INFO` (reduce noise)
- Console output: Disabled (no terminal attached)
- File logging: Enabled with rotation
- systemd journal integration (optional)

```python
import platform

def setup_logging():
    """Platform-aware logging setup."""
    is_rpi = platform.machine().startswith('arm')
    
    if is_rpi:
        # Production mode on Raspberry Pi
        log_level = logging.INFO
        enable_console = False
    else:
        # Development mode on macOS
        log_level = logging.DEBUG
        enable_console = True
    
    logger = logging.getLogger('deep-sea')
    logger.setLevel(log_level)
    
    # File handler (always enabled)
    file_handler = logging.handlers.RotatingFileHandler(...)
    logger.addHandler(file_handler)
    
    # Console handler (dev only)
    if enable_console:
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
    
    return logger
```

#### 8.5.5 Privacy Considerations

**Never log sensitive data:**
- User's personal information (even if stored locally)
- Full file paths that expose username (use `~` instead)
- IP addresses or network identifiers

**Safe to log:**
- Show dates, track titles, venue names (public data from phish.in)
- Application state (volume level, current track index)
- Error messages and stack traces
- Performance metrics

**Example - Safe Logging:**
```python
# Good - no personal data
logger.info(f"Show loaded: 1997-12-31")
logger.debug(f"Cache path: ~/.deep-sea/cache/abc123.png")

# Bad - exposes username
logger.debug(f"Cache path: /Users/johnsmith/.deep-sea/cache/abc123.png")
```

#### 8.5.6 Log File Management

**Rotation Policy:**
- Maximum file size: 10 MB
- Keep 5 backup files (total ~50 MB log storage)
- Oldest logs automatically deleted when limit reached

**Location:**
- macOS: `~/.deep-sea/logs/deep-sea.log`
- Raspberry Pi: `~/.deep-sea/logs/deep-sea.log`

**User Access:**
- Logs are plain text files readable with any text editor
- Can be attached to bug reports or support requests
- Include "Open Logs Folder" option in app menu (future enhancement)

**Cleanup:**
- Logs are not automatically deleted (user must manually clean)
- Consider adding "Clear Old Logs" button in settings (v2 feature)

---

## 9. Open Questions & Future Considerations

### 9.1 Deferred to Phase 6 (Development)

These items require hands-on coding to resolve:

1. **QSS Variable System:** How to implement design tokens efficiently in QSS (string replacement vs. programmatic generation)?
2. **Equalizer Animation Performance:** Does QTimer + paintEvent() perform well on RPi 4 at 60fps?
3. **Image Loading Performance:** Should album art be loaded asynchronously to avoid UI blocking?
4. **Touch Gesture Support:** Are PyQt5's default touch events sufficient, or do we need custom gesture recognition?

### 9.2 Nice-to-Have Features (v2)

**Real-Time Audio Visualizer:**
- Use miniaudio's `frame_process_method` callback to extract PCM data
- Apply FFT (Fast Fourier Transform) to get frequency spectrum
- Replace static Equalizer with real-time frequency bars
- Requires additional dependency: `numpy` for FFT calculation

**Bluetooth Audio Output (Raspberry Pi):**
- Enable Bluetooth audio sink on RPi 4
- Switch output between IQAudio DAC (wired) and Bluetooth (wireless)
- Requires: `bluez` configuration and PyQt5 Bluetooth integration

**Song-Version Search:**
- Requires additional data source (Jamcharts only covers 5,008 tracks)
- Potential integration with user curation (manual tagging of notable versions)

### 9.3 Pattern Documentation for GD App Refactor

Throughout Phase 6, document the following reusable patterns:

1. **QSS Design Token System:** How to translate web design specs to PyQt5
2. **Gapless HTTP Streaming:** HTTPStreamSource + generator pattern
3. **Touch-Optimized Components:** 44px minimum sizing, touch-friendly layouts
4. **State Management:** Signals/slots patterns for audio ↔ UI communication
5. **API Client & Caching:** Reusable data layer architecture
6. **Database Schema:** SQLite structure for favorites/collections/history

---

## 10. Phase 5 Approval Checklist

Before proceeding to Phase 6 (Development), confirm:

- [x] **Technology Stack Approved:** PyQt5 + miniaudio + requests + SQLite
- [x] **Architecture Patterns Understood:** UI layer, audio engine, data layer separation
- [x] **Design Translation Approach Clear:** Phase 4 CSS → PyQt5 QSS mapping
- [x] **State Management Pattern Agreed:** Qt signals/slots for event propagation
- [x] **Audio Engine Integration Defined:** HTTPStreamSource + gapless generator
- [x] **Data Layer Architecture Accepted:** API client, cache manager, SQLite database
- [x] **Build & Deployment Strategy Clear:** PyInstaller (macOS), systemd (RPi)
- [x] **Security & Privacy Reviewed:** Local-only data, no tracking, minimal attack surface
- [x] **Open Questions Acknowledged:** Deferred items documented for Phase 6

---

## 11. Next Steps

**Phase 5 → Phase 6 Transition:**

1. **Developer Review:** Read this document, ask clarifying questions, approve architecture
2. **Environment Setup:** Install PyQt5, pyminiaudio, and dependencies on macOS
3. **Repository Initialization:** Set up Git repository with application structure
4. **Design Token Extraction:** Create QSS files with Phase 4 color/spacing/typography values
5. **Begin Development (Phase 6):**
   - Build base `QMainWindow` with gradient background
   - Implement Equalizer component (prove QSS styling + animations work)
   - Build Player Screen (compose components, test layout)
   - Integrate miniaudio (HTTPStreamSource + basic playback)
   - Iterate screen-by-screen, component-by-component

**Phase 6 Development Approach:**
- Start with visual components (Equalizer, buttons, cards) to validate QSS styling
- Build screens incrementally (Welcome → Player → Browse → Collections → History)
- Integrate audio engine after UI foundation is solid
- Test on macOS continuously, deploy to RPi for validation checkpoints

---

## 12. Approval

This document is approved when the developer confirms the architecture is clear, complete, and ready for implementation. Phase 6 may not begin until this approval is given.

**Developer Approval:** //signed human &nbsp; **Date:** February 2, 2026

**PM Acknowledgment:** Claude (AI) &nbsp; | &nbsp; **Date:** February 2, 2026

---

*Technical Architecture Decision v1.0 | Deep-Sea Project | Phase 5 Complete*
