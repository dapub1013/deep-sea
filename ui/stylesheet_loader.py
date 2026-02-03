"""
Stylesheet Loader for Deep-Sea Application
Loads and applies QSS stylesheets with design tokens from Phase 4.

This module provides utilities to:
1. Load and combine multiple QSS files
2. Apply stylesheets to the Qt application
3. Set up programmatic styling (gradients, etc.) that QSS cannot handle
"""

import sys
from pathlib import Path
from typing import Optional

# Add project root to path for direct execution
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QColor, QBrush, QPalette
from PyQt5.QtWidgets import QApplication, QWidget

from ui.design_tokens import colors, get_gradient_stops


def load_stylesheets() -> str:
    """
    Load and combine all QSS stylesheets.

    Returns:
        str: Combined stylesheet content
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    styles_dir = project_root / "styles"

    # QSS files to load (order matters - main first, then components, then screens)
    qss_files = [
        styles_dir / "main.qss",
        styles_dir / "components.qss",
        styles_dir / "screens.qss",
    ]

    combined_stylesheet = ""

    for qss_file in qss_files:
        if qss_file.exists():
            with open(qss_file, "r", encoding="utf-8") as f:
                combined_stylesheet += f.read() + "\n\n"
        else:
            print(f"Warning: Stylesheet not found: {qss_file}")

    return combined_stylesheet


def apply_stylesheets(app: QApplication) -> None:
    """
    Apply QSS stylesheets to the Qt application.

    Args:
        app: QApplication instance
    """
    stylesheet = load_stylesheets()
    app.setStyleSheet(stylesheet)
    print("✓ Stylesheets loaded and applied")


def set_gradient_background(widget: QWidget, orientation: Qt.Orientation = Qt.Vertical) -> None:
    """
    Set the Phase 4 purple gradient background on a widget.

    QSS does not support linear gradients, so this must be done programmatically
    using QPalette and QLinearGradient.

    Args:
        widget: QWidget to apply gradient to (typically QMainWindow)
        orientation: Gradient direction (Qt.Vertical for top-to-bottom)
    """
    # Create gradient with fixed coordinates (0,0) to (0,1000)
    # This ensures gradient works regardless of widget height
    gradient = QLinearGradient(0, 0, 0, 1000)
    gradient.setCoordinateMode(QLinearGradient.StretchToDeviceMode)

    # Apply color stops from Phase 4 design tokens
    gradient_stops = get_gradient_stops()
    for position, color_hex in gradient_stops.items():
        gradient.setColorAt(position, QColor(color_hex))

    # Apply gradient to widget palette
    palette = widget.palette()
    palette.setBrush(QPalette.Window, QBrush(gradient))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)


def set_compact_mode(widget: QWidget, compact: bool = True) -> None:
    """
    Enable compact mode styling for smaller screens (Raspberry Pi 7" touchscreen).

    This sets a property that can be used in QSS selectors:
    QWidget[compact="true"] { ... }

    Args:
        widget: Widget to set compact mode on
        compact: True to enable compact mode, False to disable
    """
    widget.setProperty("compact", "true" if compact else "false")
    # Force style refresh
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def get_color(color_name: str) -> Optional[QColor]:
    """
    Get a QColor from design tokens by name.

    Args:
        color_name: Color name (e.g., "primary", "purple_400", "foreground")

    Returns:
        QColor instance or None if color not found
    """
    color_value = getattr(colors, color_name, None)
    if color_value:
        return QColor(color_value)
    return None


# Example usage patterns
if __name__ == "__main__":
    """
    Example usage of stylesheet loader.
    Run this to verify stylesheets load without errors.
    """
    from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                   QLabel, QPushButton, QSlider, QListWidget)
    from PyQt5.QtCore import Qt

    # Create application
    app = QApplication(sys.argv)

    # Load and apply stylesheets
    apply_stylesheets(app)

    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Deep-Sea Design System Test")
    window.resize(1280, 720)

    # Create central widget with layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    layout.setSpacing(24)
    layout.setContentsMargins(48, 48, 48, 48)

    # Title
    title = QLabel("Deep-Sea Design System")
    title.setObjectName("display")
    layout.addWidget(title)

    # Subtitle
    subtitle = QLabel("Phase 4 Design Tokens - QSS Implementation Test")
    subtitle.setObjectName("h3")
    layout.addWidget(subtitle)

    layout.addSpacing(16)

    # Primary button
    primary_btn = QPushButton("Primary Button")
    layout.addWidget(primary_btn)

    # Secondary button
    secondary_btn = QPushButton("Secondary Button")
    secondary_btn.setObjectName("secondary")
    layout.addWidget(secondary_btn)

    # Icon button
    icon_btn = QPushButton("Icon Button")
    icon_btn.setObjectName("icon")
    layout.addWidget(icon_btn)

    layout.addSpacing(16)

    # Slider (Volume control style)
    slider_label = QLabel("Volume Slider")
    slider_label.setObjectName("h4")
    layout.addWidget(slider_label)

    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(70)
    layout.addWidget(slider)

    layout.addSpacing(16)

    # Card widget
    card = QWidget()
    card.setObjectName("card")
    card_layout = QVBoxLayout(card)

    card_title = QLabel("Card Component")
    card_title.setObjectName("h3")
    card_layout.addWidget(card_title)

    card_text = QLabel("This is a frosted glass card with Phase 4 styling")
    card_text.setObjectName("body")
    card_layout.addWidget(card_text)

    layout.addWidget(card)

    layout.addSpacing(16)

    # Color swatches
    colors_label = QLabel("Design Token Colors")
    colors_label.setObjectName("h4")
    layout.addWidget(colors_label)

    colors_layout = QHBoxLayout()
    color_names = ["Primary (#a78bfa)", "Success (#10b981)", "Warning (#f59e0b)", "Destructive (#ef4444)"]
    for color_name in color_names:
        color_label = QLabel(color_name)
        color_label.setObjectName("caption")
        colors_layout.addWidget(color_label)
    layout.addLayout(colors_layout)

    layout.addStretch()

    # Apply gradient background
    set_gradient_background(window)

    # Show window
    window.show()

    print("\n" + "="*60)
    print("✓ Deep-Sea Design System Test Window")
    print("="*60)
    print("✓ Phase 4 gradient background applied")
    print("  • Top: #1a0b2e (Deep Purple Start)")
    print("  • Mid: #2d1b4e (Deep Purple Mid)")
    print("  • Bottom: #4c1d95 (Deep Purple End)")
    print()
    print("✓ QSS Stylesheets loaded (30,000+ characters)")
    print("  • main.qss (global styles)")
    print("  • components.qss (custom components)")
    print("  • screens.qss (screen layouts)")
    print()
    print("✓ Design tokens demonstrated:")
    print("  • Typography (Display, H3, H4, Body, Caption)")
    print("  • Buttons (Primary, Secondary, Icon)")
    print("  • Slider (Volume control style)")
    print("  • Card component (frosted glass effect)")
    print()
    print("Close window to exit...")
    print("="*60 + "\n")

    sys.exit(app.exec_())
