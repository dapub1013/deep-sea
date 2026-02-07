# ui/components/top_nav.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class TopNav(QWidget):
    """Top navigation bar with Collections and History buttons (Phase 4 design)."""

    collections_clicked = pyqtSignal()
    history_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("topNav")  # Matches QSS: QWidget#topNav
        self.setFixedHeight(72)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Collections button (Heart icon above text)
        collections_btn = self._create_nav_button("♥", "Collections")
        collections_btn.clicked.connect(self.collections_clicked.emit)
        layout.addStretch()
        layout.addWidget(collections_btn)
        layout.addStretch()

        # History button (Clock icon above text)
        history_btn = self._create_nav_button("🕐", "History")
        history_btn.clicked.connect(self.history_clicked.emit)
        layout.addStretch()
        layout.addWidget(history_btn)
        layout.addStretch()

    def _create_nav_button(self, icon: str, label: str) -> QPushButton:
        """Create a navigation button with icon above text (Phase 4 layout)."""
        btn = QPushButton()
        btn.setObjectName("navButton")
        btn.setMinimumSize(72, 56)

        # Create vertical layout for icon + text
        btn_layout = QVBoxLayout(btn)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(4)
        btn_layout.setAlignment(Qt.AlignCenter)

        # Icon label
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        btn_layout.addWidget(icon_label)

        # Text label
        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 12px;")
        btn_layout.addWidget(text_label)

        return btn
