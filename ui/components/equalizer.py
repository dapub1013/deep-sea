"""
Equalizer Component
Animated segmented frequency visualizer from Grateful Dead app.

This is a signature visual element for Deep-Sea. The implementation uses
the proven FrequencyVisualizer design from the Grateful Dead streaming app
with segmented bars and magenta-to-light-blue gradient.

Features:
- Segmented vertical bars (stacked rectangles with gaps)
- Color gradient: Magenta (bottom) → Light blue/white (top)
- Center-weighted frequency distribution for realistic animation
- 20 FPS smooth animation (50ms timer)
- Two size variants: compact and large
"""

import random
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QSizePolicy


class EqualizerWidget(QWidget):
    """
    Animated segmented frequency visualizer with proven GD app styling.

    Features:
    - Two size variants:
      - "compact": 160x50px with 12 bars, 5 segments (for Now Playing Bar)
      - "large": Expandable width x 120px with 16 bars, 8 segments (for Player Screen)
    - Segmented bars with gaps (stacked rectangles)
    - Magenta-to-light-blue gradient (8 colors)
    - Center-weighted frequency distribution
    - Smooth 20 FPS animation

    Usage:
        # Compact visualizer in Now Playing Bar
        visualizer_compact = EqualizerWidget(size="compact")
        visualizer_compact.start()

        # Large visualizer in Player Screen
        visualizer_large = EqualizerWidget(size="large")
        visualizer_large.start()
    """

    def __init__(self, size="compact", parent=None):
        """
        Initialize frequency visualizer.

        Args:
            size: "compact" (160x50, 12 bars) or "large" (expandable x 120, 16 bars)
            parent: Parent widget
        """
        super().__init__(parent)
        self.size = size
        self._is_playing = False

        # Configure size and bar count based on variant
        if size == "compact":
            self.num_bars = 12
            self.num_segments = 5  # Fewer segments for compact size
            self.setFixedSize(160, 50)
        else:  # large
            self.num_bars = 16
            self.num_segments = 8  # Full 8 segments for large size
            self.setFixedHeight(120)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Initialize bar values (0.0 to 1.0 for each bar)
        self.bar_values = [0.0] * self.num_bars

        # Color gradient from bottom (magenta) to top (light blue/white)
        # From Grateful Dead app FrequencyVisualizer
        if self.num_segments == 8:
            self.row_colors = [
                QColor("#C43C94"),  # Bottom - magenta/pink
                QColor("#A04090"),
                QColor("#8050A0"),
                QColor("#7060A8"),
                QColor("#6878B0"),
                QColor("#7898C0"),
                QColor("#98B8D8"),
                QColor("#C8DCF0"),  # Top - light blue/white
            ]
        else:  # 5 segments for compact
            self.row_colors = [
                QColor("#C43C94"),  # Bottom - magenta
                QColor("#8050A0"),
                QColor("#6878B0"),
                QColor("#98B8D8"),
                QColor("#C8DCF0"),  # Top - light blue
            ]

        # Animation timer (20 FPS = 50ms)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._animate)

    def start(self):
        """Start visualization animation (called when playback starts)."""
        self._is_playing = True
        self.animation_timer.start(50)  # 20 FPS

    def stop(self):
        """Stop visualization and fade out (called when playback stops)."""
        self._is_playing = False
        self.animation_timer.stop()
        # Fade out bars
        self.bar_values = [0.0] * self.num_bars
        self.update()

    def set_playing(self, is_playing):
        """
        Set playing state to control animation.

        Args:
            is_playing: True to start animation, False to stop
        """
        if is_playing and not self._is_playing:
            self.start()
        elif not is_playing and self._is_playing:
            self.stop()

    def _animate(self):
        """
        Animate bars with smooth random values.

        Uses center-weighted frequency distribution for more realistic
        appearance (more activity in mid-range frequencies).
        """
        for i in range(self.num_bars):
            # Create frequency-like distribution (more activity in mid-range)
            center_weight = 1.0 - abs(i - self.num_bars / 2) / (self.num_bars / 2)
            base_activity = 0.3 + center_weight * 0.4
            target = random.random() * base_activity + 0.1

            # Smooth transition (60% old value, 40% new target)
            self.bar_values[i] = self.bar_values[i] * 0.6 + target * 0.4

        self.update()

    def paintEvent(self, event):
        """
        Paint segmented frequency bars with color gradient.

        Each bar is composed of multiple segments (rectangles) with gaps
        between them. Segments are lit from bottom to top based on the
        bar value, creating a frequency analyzer appearance.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        total_width = self.width()
        total_height = self.height()

        # Gap configuration
        if self.size == "compact":
            h_gap = 4  # Horizontal gap between bars
            v_gap = 3  # Vertical gap between segments
        else:  # large
            # 5% margin on each side for large visualizer
            margin_percent = 0.05
            h_margin = int(total_width * margin_percent)
            usable_width = total_width - (2 * h_margin)
            h_gap = 6
            v_gap = 4

        # Calculate segment dimensions
        if self.size == "compact":
            segment_width = (total_width - (self.num_bars - 1) * h_gap) // self.num_bars
        else:
            segment_width = (usable_width - (self.num_bars - 1) * h_gap) // self.num_bars

        segment_height = (total_height - (self.num_segments - 1) * v_gap) // self.num_segments

        painter.setPen(Qt.NoPen)

        # Draw each bar
        for i, value in enumerate(self.bar_values):
            # Calculate x position
            if self.size == "compact":
                x = i * (segment_width + h_gap)
            else:
                x = h_margin + i * (segment_width + h_gap)

            # How many segments to light up (1 to num_segments)
            lit_segments = max(1, int(value * self.num_segments))

            # Draw segments from bottom to top
            for seg in range(lit_segments):
                # Calculate y position (draw from bottom up)
                y = total_height - (seg + 1) * segment_height - seg * v_gap

                # Get color for this segment
                color = self.row_colors[min(seg, len(self.row_colors) - 1)]
                painter.setBrush(color)

                # Draw rounded rectangle (2px corners)
                painter.drawRoundedRect(x, y, segment_width, segment_height, 2, 2)


# Test the equalizer component
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
    from pathlib import Path

    # Add project root to path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    from ui.stylesheet_loader import apply_stylesheets, set_gradient_background

    app = QApplication(sys.argv)
    apply_stylesheets(app)

    window = QMainWindow()
    window.setWindowTitle("Frequency Visualizer Test")
    window.resize(1000, 600)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(40)

    # Title
    title = QLabel("Frequency Visualizer Test")
    title.setObjectName("display")
    layout.addWidget(title, alignment=Qt.AlignCenter)

    # Compact visualizer
    compact_section = QVBoxLayout()
    compact_label = QLabel("Compact Visualizer (160x50)")
    compact_label.setObjectName("h3")
    compact_section.addWidget(compact_label, alignment=Qt.AlignCenter)

    compact_viz = EqualizerWidget(size="compact")
    compact_section.addWidget(compact_viz, alignment=Qt.AlignCenter)
    layout.addLayout(compact_section)

    # Large visualizer
    large_section = QVBoxLayout()
    large_label = QLabel("Large Visualizer (Expandable x 120)")
    large_label.setObjectName("h3")
    large_section.addWidget(large_label, alignment=Qt.AlignCenter)

    large_viz = EqualizerWidget(size="large")
    large_section.addWidget(large_viz)
    layout.addLayout(large_section)

    # Control buttons
    button_layout = QHBoxLayout()

    start_btn = QPushButton("Start Animation")
    start_btn.clicked.connect(compact_viz.start)
    start_btn.clicked.connect(large_viz.start)
    button_layout.addWidget(start_btn)

    stop_btn = QPushButton("Stop Animation")
    stop_btn.clicked.connect(compact_viz.stop)
    stop_btn.clicked.connect(large_viz.stop)
    button_layout.addWidget(stop_btn)

    layout.addLayout(button_layout)

    # Apply gradient background
    set_gradient_background(window)

    window.show()

    print("\n" + "="*60)
    print("✓ Frequency Visualizer Test (Grateful Dead App Design)")
    print("="*60)
    print("✓ Two size variants:")
    print("  • Compact: 160x50px, 12 bars, 5 segments (Now Playing Bar)")
    print("  • Large: Expandable x 120px, 16 bars, 8 segments (Player)")
    print()
    print("✓ Features:")
    print("  • Segmented bars with gaps")
    print("  • Magenta → Light blue gradient (8 colors)")
    print("  • Center-weighted frequency distribution")
    print("  • 20 FPS smooth animation (50ms)")
    print("  • 2px rounded corners")
    print()
    print("✓ Colors (bottom to top):")
    print("  • #C43C94 (Magenta/Pink)")
    print("  • #A04090 → #8050A0 → #7060A8")
    print("  • #6878B0 → #7898C0 → #98B8D8")
    print("  • #C8DCF0 (Light Blue/White)")
    print()
    print("Click 'Start Animation' to see bars animate")
    print("Click 'Stop Animation' to pause")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())
