"""
Design Tokens for Deep-Sea Application
Extracted from Phase 4 Design System (docs/04-phase4-design-summary.md)

These tokens map the React/Tailwind CSS design to PyQt5/QSS implementation.
All values are based on the approved Phase 4 prototype design system.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Colors:
    """Color palette - Purple-based dark theme."""

    # Purple Scale
    purple_50 = "#f5f3ff"
    purple_100 = "#ede9fe"
    purple_200 = "#ddd6fe"
    purple_300 = "#c4b5fd"
    purple_400 = "#a78bfa"
    purple_500 = "#8b5cf6"
    purple_600 = "#7c3aed"
    purple_700 = "#6d28d9"
    purple_800 = "#5b21b6"
    purple_900 = "#4c1d95"
    purple_950 = "#2e1065"

    # Deep Purple Gradient (Background)
    deep_purple_start = "#1a0b2e"  # Darkest - top
    deep_purple_mid = "#2d1b4e"    # Middle
    deep_purple_end = "#4c1d95"    # Lightest - bottom

    # Semantic Colors
    foreground = "#f0f0f0"
    primary = purple_400        # #a78bfa
    primary_hover = purple_300  # #c4b5fd
    card = "rgba(139, 92, 246, 0.15)"  # Purple-500 at 15% opacity
    border = "rgba(167, 139, 250, 0.3)"  # Purple-400 at 30% opacity
    input_border = "rgba(167, 139, 250, 0.3)"

    # State Colors
    success = "#10b981"      # Green
    warning = "#f59e0b"      # Amber
    destructive = "#ef4444"  # Red

    # Equalizer Gradient
    equalizer_dark = purple_800   # #5b21b6
    equalizer_mid = purple_600    # #7c3aed
    equalizer_light = purple_400  # #a78bfa


@dataclass
class Typography:
    """Typography scale - iOS-inspired."""

    # Font Stack
    font_family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

    # Type Scale (sizes in pixels)
    display_size = 40
    title_size = 28
    h1_size = 32
    h2_size = 24
    h3_size = 20
    h4_size = 16
    body_size = 16
    caption_size = 14

    # Font Weights
    weight_medium = 500  # Headings, buttons, labels
    weight_normal = 400  # Body text, inputs

    # Letter Spacing (in em)
    display_spacing = "-0.03em"
    title_spacing = "-0.02em"
    h1_spacing = "-0.02em"
    h2_spacing = "-0.01em"


@dataclass
class Spacing:
    """8-point spacing grid."""

    spacing_1 = 4   # 0.25rem
    spacing_2 = 8   # 0.5rem
    spacing_3 = 12  # 0.75rem
    spacing_4 = 16  # 1rem
    spacing_5 = 24  # 1.5rem
    spacing_6 = 32  # 2rem
    spacing_7 = 48  # 3rem
    spacing_8 = 64  # 4rem

    # Touch Targets
    touch_target = 44  # Minimum for all interactive elements


@dataclass
class BorderRadius:
    """iOS-inspired border radius values."""

    radius_sm = 8   # Small elements
    radius_md = 10  # Medium elements
    radius_lg = 12  # Base radius, large cards/panels
    radius_xl = 16  # Extra large containers

    # Alias for base radius
    radius = radius_lg


@dataclass
class Shadows:
    """Subtle depth shadows."""

    shadow_sm = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    shadow_md = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)"
    shadow_lg = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)"
    shadow_xl = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"


# Export singleton instances
colors = Colors()
typography = Typography()
spacing = Spacing()
border_radius = BorderRadius()
shadows = Shadows()


def get_gradient_stops() -> Dict[float, str]:
    """
    Get gradient color stops for background.
    Returns dict of position (0.0-1.0) to color hex.
    """
    return {
        0.0: colors.deep_purple_start,  # #1a0b2e
        0.5: colors.deep_purple_mid,    # #2d1b4e
        1.0: colors.deep_purple_end,    # #4c1d95
    }
