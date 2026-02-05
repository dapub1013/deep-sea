# main.py - Task 2: Add gradient background
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush

class DeepSeaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deep-Sea")
        self.setFixedSize(1280, 720)
        self.setup_gradient_background()

        label = QLabel("Deep-Sea v1.0", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 32px;")
        self.setCentralWidget(label)

    def setup_gradient_background(self):
        """Apply purple gradient background programmatically."""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#1a0b2e"))
        gradient.setColorAt(0.5, QColor("#2d1b4e"))
        gradient.setColorAt(1.0, QColor("#4c1d95"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeepSeaApp()
    window.show()
    sys.exit(app.exec_())
