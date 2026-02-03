"""
Deep-Sea Main Window
Base QMainWindow for the application with Phase 4 gradient background.
Implements screen navigation and core application structure.
"""

import sys
from pathlib import Path
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget,
    QApplication
)

# Add project root to path for imports
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from ui.stylesheet_loader import apply_stylesheets, set_gradient_background


class MainWindow(QMainWindow):
    """
    Deep-Sea main application window.

    Features:
    - Phase 4 purple gradient background
    - Screen navigation via QStackedWidget
    - Top navigation bar (future)
    - Bottom navigation tabs (future)
    - Now Playing Bar (future)
    """

    # Signals
    navigate_to_screen = pyqtSignal(str)  # Emit screen name to navigate

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        self.apply_styling()

    def setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle("Deep-Sea - Phish Concert Streaming")

        # Set window size to target resolution (1280x720 for Raspberry Pi 7" screen)
        self.resize(1280, 720)

        # Set minimum size to prevent too-small windows
        self.setMinimumSize(800, 600)

    def setup_ui(self):
        """Set up the main UI structure."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Screen container (QStackedWidget for screen navigation)
        self.screen_stack = QStackedWidget()
        main_layout.addWidget(self.screen_stack)

        # TODO: Add top navigation bar
        # TODO: Add bottom navigation tabs
        # TODO: Add now playing bar (hideable)

        # For now, add a placeholder welcome screen
        self._add_placeholder_welcome_screen()

    def _add_placeholder_welcome_screen(self):
        """Add a temporary welcome screen for testing."""
        from PyQt5.QtWidgets import QLabel

        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Deep-Sea")
        title.setObjectName("display")
        welcome_layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel("Phish Concert Streaming Player")
        subtitle.setObjectName("h3")
        welcome_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        version = QLabel("Phase 6 Development")
        version.setObjectName("caption")
        welcome_layout.addWidget(version, alignment=Qt.AlignCenter)

        self.screen_stack.addWidget(welcome_widget)

    def apply_styling(self):
        """Apply Phase 4 design system styling."""
        # Apply gradient background to main window
        set_gradient_background(self)

    def navigate_to(self, screen_name: str):
        """
        Navigate to a specific screen.

        Args:
            screen_name: Name of screen to navigate to
                        (e.g., "welcome", "player", "browse", etc.)
        """
        # TODO: Implement screen navigation
        # For now, this is a placeholder
        print(f"Navigate to screen: {screen_name}")

    def add_screen(self, screen_widget: QWidget, screen_name: str):
        """
        Add a screen to the navigation stack.

        Args:
            screen_widget: QWidget instance for the screen
            screen_name: Identifier for the screen
        """
        self.screen_stack.addWidget(screen_widget)
        # TODO: Store screen_name -> widget index mapping

    def show_now_playing_bar(self):
        """Show the persistent now playing bar."""
        # TODO: Implement now playing bar
        pass

    def hide_now_playing_bar(self):
        """Hide the now playing bar."""
        # TODO: Implement now playing bar
        pass


def main():
    """
    Run the Deep-Sea application.
    For development testing of the main window.
    """
    app = QApplication(sys.argv)

    # Load and apply stylesheets
    apply_stylesheets(app)

    # Create and show main window
    window = MainWindow()
    window.show()

    print("\n" + "="*60)
    print("✓ Deep-Sea Main Window")
    print("="*60)
    print("✓ Phase 4 gradient background applied")
    print("  • Top: #1a0b2e (Deep Purple Start)")
    print("  • Mid: #2d1b4e (Deep Purple Mid)")
    print("  • Bottom: #4c1d95 (Deep Purple End)")
    print()
    print("✓ QSS Stylesheets loaded")
    print("  • main.qss (global styles)")
    print("  • components.qss (custom components)")
    print("  • screens.qss (screen layouts)")
    print()
    print("✓ Window Configuration:")
    print("  • Target Resolution: 1280x720 (Raspberry Pi 7\" screen)")
    print("  • Minimum Size: 800x600")
    print()
    print("Next Steps:")
    print("  1. Implement Equalizer component")
    print("  2. Build Player Screen")
    print("  3. Integrate audio engine")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
