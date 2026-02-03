"""
Now Playing Card Widget
Displays the currently playing track with controls and visualizer.
Part of the Player Screen right column.
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider
)

from ui.design_tokens import colors, typography, spacing, border_radius
from ui.components.equalizer import EqualizerWidget


class PlayerControlsWidget(QWidget):
    """Player control buttons (previous, play/pause, next)."""

    # Signals
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_playing = False
        self.setup_ui()

    def setup_ui(self):
        """Set up control buttons layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.spacing_4)

        # Previous button
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setObjectName("control_btn")
        self.prev_btn.setFixedSize(spacing.touch_target, spacing.touch_target)
        self.prev_btn.clicked.connect(self.previous_clicked.emit)

        # Play/Pause button (larger)
        self.play_pause_btn = QPushButton("▶")
        self.play_pause_btn.setObjectName("play_btn")
        self.play_pause_btn.setFixedSize(60, 60)
        self.play_pause_btn.clicked.connect(self.on_play_pause_clicked)

        # Next button
        self.next_btn = QPushButton("⏭")
        self.next_btn.setObjectName("control_btn")
        self.next_btn.setFixedSize(spacing.touch_target, spacing.touch_target)
        self.next_btn.clicked.connect(self.next_clicked.emit)

        # Apply styling
        control_style = f"""
            QPushButton#control_btn {{
                background-color: {colors.card};
                color: {colors.foreground};
                border: 1px solid {colors.border};
                border-radius: {border_radius.radius_lg}px;
                font-size: 20px;
            }}
            QPushButton#control_btn:hover {{
                background-color: rgba(139, 92, 246, 0.25);
                color: {colors.primary};
            }}
            QPushButton#control_btn:pressed {{
                background-color: rgba(139, 92, 246, 0.35);
            }}
        """

        play_style = f"""
            QPushButton#play_btn {{
                background-color: {colors.primary};
                color: {colors.deep_purple_start};
                border: none;
                border-radius: 30px;
                font-size: 24px;
            }}
            QPushButton#play_btn:hover {{
                background-color: {colors.primary_hover};
            }}
            QPushButton#play_btn:pressed {{
                background-color: {colors.purple_500};
            }}
        """

        self.prev_btn.setStyleSheet(control_style)
        self.play_pause_btn.setStyleSheet(play_style)
        self.next_btn.setStyleSheet(control_style)

        # Layout
        layout.addStretch()
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.play_pause_btn)
        layout.addWidget(self.next_btn)
        layout.addStretch()

    def on_play_pause_clicked(self):
        """Handle play/pause button click."""
        if self.is_playing:
            self.set_paused()
            self.pause_clicked.emit()
        else:
            self.set_playing()
            self.play_clicked.emit()

    def set_playing(self):
        """Update button to show pause state."""
        self.is_playing = True
        self.play_pause_btn.setText("⏸")

    def set_paused(self):
        """Update button to show play state."""
        self.is_playing = False
        self.play_pause_btn.setText("▶")


class ProgressBarWidget(QWidget):
    """Progress bar with time labels."""

    # Signals
    seek_requested = pyqtSignal(float)  # Emit position (0.0-1.0)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.duration = 0
        self.setup_ui()

    def setup_ui(self):
        """Set up progress bar layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing.spacing_2)

        # Time row
        time_row = QHBoxLayout()
        time_row.setContentsMargins(0, 0, 0, 0)

        self.current_time_label = QLabel("0:00")
        self.current_time_label.setObjectName("caption")
        self.current_time_label.setStyleSheet(f"""
            QLabel#caption {{
                color: {colors.foreground};
                font-size: {typography.caption_size}px;
            }}
        """)

        self.duration_label = QLabel("0:00")
        self.duration_label.setObjectName("caption")
        self.duration_label.setStyleSheet(f"""
            QLabel#caption {{
                color: rgba(240, 240, 240, 0.7);
                font-size: {typography.caption_size}px;
            }}
        """)

        time_row.addWidget(self.current_time_label)
        time_row.addStretch()
        time_row.addWidget(self.duration_label)

        layout.addLayout(time_row)

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setObjectName("progress_slider")
        self.slider.setRange(0, 1000)  # Use 0-1000 for smooth progress
        self.slider.setValue(0)
        self.slider.setStyleSheet(f"""
            QSlider#progress_slider::groove:horizontal {{
                background: {colors.card};
                height: 8px;
                border-radius: 4px;
            }}
            QSlider#progress_slider::handle:horizontal {{
                background: {colors.primary};
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }}
            QSlider#progress_slider::sub-page:horizontal {{
                background: {colors.primary};
                border-radius: 4px;
            }}
        """)

        self.slider.sliderMoved.connect(self.on_slider_moved)

        layout.addWidget(self.slider)

    def set_duration(self, duration_seconds: int):
        """Set the total duration."""
        self.duration = duration_seconds
        self.duration_label.setText(self.format_time(duration_seconds))

    def set_position(self, position_seconds: int):
        """Update the current position."""
        self.current_time_label.setText(self.format_time(position_seconds))
        if self.duration > 0:
            progress = position_seconds / self.duration
            self.slider.setValue(int(progress * 1000))

    def on_slider_moved(self, value: int):
        """Handle slider movement (seeking)."""
        position = value / 1000.0  # Convert to 0.0-1.0
        self.seek_requested.emit(position)

    @staticmethod
    def format_time(seconds: int) -> str:
        """Format seconds as MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"


