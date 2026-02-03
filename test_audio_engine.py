#!/usr/bin/env python3
"""
Audio Engine Integration Test

Tests the miniaudio integration with HTTPStreamSource and basic playback.
This script loads a short sample show and tests playback functionality.
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

from audio import AudioEngine
from data import PhishInAPI

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class AudioTestWindow(QMainWindow):
    """Simple test window for audio playback."""

    def __init__(self):
        super().__init__()
        self.audio_engine = None
        self.current_show = None
        self.setup_ui()
        self.setup_audio()

    def setup_ui(self):
        """Create test UI."""
        self.setWindowTitle("Deep-Sea Audio Engine Test")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Status label
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #7c3aed;")
        layout.addWidget(self.status_label)

        # Track info label
        self.track_label = QLabel("No track loaded")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("font-size: 12px; color: #a78bfa;")
        layout.addWidget(self.track_label)

        # Control buttons
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play_clicked)
        self.play_button.setEnabled(False)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.on_pause_clicked)
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        layout.addStretch()

    def setup_audio(self):
        """Initialize audio engine and load test show."""
        try:
            # Create audio engine
            self.audio_engine = AudioEngine()

            # Connect signals
            self.audio_engine.playback_started.connect(self.on_playback_started)
            self.audio_engine.playback_paused.connect(self.on_playback_paused)
            self.audio_engine.playback_stopped.connect(self.on_playback_stopped)
            self.audio_engine.track_changed.connect(self.on_track_changed)
            self.audio_engine.error_occurred.connect(self.on_error_occurred)

            self.status_label.setText("Loading test show...")

            # Load a sample show from phish.in
            # Using 1997-12-31 (NYE) - iconic show with just a few tracks to test
            logger.info("Fetching show from phish.in API...")
            show_data = PhishInAPI.get_show("1997-12-31")

            if show_data:
                # Limit to first 2 tracks for testing
                show_data['tracks'] = show_data['tracks'][:2]

                self.current_show = show_data
                self.audio_engine.load_show(show_data)

                show_date = show_data.get('date', 'Unknown')
                track_count = len(show_data['tracks'])

                self.status_label.setText(f"Show loaded: {show_date} ({track_count} tracks)")
                self.play_button.setEnabled(True)

                logger.info(f"Show loaded: {show_date} with {track_count} tracks")

        except Exception as e:
            error_msg = f"Failed to initialize: {str(e)}"
            self.status_label.setText(error_msg)
            logger.error(error_msg, exc_info=True)

    def on_play_clicked(self):
        """Handle play button click."""
        if self.audio_engine:
            self.audio_engine.play()

    def on_pause_clicked(self):
        """Handle pause button click."""
        if self.audio_engine:
            self.audio_engine.pause()

    def on_stop_clicked(self):
        """Handle stop button click."""
        if self.audio_engine:
            self.audio_engine.stop()

    def on_playback_started(self):
        """Handle playback started signal."""
        self.status_label.setText("Playing...")
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        logger.info("UI: Playback started")

    def on_playback_paused(self):
        """Handle playback paused signal."""
        self.status_label.setText("Paused")
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        logger.info("UI: Playback paused")

    def on_playback_stopped(self):
        """Handle playback stopped signal."""
        self.status_label.setText("Stopped")
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        logger.info("UI: Playback stopped")

    def on_track_changed(self, track_index):
        """Handle track changed signal."""
        if self.current_show and 0 <= track_index < len(self.current_show['tracks']):
            track = self.current_show['tracks'][track_index]
            track_title = track.get('title', 'Unknown')
            self.track_label.setText(f"Track {track_index + 1}: {track_title}")
            logger.info(f"UI: Track changed to {track_index} - {track_title}")

    def on_error_occurred(self, error_message):
        """Handle error signal."""
        self.status_label.setText(f"Error: {error_message}")
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        logger.error(f"UI: Error occurred - {error_message}")


def main():
    """Run audio engine test."""
    logger.info("Starting Deep-Sea Audio Engine Test")

    app = QApplication(sys.argv)

    # Create and show test window
    window = AudioTestWindow()
    window.show()

    logger.info("Test window displayed")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
