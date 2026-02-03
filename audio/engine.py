"""
Audio Engine - High-level API

Provides a clean interface for audio playback with Qt signal integration
for UI updates.
"""

import logging
from PyQt5.QtCore import QObject, pyqtSignal

from .gapless_player import GaplessPlayer

logger = logging.getLogger(__name__)


class AudioEngine(QObject):
    """
    High-level audio engine API.

    Coordinates playback operations and emits signals for UI synchronization.

    Signals:
        playback_started: Emitted when playback starts
        playback_paused: Emitted when playback pauses
        playback_stopped: Emitted when playback stops
        track_changed: Emitted when current track changes (int: track_index)
        position_changed: Emitted periodically with position (float: seconds)
        volume_changed: Emitted when volume changes (int: 0-100)
        error_occurred: Emitted when an error occurs (str: error_message)
    """

    # Signals
    playback_started = pyqtSignal()
    playback_paused = pyqtSignal()
    playback_stopped = pyqtSignal()
    track_changed = pyqtSignal(int)  # Track index
    position_changed = pyqtSignal(float)  # Position in seconds
    volume_changed = pyqtSignal(int)  # Volume 0-100
    error_occurred = pyqtSignal(str)  # Error message

    def __init__(self):
        """Initialize audio engine."""
        super().__init__()

        # Create gapless player
        self.player = GaplessPlayer()

        # Current state
        self.current_show = None
        self.volume = 80  # Default volume (0-100)
        self._is_playing = False
        self._is_paused = False

        # Connect player signals to engine signals
        self.player.track_changed.connect(self._on_track_changed)
        self.player.position_changed.connect(self._on_position_changed)
        self.player.playback_finished.connect(self._on_playback_finished)
        self.player.error_occurred.connect(self._on_error_occurred)

        logger.info("AudioEngine initialized")

    def load_show(self, show_data):
        """
        Load a show for playback.

        Args:
            show_data: Dictionary containing show metadata and tracks
                      Expected format: {'date': '1997-12-31', 'tracks': [...]}
        """
        self.current_show = show_data

        # Extract MP3 URLs from tracks
        track_urls = [track['mp3'] for track in show_data['tracks']]

        # Load into player
        self.player.load_show(track_urls)

        logger.info(f"Show loaded: {show_data.get('date', 'unknown')} ({len(track_urls)} tracks)")

    def play(self):
        """Start playback."""
        if not self.current_show:
            logger.warning("Cannot play: no show loaded")
            self.error_occurred.emit("No show loaded")
            return

        self.player.play()
        self._is_playing = True
        self._is_paused = False
        self.playback_started.emit()

        logger.info("Playback started")

    def pause(self):
        """Pause playback."""
        if not self._is_playing:
            logger.debug("Cannot pause: not playing")
            return

        self.player.pause()
        self._is_paused = True
        self.playback_paused.emit()

        logger.info("Playback paused")

    def stop(self):
        """Stop playback."""
        self.player.stop()
        self._is_playing = False
        self._is_paused = False
        self.playback_stopped.emit()

        logger.info("Playback stopped")

    def jump_to_track(self, track_index):
        """
        Jump to a specific track in the current show.

        Args:
            track_index: Index of track to jump to (0-based)
        """
        if not self.current_show:
            logger.warning("Cannot jump to track: no show loaded")
            return

        self.player.jump_to_track(track_index)
        self.track_changed.emit(track_index)

        logger.info(f"Jumped to track {track_index}")

    def set_volume(self, volume):
        """
        Set playback volume.

        Args:
            volume: Volume level (0-100)
        """
        # Clamp volume to valid range
        volume = max(0, min(100, volume))

        self.volume = volume

        # TODO: Apply volume to miniaudio device
        # This requires device-level volume control which we'll implement later

        self.volume_changed.emit(volume)

        logger.debug(f"Volume set to {volume}")

    def seek(self, position_seconds):
        """
        Seek to position in current track.

        Note: Not supported in v1 for HTTP streams.

        Args:
            position_seconds: Target position in seconds

        Raises:
            NotImplementedError: Seeking not supported for HTTP streams
        """
        raise NotImplementedError("Seeking not supported for HTTP streams in v1")

    def get_current_position(self):
        """
        Get current playback position.

        Returns:
            Current position in seconds
        """
        return self.player.get_position()

    def get_current_track_index(self):
        """
        Get current track index.

        Returns:
            Current track index (0-based)
        """
        return self.player.get_current_track_index()

    def get_current_track(self):
        """
        Get current track metadata.

        Returns:
            Track dictionary or None if no show loaded
        """
        if not self.current_show:
            return None

        track_index = self.player.get_current_track_index()
        if 0 <= track_index < len(self.current_show['tracks']):
            return self.current_show['tracks'][track_index]

        return None

    def is_playing(self):
        """
        Check if audio is currently playing.

        Returns:
            True if playing, False otherwise
        """
        return self._is_playing and not self._is_paused

    def is_paused(self):
        """
        Check if playback is paused.

        Returns:
            True if paused, False otherwise
        """
        return self._is_paused

    # Internal signal handlers

    def _on_track_changed(self, track_index):
        """Handle track change from player."""
        self.track_changed.emit(track_index)
        logger.debug(f"Track changed to {track_index}")

    def _on_position_changed(self, position):
        """Handle position update from player."""
        self.position_changed.emit(position)

    def _on_playback_finished(self):
        """Handle playback completion."""
        self._is_playing = False
        self._is_paused = False
        self.playback_stopped.emit()
        logger.info("Playback finished")

    def _on_error_occurred(self, error_message):
        """Handle error from player."""
        self.error_occurred.emit(error_message)
        logger.error(f"Player error: {error_message}")
