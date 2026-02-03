#!/usr/bin/env python3
"""
Deep-Sea Application Entry Point

Phish Concert Streaming Player
macOS + Raspberry Pi 4 with IQAudio DAC
"""

import sys
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.stylesheet_loader import apply_stylesheets


def main():
    """
    Launch the Deep-Sea application.
    """
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Deep-Sea")
    app.setOrganizationName("Deep-Sea")

    # Load and apply Phase 4 design system stylesheets
    apply_stylesheets(app)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
