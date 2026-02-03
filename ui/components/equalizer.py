"""
Equalizer Component
Animated 5-bar equalizer with proven styling from Grateful Dead app.

This is a signature visual element for Deep-Sea. The implementation uses
the proven blue gradient and rendering approach from the Grateful Dead
streaming application visualizer.

Styling:
- Blue gradient: Bright cyan (#00BFFF) to dodger blue (#1E90FF)
- 8px rounded corners via QPainterPath
- Smooth antialiased rendering
"""

import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget


class EqualizerWidget(QWidget):
    """
    Animated 5-bar equalizer with proven styling from Grateful Dead app.

    Features:
    - Two size variants: "compact" (40px) and "large" (120px)
    - Blue gradient (bright cyan to dodger blue)
    - Smooth random animation when playing
    - Static minimal bars when stopped
    - 8px rounded corners for polished appearance

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
        Draw 5 animated bars with blue gradient.

        Uses the proven rendering approach from the Grateful Dead app:
        - Bright cyan (#00BFFF) to dodger blue (#1E90FF) gradient
        - QPainterPath with 8px rounded corners
        - Smooth antialiasing
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        bar_width = width / 7  # 5 bars + 4 gaps (each gap is half a bar width)
        gap = bar_width / 2

        # Define gradient (bright cyan to dodger blue)
        # From Grateful Dead app visualizer
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0.0, QColor("#00BFFF"))  # Bright cyan/blue
        gradient.setColorAt(1.0, QColor("#1E90FF"))  # Dodger blue

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

            # Create rounded rectangle path (8px radius for polished look)
            path = QPainterPath()
            path.addRoundedRect(x, y, bar_width, bar_height, 8, 8)
            painter.fillPath(path, gradient)


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
    print("✓ Features (from Grateful Dead app):")
    print("  • Blue gradient (bright cyan #00BFFF → dodger blue #1E90FF)")
    print("  • 5 animated bars with 8px rounded corners")
    print("  • 100ms update interval")
    print("  • Random heights (0.2-1.0)")
    print()
    print("Click 'Start Animation' to see bars animate")
    print("Click 'Stop Animation' to pause")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())
