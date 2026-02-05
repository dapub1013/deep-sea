# ui/components/bottom_nav.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class BottomNav(QWidget):
    tab_changed = pyqtSignal(str)  # Emits tab name

    def __init__(self):
        super().__init__()
        self.setObjectName("bottomNav")  # Matches QSS: QWidget#bottomNav
        self.setFixedHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        tabs = ["Home", "Browse", "Collections", "History"]
        for tab in tabs:
            btn = QPushButton(tab)
            # No objectName needed - inherits from QWidget#bottomNav QPushButton
            btn.clicked.connect(lambda checked, t=tab: self.tab_changed.emit(t))
            layout.addWidget(btn)
