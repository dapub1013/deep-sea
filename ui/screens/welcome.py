# ui/screens/welcome.py
"""
Welcome Screen (Phase 4 design)
Design Reference: docs/04-ui-ux-design/src/app/screens/WelcomeScreen.tsx
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QLinearGradient, QColor, QBrush, QPalette

class WelcomeScreen(QWidget):
    """Welcome screen with logo and 3 action buttons (Phase 4 design)."""

    find_show_clicked = pyqtSignal()
    random_show_clicked = pyqtSignal()
    today_in_history_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("welcomeScreen")
        self.setup_ui()

    def setup_ui(self):
        # Main layout - centered with max width
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 96, 32, 96)  # pt-24 pb-24 → 96px top/bottom
        main_layout.setAlignment(Qt.AlignCenter)

        # Container for centered content (max-width: 448px)
        container = QWidget()
        container.setMaximumWidth(448)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(32)  # space-y-8

        # Logo: Fish emoji in purple gradient box
        logo_container = QWidget()
        logo_container.setFixedSize(128, 128)
        logo_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7c3aed,
                    stop:1 #5b21b6
                );
                border-radius: 24px;
            }
        """)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel("🐟")
        logo_label.setStyleSheet("font-size: 64px; background: transparent;")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)

        # Center the logo
        logo_wrapper = QVBoxLayout()
        logo_wrapper.addWidget(logo_container, 0, Qt.AlignCenter)
        logo_wrapper.addSpacing(48)  # mb-12
        container_layout.addLayout(logo_wrapper)

        # Buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(16)  # gap-4

        # "Find a show" button (primary)
        find_btn = QPushButton("Find a show")
        find_btn.setObjectName("primaryButton")
        find_btn.setMinimumHeight(44)
        find_btn.clicked.connect(self.find_show_clicked.emit)
        buttons_layout.addWidget(find_btn)

        # "Random show" button (secondary)
        random_btn = QPushButton("Random show")
        random_btn.setObjectName("secondaryButton")
        random_btn.setMinimumHeight(44)
        random_btn.clicked.connect(self.random_show_clicked.emit)
        buttons_layout.addWidget(random_btn)

        # "Today in History" button (secondary)
        today_btn = QPushButton("Today in History")
        today_btn.setObjectName("secondaryButton")
        today_btn.setMinimumHeight(44)
        today_btn.clicked.connect(self.today_in_history_clicked.emit)
        buttons_layout.addWidget(today_btn)

        container_layout.addLayout(buttons_layout)

        # Add container to main layout
        main_layout.addWidget(container)
