# main.py - Phase 4 Design: TopNav (Collections, History)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QPainter
from ui.stylesheet_loader import load_stylesheets
from ui.components.top_nav import TopNav
from ui.screens.welcome import WelcomeScreen

class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep-Sea")
        self.setFixedSize(1280, 720)

        # Create central widget with layout
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add top navigation (Phase 4: only on Welcome screen)
        self.top_nav = TopNav()
        self.top_nav.collections_clicked.connect(self.on_collections_clicked)
        self.top_nav.history_clicked.connect(self.on_history_clicked)
        main_layout.addWidget(self.top_nav)

        # Add screen container
        self.screen_container = QWidget()
        screen_layout = QVBoxLayout(self.screen_container)
        screen_layout.setContentsMargins(0, 0, 0, 0)
        self.current_screen = WelcomeScreen()
        self.current_screen.play_random_clicked.connect(
            lambda: print("Play Random clicked")
        )
        screen_layout.addWidget(self.current_screen)

        # Add to main layout
        main_layout.addWidget(self.screen_container)

        self.setCentralWidget(central)

    def on_collections_clicked(self):
        """Navigate to Collections screen (console output for now)."""
        print("Collections clicked")

    def on_history_clicked(self):
        """Navigate to History screen (console output for now)."""
        print("History clicked")

    def setup_gradient_background(self):
        """Apply purple gradient background programmatically."""
        # Store gradient for painting
        self.gradient = QLinearGradient(0, 0, 0, self.height())
        self.gradient.setColorAt(0.0, QColor("#1a0b2e"))
        self.gradient.setColorAt(0.5, QColor("#2d1b4e"))
        self.gradient.setColorAt(1.0, QColor("#4c1d95"))

    def paintEvent(self, event):
        """Paint gradient background (overrides QSS)."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QBrush(self.gradient))
        super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet = load_stylesheets()
    app.setStyleSheet(stylesheet)
    window = DeepSeaApp()
    window.setup_gradient_background()  # Apply gradient AFTER stylesheets
    window.show()
    sys.exit(app.exec_())
