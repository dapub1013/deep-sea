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
    # Create gradient
    gradient = QLinearGradient(0, 0, 0, widget.height())

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
    # Create application
    app = QApplication(sys.argv)

    # Load and apply stylesheets
    apply_stylesheets(app)

    # Create main window and apply gradient
    from PyQt5.QtWidgets import QMainWindow

    window = QMainWindow()
    window.setWindowTitle("Deep-Sea Stylesheet Test")
    window.resize(1280, 720)

    # Apply gradient background
    set_gradient_background(window)

    # Show window
    window.show()

    print("✓ Stylesheet test window displayed")
    print("  - Gradient background applied")
    print("  - QSS styles loaded")
    print("  - Close window to exit")

    sys.exit(app.exec_())
