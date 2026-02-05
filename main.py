# main.py - Task 4: Add Bottom Navigation Bar
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QPainter
from ui.stylesheet_loader import load_stylesheets
from ui.components.bottom_nav import BottomNav

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

        # Add label
        label = QLabel("Deep-Sea v1.0")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 32px;")
        main_layout.addWidget(label)

        # Add bottom navigation
        self.bottom_nav = BottomNav()
        self.bottom_nav.tab_changed.connect(self.on_tab_changed)
        main_layout.addWidget(self.bottom_nav)

        self.setCentralWidget(central)

    def on_tab_changed(self, tab_name):
        """Handle tab change (console output only for now)."""
        print(f"Tab clicked: {tab_name}")

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
