"""
Player Screen
Main playback interface with two-column layout.
Left: Show metadata + track list
Right: Now playing card with controls
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout
)

from ui.design_tokens import spacing
from ui.components.show_metadata import ShowMetadataWidget
from ui.components.track_list import TrackListWidget
from ui.components.now_playing_card import NowPlayingCardWidget


class PlayerScreen(QWidget):
    """
    Player Screen - Two-column layout implementing Phase 4 design.

    Layout:
    ┌─────────────────────────────────────────────────────────┐
    │                    Player Screen                        │
    ├───────────────────────────┬─────────────────────────────┤
    │  Left Column (50%)        │  Right Column (50%)         │
    │                           │                             │
    │  ┌─────────────────────┐  │  ┌───────────────────────┐ │
    │  │  Show Metadata      │  │  │                       │ │
    │  │  • Album Art        │  │  │   Now Playing Card    │ │
    │  │  • Venue            │  │  │   • Equalizer         │ │
    │  │  • Date/Location    │  │  │   • Track Info        │ │
    │  │  • Source           │  │  │   • Progress Bar      │ │
    │  └─────────────────────┘  │  │   • Controls          │ │
    │                           │  │                       │ │
    │  ┌─────────────────────┐  │  │                       │ │
    │  │                     │  │  │                       │ │
    │  │   Track List        │  │  │                       │ │
    │  │   (Scrollable)      │  │  │                       │ │
    │  │                     │  │  └───────────────────────┘ │
    │  │                     │  │                             │
    │  │                     │  │                             │
    │  └─────────────────────┘  │                             │
    └───────────────────────────┴─────────────────────────────┘

    Signals:
        track_selected: User selected a track from list (track_index)
        play_clicked: User clicked play
        pause_clicked: User clicked pause
        previous_clicked: User clicked previous track
        next_clicked: User clicked next track
        seek_requested: User scrubbed progress bar (position: 0.0-1.0)
    """

    # Signals for audio engine integration
    track_selected = pyqtSignal(int)
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    seek_requested = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_track_index = 0
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Set up the two-column layout."""
        self.setObjectName("player_screen")

        # Main horizontal layout (two columns)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(
            spacing.spacing_6,
            spacing.spacing_6,
            spacing.spacing_6,
            spacing.spacing_6
        )
        main_layout.setSpacing(spacing.spacing_6)

        # Left column: metadata + track list
        left_column = QVBoxLayout()
        left_column.setSpacing(spacing.spacing_4)

        self.metadata_widget = ShowMetadataWidget()
        left_column.addWidget(self.metadata_widget)

        self.track_list = TrackListWidget()
        left_column.addWidget(self.track_list, 1)  # Give track list remaining space

        # Right column: now playing card
        right_column = QVBoxLayout()
        right_column.setSpacing(0)

        self.now_playing_card = NowPlayingCardWidget()
        right_column.addWidget(self.now_playing_card)
        right_column.addStretch()

        # Add columns to main layout (50/50 split)
        main_layout.addLayout(left_column, 1)
        main_layout.addLayout(right_column, 1)

    def connect_signals(self):
        """Connect component signals to screen signals."""
        # Track list selection
        self.track_list.track_selected.connect(self.on_track_selected)

        # Now playing card controls
        self.now_playing_card.play_clicked.connect(self.play_clicked.emit)
        self.now_playing_card.pause_clicked.connect(self.pause_clicked.emit)
        self.now_playing_card.previous_clicked.connect(self.previous_clicked.emit)
        self.now_playing_card.next_clicked.connect(self.next_clicked.emit)
        self.now_playing_card.seek_requested.connect(self.seek_requested.emit)

    def on_track_selected(self, track_index: int):
        """Handle track selection from list."""
        self.current_track_index = track_index
        self.track_selected.emit(track_index)

        # Update now playing card (placeholder - will be replaced with real data)
        # In real implementation, this will be driven by audio engine
        tracks = self.track_list.tracks
        if 0 <= track_index < len(tracks):
            track = tracks[track_index]
            self.now_playing_card.set_track_data({
                'title': track['title'],
                'set_info': f'Track {track_index + 1}',
                'duration': self.parse_duration(track['duration'])
            })

    @staticmethod
    def parse_duration(duration_str: str) -> int:
        """Parse MM:SS duration string to seconds."""
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                mins, secs = map(int, parts)
                return mins * 60 + secs
        except:
            pass
        return 0

    def load_show(self, show_data: dict):
        """
        Load a show into the player.

        Args:
            show_data: Dictionary with keys:
                - venue: str
                - date: str (YYYY-MM-DD)
                - location: str
                - source: str (optional)
                - album_art_url: str (optional)
                - tracks: list of dicts with 'title' and 'duration'
        """
        # Update metadata
        self.metadata_widget.set_show_data({
            'venue': show_data.get('venue'),
            'date': show_data.get('date'),
            'location': show_data.get('location'),
            'source': show_data.get('source'),
            'album_art_url': show_data.get('album_art_url')
        })

        # Update track list
        tracks = show_data.get('tracks', [])
        self.track_list.set_tracks(tracks)

        # Select first track
        if tracks:
            self.track_list.set_current_track(0)
            self.on_track_selected(0)

    def start_playback(self):
        """
        Start playback (called by audio engine).
        Updates UI to show playing state.
        """
        self.now_playing_card.start_playback()

    def stop_playback(self):
        """
        Stop playback (called by audio engine).
        Updates UI to show paused state.
        """
        self.now_playing_card.stop_playback()

    def update_position(self, position_seconds: int):
        """
        Update playback position (called by audio engine).

        Args:
            position_seconds: Current position in seconds
        """
        self.now_playing_card.update_position(position_seconds)

    def set_current_track(self, track_index: int):
        """
        Set the currently playing track (called by audio engine).

        Args:
            track_index: Index of the track (0-based)
        """
        self.current_track_index = track_index
        self.track_list.set_current_track(track_index)

        # Update now playing card
        tracks = self.track_list.tracks
        if 0 <= track_index < len(tracks):
            track = tracks[track_index]
            self.now_playing_card.set_track_data({
                'title': track['title'],
                'set_info': f'Track {track_index + 1}',
                'duration': self.parse_duration(track['duration'])
            })
