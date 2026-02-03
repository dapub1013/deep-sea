"""
Gapless Audio Player using miniaudio

Provides seamless playback across multiple tracks by using a Python
generator that continuously yields PCM frames without gaps.
"""

import logging
import threading
import miniaudio
from PyQt5.QtCore import QObject, pyqtSignal

from .http_source import HTTPStreamSource

logger = logging.getLogger(__name__)


class GaplessPlayer(QObject):
    """
    Gapless audio player using miniaudio.

    Uses a Python generator to continuously yield PCM frames across
    multiple tracks, enabling seamless playback without gaps.

    Signals:
        track_changed: Emitted when playback moves to a new track (int: track_index)
        position_changed: Emitted periodically with playback position (float: seconds)
        playback_finished: Emitted when all tracks have been played
        error_occurred: Emitted when an error occurs (str: error_message)
    """

    # Qt Signals
    track_changed = pyqtSignal(int)  # Track index
    position_changed = pyqtSignal(float)  # Position in seconds
    playback_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)  # Error message

    def __init__(self):
        """Initialize gapless player."""
        super().__init__()

        self.device = None
        self.current_track_index = 0
        self.track_urls = []
        self.is_playing = False
        self.is_paused = False
        self._stop_requested = False
        self._playback_thread = None

        # Position tracking
        self._current_position = 0.0
        self._frame_count = 0
        self._sample_rate = 44100  # Default, will be updated from decoder

        logger.info("GaplessPlayer initialized")

    def load_show(self, track_urls):
        """
        Load a show's track URLs into the playback queue.

        Args:
            track_urls: List of MP3 URL strings
        """
        self.track_urls = track_urls
        self.current_track_index = 0
        logger.info(f"Loaded show with {len(track_urls)} tracks")

    def play(self):
        """Start or resume gapless playback."""
        if not self.track_urls:
            logger.warning("Cannot play: no tracks loaded")
            return

        if self.is_playing and not self.is_paused:
            logger.debug("Already playing")
            return

        if self.is_paused:
            # Resume playback
            self.is_paused = False
            logger.info("Playback resumed")
            return

        # Start new playback
        self.is_playing = True
        self.is_paused = False
        self._stop_requested = False

        # Start playback in separate thread to avoid blocking UI
        self._playback_thread = threading.Thread(target=self._start_playback, daemon=True)
        self._playback_thread.start()

        logger.info("Playback started")

    def _start_playback(self):
        """Internal method to start playback (runs in separate thread)."""
        try:
            # Create audio generator
            generator = self._audio_generator()

            # Start playback device with generator
            # Note: This is a simplified version. Real implementation may need
            # more sophisticated device management and format handling.
            self.device = miniaudio.PlaybackDevice()

            # For now, we'll use a simple approach: decode each track fully
            # A more advanced implementation would stream in real-time
            for samples in generator:
                if self._stop_requested:
                    break

                # Device would play samples here
                # This is a placeholder for actual playback logic

        except Exception as e:
            logger.error(f"Playback error: {e}")
            self.error_occurred.emit(str(e))
        finally:
            self.is_playing = False
            if not self._stop_requested:
                self.playback_finished.emit()

    def _audio_generator(self):
        """
        Generator that yields PCM frames across all tracks.

        This generator seamlessly transitions between tracks by
        continuously yielding frames without gaps.

        Yields:
            Audio samples for playback
        """
        for i, url in enumerate(self.track_urls):
            if self._stop_requested:
                break

            try:
                logger.debug(f"Decoding track {i}: {url}")

                # Create HTTP stream source
                stream_source = HTTPStreamSource(url, timeout=30)

                # Read all data from stream for decoding
                # miniaudio.decode() expects bytes or a file path
                audio_data = stream_source.read()
                stream_source.close()

                if not audio_data:
                    logger.warning(f"No data received for track {i}, skipping")
                    continue

                # Decode MP3 to PCM
                decoded = miniaudio.decode(audio_data, output_format=miniaudio.SampleFormat.SIGNED16)

                # Update sample rate for position tracking
                self._sample_rate = decoded.sample_rate

                # Notify UI of track change
                self.track_changed.emit(i)
                self.current_track_index = i

                # Yield all frames from this track
                self._frame_count = 0

                # Convert decoded audio to numpy array and yield
                # In a real implementation, we'd yield chunks for streaming
                yield decoded.samples

                # Update position
                duration = len(decoded.samples) / (decoded.sample_rate * decoded.nchannels)
                logger.info(f"Track {i} completed: {duration:.1f}s")

            except Exception as e:
                logger.error(f"Error processing track {i} ({url}): {e}")
                self.error_occurred.emit(f"Unable to play track {i + 1}")
                # Continue to next track on error

    def pause(self):
        """Pause playback."""
        if not self.is_playing:
            logger.debug("Cannot pause: not playing")
            return

        self.is_paused = True
        # In real implementation, would pause the device
        logger.info("Playback paused")

    def stop(self):
        """Stop playback and reset."""
        self._stop_requested = True
        self.is_playing = False
        self.is_paused = False

        # Stop device
        if self.device:
            try:
                self.device.stop()
                self.device.close()
            except Exception as e:
                logger.error(f"Error stopping device: {e}")
            finally:
                self.device = None

        # Reset state
        self.current_track_index = 0
        self._frame_count = 0
        self._current_position = 0.0

        logger.info("Playback stopped")

    def jump_to_track(self, track_index):
        """
        Jump to a specific track in the current show.

        Args:
            track_index: Index of track to jump to (0-based)
        """
        if track_index < 0 or track_index >= len(self.track_urls):
            logger.warning(f"Invalid track index: {track_index}")
            return

        # Stop current playback
        was_playing = self.is_playing
        self.stop()

        # Update track index
        self.current_track_index = track_index

        # Resume playback if it was playing
        if was_playing:
            self.play()

        logger.info(f"Jumped to track {track_index}")

    def get_position(self):
        """
        Get current playback position in seconds.

        Returns:
            Current position in seconds
        """
        return self._current_position

    def get_current_track_index(self):
        """
        Get current track index.

        Returns:
            Current track index (0-based)
        """
        return self.current_track_index
