#!/usr/bin/env python3
"""
Test script for Player Screen
Launch the Player Screen with placeholder data to test layout and components.
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.stylesheet_loader import apply_stylesheets, set_gradient_background
from ui.screens.player import PlayerScreen


class TestWindow(QMainWindow):
    """Test window for Player Screen."""

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.apply_styling()

    def setup_window(self):
        """Configure window."""
        self.setWindowTitle("Deep-Sea - Player Screen Test")
        self.resize(1280, 720)
        self.setMinimumSize(800, 600)

    def setup_ui(self):
        """Set up UI."""
        # Create player screen
        self.player_screen = PlayerScreen()

        # Connect signals for testing
        self.player_screen.track_selected.connect(self.on_track_selected)
        self.player_screen.play_clicked.connect(self.on_play_clicked)
        self.player_screen.pause_clicked.connect(self.on_pause_clicked)
        self.player_screen.previous_clicked.connect(self.on_previous_clicked)
        self.player_screen.next_clicked.connect(self.on_next_clicked)
        self.player_screen.seek_requested.connect(self.on_seek_requested)

        # Set as central widget
        self.setCentralWidget(self.player_screen)

        # Load test show data
        self.load_test_show()

    def apply_styling(self):
        """Apply gradient background."""
        set_gradient_background(self)

    def load_test_show(self):
        """Load placeholder show data for testing."""
        test_show = {
            'venue': 'Madison Square Garden',
            'date': '1997-12-31',
            'location': 'New York, NY',
            'source': 'Matrix • SBD',
            'album_art_url': None,
            'tracks': [
                {'title': 'Tweezer', 'duration': '12:34'},
                {'title': 'Split Open and Melt', 'duration': '8:45'},
                {'title': 'Harry Hood', 'duration': '15:22'},
                {'title': 'You Enjoy Myself', 'duration': '21:03'},
                {'title': 'Chalk Dust Torture', 'duration': '7:18'},
                {'title': 'Cavern', 'duration': '4:32'},
                {'title': 'Down with Disease', 'duration': '18:56'},
                {'title': "Mike's Song", 'duration': '9:41'},
                {'title': 'I Am Hydrogen', 'duration': '3:15'},
                {'title': 'Weekapaug Groove', 'duration': '8:22'},
            ]
        }
        self.player_screen.load_show(test_show)

    # Signal handlers for testing
    def on_track_selected(self, track_index: int):
        """Handle track selection."""
        print(f"[TEST] Track selected: {track_index}")
        # Simulate starting playback
        self.player_screen.start_playback()

    def on_play_clicked(self):
        """Handle play button."""
        print("[TEST] Play clicked")
        self.player_screen.start_playback()

    def on_pause_clicked(self):
        """Handle pause button."""
        print("[TEST] Pause clicked")
        self.player_screen.stop_playback()

    def on_previous_clicked(self):
        """Handle previous button."""
        print("[TEST] Previous clicked")
        current = self.player_screen.current_track_index
        if current > 0:
            self.player_screen.set_current_track(current - 1)

    def on_next_clicked(self):
        """Handle next button."""
        print("[TEST] Next clicked")
        current = self.player_screen.current_track_index
        max_tracks = len(self.player_screen.track_list.tracks)
        if current < max_tracks - 1:
            self.player_screen.set_current_track(current + 1)

    def on_seek_requested(self, position: float):
        """Handle seek request."""
        print(f"[TEST] Seek requested: {position:.2%}")


def main():
    """Launch the test window."""
    app = QApplication(sys.argv)
    app.setApplicationName("Deep-Sea Player Screen Test")

    # Apply stylesheets
    apply_stylesheets(app)

    # Create and show test window
    window = TestWindow()
    window.show()

    print("\n" + "="*60)
    print("✓ Player Screen Test")
    print("="*60)
    print("✓ Two-column layout loaded")
    print("  • Left: Show metadata + track list")
    print("  • Right: Now playing card with controls")
    print()
    print("✓ Components:")
    print("  • ShowMetadataWidget (album art, venue, date, location)")
    print("  • TrackListWidget (scrollable track list)")
    print("  • NowPlayingCardWidget (equalizer, controls, progress)")
    print()
    print("✓ Test Data:")
    print("  • Madison Square Garden - 1997-12-31")
    print("  • 10 placeholder tracks")
    print()
    print("Test Interactions:")
    print("  • Click tracks in list to select")
    print("  • Click play/pause to toggle playback")
    print("  • Click previous/next to navigate")
    print("  • Drag progress bar to seek")
    print("  • Watch console for signal output")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
