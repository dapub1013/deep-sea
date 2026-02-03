# Audio Engine Usage Guide

Quick reference for using the Deep-Sea audio engine in your UI code.

---

## Basic Setup

```python
from PyQt5.QtWidgets import QMainWindow
from audio import AudioEngine

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create audio engine
        self.audio_engine = AudioEngine()

        # Connect signals
        self._connect_audio_signals()

    def _connect_audio_signals(self):
        """Connect audio engine signals to UI handlers."""
        self.audio_engine.playback_started.connect(self.on_playback_started)
        self.audio_engine.playback_paused.connect(self.on_playback_paused)
        self.audio_engine.playback_stopped.connect(self.on_playback_stopped)
        self.audio_engine.track_changed.connect(self.on_track_changed)
        self.audio_engine.position_changed.connect(self.on_position_changed)
        self.audio_engine.error_occurred.connect(self.on_error_occurred)
```

## Loading a Show

```python
# Show data structure (from phish.in API)
show_data = {
    'date': '1997-12-31',
    'venue': {'name': 'Madison Square Garden'},
    'tracks': [
        {
            'title': 'Down with Disease',
            'position': 1,
            'duration': 840,  # seconds
            'mp3': 'https://phish.in/audio/000/035/199/35199.mp3'
        },
        # ... more tracks
    ]
}

# Load into engine
self.audio_engine.load_show(show_data)
```

## Playback Control

```python
# Play
self.audio_engine.play()

# Pause
self.audio_engine.pause()

# Stop
self.audio_engine.stop()

# Jump to specific track
self.audio_engine.jump_to_track(5)  # Jump to track 5 (0-based)

# Volume control
self.audio_engine.set_volume(80)  # 0-100
```

## Getting State

```python
# Check if playing
is_playing = self.audio_engine.is_playing()

# Check if paused
is_paused = self.audio_engine.is_paused()

# Get current position
position = self.audio_engine.get_current_position()  # seconds

# Get current track index
track_index = self.audio_engine.get_current_track_index()  # 0-based

# Get current track metadata
track = self.audio_engine.get_current_track()
if track:
    print(f"Now playing: {track['title']}")
```

## Signal Handlers

```python
def on_playback_started(self):
    """Called when playback starts."""
    print("Playback started")
    self.play_button.setText("Pause")
    self.equalizer.start()

def on_playback_paused(self):
    """Called when playback pauses."""
    print("Playback paused")
    self.play_button.setText("Play")
    self.equalizer.stop()

def on_playback_stopped(self):
    """Called when playback stops."""
    print("Playback stopped")
    self.play_button.setText("Play")
    self.equalizer.stop()

def on_track_changed(self, track_index):
    """Called when track changes."""
    track = self.audio_engine.get_current_track()
    if track:
        print(f"Track {track_index + 1}: {track['title']}")
        self.now_playing_label.setText(track['title'])

def on_position_changed(self, position):
    """Called periodically with playback position."""
    # Update progress bar
    self.progress_bar.setValue(int(position))

def on_error_occurred(self, error_message):
    """Called when an error occurs."""
    print(f"Error: {error_message}")
    self.status_label.setText(f"Error: {error_message}")
```

## Complete Example

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from audio import AudioEngine
from data import PhishInAPI
import sys

class SimplePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Phish Player")

        # Create audio engine
        self.audio_engine = AudioEngine()
        self.audio_engine.playback_started.connect(lambda: self.play_btn.setText("Pause"))
        self.audio_engine.playback_paused.connect(lambda: self.play_btn.setText("Play"))
        self.audio_engine.track_changed.connect(self.update_track_label)

        # Create UI
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.track_label = QLabel("No track loaded")
        layout.addWidget(self.track_label)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)

        # Load a show
        try:
            show = PhishInAPI.get_show("1997-12-31")
            self.audio_engine.load_show(show)
            self.track_label.setText(f"Loaded: {show['date']}")
        except Exception as e:
            self.track_label.setText(f"Error: {e}")

    def toggle_play(self):
        if self.audio_engine.is_playing():
            self.audio_engine.pause()
        else:
            self.audio_engine.play()

    def update_track_label(self, track_index):
        track = self.audio_engine.get_current_track()
        if track:
            self.track_label.setText(f"Track {track_index + 1}: {track['title']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = SimplePlayer()
    player.show()
    sys.exit(app.exec_())
```

## Available Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `playback_started` | None | Emitted when playback starts |
| `playback_paused` | None | Emitted when playback pauses |
| `playback_stopped` | None | Emitted when playback stops |
| `track_changed` | `int` track_index | Emitted when track changes (0-based) |
| `position_changed` | `float` seconds | Emitted periodically with position |
| `volume_changed` | `int` volume | Emitted when volume changes (0-100) |
| `error_occurred` | `str` message | Emitted when an error occurs |

## Tips

1. **Always connect signals before loading shows** to ensure you don't miss events
2. **Handle errors gracefully** - network issues can cause stream failures
3. **Use position_changed sparingly** - update UI throttled to avoid performance issues
4. **Volume is 0-100** - convert to/from other scales as needed
5. **Track indices are 0-based** - add 1 when displaying to users

---

*For more details, see the implementation in `audio/engine.py`*