class NowPlayingCardWidget(QWidget):
    """
    Now Playing Card - displays current track with controls.

    Signals:
        play_clicked: User clicked play
        pause_clicked: User clicked pause
        previous_clicked: User clicked previous
        next_clicked: User clicked next
        seek_requested: User scrubbed progress bar (position: float 0.0-1.0)
    """

    # Signals
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    previous_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    seek_requested = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        # Load placeholder data for testing
        self.load_placeholder_data()

    def setup_ui(self):
        """Set up the now playing card layout."""
        self.setObjectName("now_playing_card")

        # Card styling
        self.setStyleSheet(f"""
            QWidget#now_playing_card {{
                background-color: {colors.card};
                border: 1px solid {colors.border};
                border-radius: {border_radius.radius_xl}px;
            }}
        """)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            spacing.spacing_6,
            spacing.spacing_6,
            spacing.spacing_6,
            spacing.spacing_6
        )
        layout.setSpacing(spacing.spacing_5)

        # Equalizer (large)
        self.equalizer = EqualizerWidget(size="large")
        self.equalizer.setObjectName("equalizer_large")
        layout.addWidget(self.equalizer, alignment=Qt.AlignCenter)

        # Track title
        self.track_title = QLabel("Track Title")
        self.track_title.setObjectName("h1")
        self.track_title.setAlignment(Qt.AlignCenter)
        self.track_title.setWordWrap(True)
        self.track_title.setStyleSheet(f"""
            QLabel#h1 {{
                color: {colors.foreground};
                font-size: {typography.h1_size}px;
                font-weight: {typography.weight_medium};
            }}
        """)
        layout.addWidget(self.track_title)

        # Track subtitle (set info)
        self.track_subtitle = QLabel("Set 1 • Track 3")
        self.track_subtitle.setObjectName("caption")
        self.track_subtitle.setAlignment(Qt.AlignCenter)
        self.track_subtitle.setStyleSheet(f"""
            QLabel#caption {{
                color: rgba(240, 240, 240, 0.7);
                font-size: {typography.caption_size}px;
            }}
        """)
        layout.addWidget(self.track_subtitle)

        layout.addSpacing(spacing.spacing_4)

        # Progress bar
        self.progress_bar = ProgressBarWidget()
        self.progress_bar.seek_requested.connect(self.seek_requested.emit)
        layout.addWidget(self.progress_bar)

        layout.addSpacing(spacing.spacing_3)

        # Player controls
        self.controls = PlayerControlsWidget()
        self.controls.play_clicked.connect(self.play_clicked.emit)
        self.controls.pause_clicked.connect(self.pause_clicked.emit)
        self.controls.previous_clicked.connect(self.previous_clicked.emit)
        self.controls.next_clicked.connect(self.next_clicked.emit)
        layout.addWidget(self.controls)

        layout.addStretch()

    def load_placeholder_data(self):
        """Load placeholder data for testing."""
        self.set_track_data({
            'title': 'You Enjoy Myself',
            'set_info': 'Set 1 • Track 3',
            'duration': 1263  # 21:03 in seconds
        })

    def set_track_data(self, track_data: dict):
        """
        Update the card with track data.

        Args:
            track_data: Dictionary with keys:
                - title: str
                - set_info: str (e.g., "Set 1 • Track 3")
                - duration: int (seconds)
        """
        self.track_title.setText(track_data.get('title', 'Unknown Track'))
        self.track_subtitle.setText(track_data.get('set_info', ''))
        self.progress_bar.set_duration(track_data.get('duration', 0))

    def start_playback(self):
        """Start visualizer animation."""
        self.equalizer.start()
        self.controls.set_playing()

    def stop_playback(self):
        """Stop visualizer animation."""
        self.equalizer.stop()
        self.controls.set_paused()

    def update_position(self, position_seconds: int):
        """Update playback position."""
        self.progress_bar.set_position(position_seconds)
