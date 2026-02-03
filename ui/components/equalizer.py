"""
Equalizer Component
Animated 5-bar equalizer matching Phase 4 design system.

This is a signature visual element for Deep-Sea. The implementation follows
the pattern from the technical architecture (Section 4.3.1), with visual
styling that may be refined based on the Grateful Dead app animation.
"""

import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush
from PyQt5.QtWidgets import QWidget


class EqualizerWidget(QWidget):
    """
    Animated 5-bar equalizer matching Phase 4 design.

    Features:
    - Two size variants: "compact" (40px) and "large" (120px)
    - Purple gradient (dark to light)
    - Smooth random animation when playing
    - Static minimal bars when stopped

    Usage:
        # Compact equalizer in Now Playing Bar
        equalizer_compact = EqualizerWidget(size="compact")
        equalizer_compact.start()  # Start animation when playing

        # Large equalizer in Player Screen
        equalizer_large = EqualizerWidget(size="large")
        equalizer_large.start()
    """

    def __init__(self, size="compact", parent=None):
        """
        Initialize equalizer widget.

        Args:
            size: "compact" (40px) or "large" (120px)
            parent: Parent widget
        """
        super().__init__(parent)
        self.size = size
        self.bar_heights = [0.3, 0.6, 0.8, 0.5, 0.4]  # Normalized heights (0.0-1.0)
        self.is_playing = False

        # Set fixed size based on variant
        if size == "compact":
            self.setFixedSize(40, 40)
        else:  # large
            self.setFixedSize(120, 120)

        # Animation timer (updates every 100ms for smooth animation)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_bars)

    def start(self):
        """Start animation (called when audio playback starts)."""
        self.is_playing = True
        self.timer.start(100)  # Update every 100ms

    def stop(self):
        """Stop animation (called when audio playback stops)."""
        self.is_playing = False
        self.timer.stop()
        self.update()  # Trigger repaint to show minimal bars

    def animate_bars(self):
        """Animate bar heights randomly (simulates audio levels)."""
        # Generate random heights between 0.2 and 1.0
        self.bar_heights = [random.uniform(0.2, 1.0) for _ in range(5)]
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        """
        Draw 5 animated bars with purple gradient.

        The gradient goes from dark purple (bottom) to light purple (top),
        matching the Phase 4 design system.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        bar_width = width / 7  # 5 bars + 4 gaps (each gap is half a bar width)
        gap = bar_width / 2

        # Define gradient (dark to light purple)
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor("#5b21b6"))  # Purple-800 (dark)
        gradient.setColorAt(0.5, QColor("#7c3aed"))  # Purple-600 (mid)
        gradient.setColorAt(1.0, QColor("#a78bfa"))  # Purple-400 (light)

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        # Draw 5 bars
        for i in range(5):
            x = i * (bar_width + gap)

            # Calculate bar height based on playing state
            if self.is_playing:
                bar_height = height * self.bar_heights[i]
            else:
                # Minimal static bars when stopped
                bar_height = height * 0.1

            y = height - bar_height

            # Rounded rectangle for each bar
            painter.drawRoundedRect(
                int(x), int(y), int(bar_width), int(bar_height),
                4, 4  # Corner radius
            )


# Test the equalizer component
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
    from pathlib import Path

    # Add project root to path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    from ui.stylesheet_loader import apply_stylesheets, set_gradient_background

    app = QApplication(sys.argv)
    apply_stylesheets(app)

    window = QMainWindow()
    window.setWindowTitle("Equalizer Component Test")
    window.resize(800, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(32)

    # Title
    title = QLabel("Equalizer Component Test")
    title.setObjectName("display")
    layout.addWidget(title, alignment=Qt.AlignCenter)

    # Compact equalizer
    compact_section = QVBoxLayout()
    compact_label = QLabel("Compact Equalizer (40px)")
    compact_label.setObjectName("h3")
    compact_section.addWidget(compact_label, alignment=Qt.AlignCenter)

    compact_eq = EqualizerWidget(size="compact")
    compact_section.addWidget(compact_eq, alignment=Qt.AlignCenter)
    layout.addLayout(compact_section)

    # Large equalizer
    large_section = QVBoxLayout()
    large_label = QLabel("Large Equalizer (120px)")
    large_label.setObjectName("h3")
    large_section.addWidget(large_label, alignment=Qt.AlignCenter)

    large_eq = EqualizerWidget(size="large")
    large_section.addWidget(large_eq, alignment=Qt.AlignCenter)
    layout.addLayout(large_section)

    # Control buttons
    button_layout = QHBoxLayout()

    start_btn = QPushButton("Start Animation")
    start_btn.clicked.connect(compact_eq.start)
    start_btn.clicked.connect(large_eq.start)
    button_layout.addWidget(start_btn)

    stop_btn = QPushButton("Stop Animation")
    stop_btn.clicked.connect(compact_eq.stop)
    stop_btn.clicked.connect(large_eq.stop)
    button_layout.addWidget(stop_btn)

    layout.addLayout(button_layout)

    # Apply gradient background
    set_gradient_background(window)

    window.show()

    print("\n" + "="*60)
    print("✓ Equalizer Component Test")
    print("="*60)
    print("✓ Two size variants:")
    print("  • Compact: 40x40px (for Now Playing Bar)")
    print("  • Large: 120x120px (for Player Screen)")
    print()
    print("✓ Features:")
    print("  • Purple gradient (dark to light)")
    print("  • 5 animated bars")
    print("  • 100ms update interval")
    print("  • Random heights (0.2-1.0)")
    print()
    print("Click 'Start Animation' to see bars animate")
    print("Click 'Stop Animation' to pause")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())
