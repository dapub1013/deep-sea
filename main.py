# main.py - Task 3: Load QSS Stylesheets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QPainter
from ui.stylesheet_loader import load_stylesheets

class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep-Sea")
        self.setFixedSize(1280, 720)

        label = QLabel("Deep-Sea v1.0", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 32px;")
        self.setCentralWidget(label)

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
