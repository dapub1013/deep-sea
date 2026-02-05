# ui/screens/welcome.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class WelcomeScreen(QWidget):
    play_random_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Welcome to Deep-Sea")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Stream Phish concerts from phish.in")
        subtitle.setObjectName("caption")
        subtitle.setAlignment(Qt.AlignCenter)

        play_btn = QPushButton("Play Random Show")
        # No objectName needed - default QPushButton style is primary
        play_btn.clicked.connect(self.play_random_clicked.emit)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(32)
        layout.addWidget(play_btn)
        layout.addStretch()
