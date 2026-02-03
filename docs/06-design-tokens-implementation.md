# Design Tokens Implementation

**Phase 6 Task 4 Deliverable | February 2, 2026**

---

## Overview

This document describes the implementation of Phase 4 design tokens in PyQt5/QSS for the Deep-Sea application. The design tokens translate the React/Tailwind CSS prototype specifications into Qt-native styling.

---

## Files Created

### 1. Python Design Tokens Module
**Location:** `ui/design_tokens.py`

Provides programmatic access to all Phase 4 design values:
- `Colors` - Complete purple palette, semantic colors, gradients
- `Typography` - Font stack, type scale, weights, letter spacing
- `Spacing` - 8pt grid system, touch targets
- `BorderRadius` - iOS-inspired rounding values
- `Shadows` - Subtle depth shadows

**Usage:**
```python
from ui.design_tokens import colors, typography, spacing

# Access design tokens
primary_color = colors.primary  # #a78bfa
body_size = typography.body_size  # 16
touch_target = spacing.touch_target  # 44
```

### 2. QSS Stylesheets

#### `styles/main.qss` (11,000+ characters)
Global styles including:
- Base widget styles (QWidget, QLabel, etc.)
- Typography styles (display, title, h1-h4, body, caption)
- Button styles (primary, secondary, icon)
- Input fields (QLineEdit, QTextEdit)
- Sliders (horizontal/vertical for volume and progress)
- Scroll areas and scrollbars
- List widgets
- Status bar and tooltips
- Menu bar and menus
- Tab widgets (bottom navigation)
- Checkboxes and radio buttons
- Progress bars

#### `styles/components.qss` (9,000+ characters)
Component-specific styles:
- Card components (base, show, tour)
- Now Playing Bar
- Player Controls
- Progress Bar (with scrubbing)
- Volume Control
- Track List
- Top Navigation
- Bottom Navigation
- Equalizer Widget
- Touch Date Picker
- Album Art / Image components
- Action buttons (Jump to Highlight, Favorite)
- Loading indicators

#### `styles/screens.qss` (10,000+ characters)
Screen-specific layouts:
- Welcome Screen
- Player Screen (two-column layout)
- Browse Screen
- Collections Screen
- History Screen
- Tour Detail Screen
- Dialog overlays
- Error/Success/Warning states
- Responsive adjustments for compact mode

### 3. Stylesheet Loader Utility
**Location:** `ui/stylesheet_loader.py`

Utilities for loading and applying styles:
- `load_stylesheets()` - Combine and load all QSS files
- `apply_stylesheets(app)` - Apply styles to Qt application
- `set_gradient_background(widget)` - Apply Phase 4 gradient programmatically
- `set_compact_mode(widget)` - Enable compact styling for small screens
- `get_color(name)` - Get QColor from design tokens

---

## Design Token Mapping

### Colors

| Phase 4 Token | Value | QSS Usage |
|---------------|-------|-----------|
| `--purple-400` | `#a78bfa` | Primary color, buttons, highlights |
| `--purple-300` | `#c4b5fd` | Hover states |
| `--purple-500` | `#8b5cf6` | Pressed states, emphasis |
| `--purple-600` | `#7c3aed` | Equalizer gradient mid |
| `--purple-800` | `#5b21b6` | Equalizer gradient dark |
| `--deep-purple-start` | `#1a0b2e` | Gradient background top |
| `--deep-purple-mid` | `#2d1b4e` | Gradient background middle |
| `--deep-purple-end` | `#4c1d95` | Gradient background bottom |
| `--foreground` | `#f0f0f0` | Text color |
| Card background | `rgba(139, 92, 246, 0.15)` | Frosted glass cards |
| Border color | `rgba(167, 139, 250, 0.3)` | Borders, inputs |

### Typography

| Phase 4 Token | Size | Weight | QSS Selector |
|---------------|------|--------|--------------|
| Display | 40px | 500 | `QLabel#display` |
| Title | 28px | 500 | `QLabel#title` |
| H1 | 32px | 500 | `QLabel#h1` |
| H2 | 24px | 500 | `QLabel#h2` |
| H3 | 20px | 500 | `QLabel#h3` |
| H4 | 16px | 500 | `QLabel#h4` |
| Body | 16px | 400 | `QLabel#body` or default |
| Caption | 14px | 400 | `QLabel#caption` |

### Spacing

| Phase 4 Token | Value | Usage |
|---------------|-------|-------|
| `--spacing-1` | 4px | Minimal gaps |
| `--spacing-2` | 8px | Small spacing |
| `--spacing-3` | 12px | Button padding |
| `--spacing-4` | 16px | Card padding, margins |
| `--spacing-5` | 24px | Section spacing |
| `--spacing-6` | 32px | Large gaps |
| `--spacing-7` | 48px | Screen padding |
| `--spacing-8` | 64px | Extra large gaps |
| `--touch-target` | 44px | Minimum button size |

### Border Radius

| Phase 4 Token | Value | Usage |
|---------------|-------|-------|
| `--radius-sm` | 8px | Small elements, icon buttons |
| `--radius-md` | 10px | Medium controls |
| `--radius-lg` | 12px | Base radius, cards, buttons |
| `--radius-xl` | 16px | Large containers |

---

## Key Implementation Notes

### 1. Gradient Background
QSS does not support CSS `linear-gradient()`. The Phase 4 gradient background must be applied programmatically:

```python
from ui.stylesheet_loader import set_gradient_background

# In QMainWindow.__init__()
set_gradient_background(self)
```

This applies the three-color gradient: `#1a0b2e → #2d1b4e → #4c1d95`

### 2. Touch Targets
All interactive elements meet the 44px minimum touch target requirement from Phase 4:
- Buttons: `min-height: 44px; min-width: 44px`
- List items: `min-height: 44px`
- Input fields: `min-height: 44px`

### 3. Object Names for Custom Styling
QSS uses `objectName` for component-specific styling:

```python
# Set object name in Python
button.setObjectName("secondary")

# Reference in QSS
QPushButton#secondary {
    background-color: transparent;
    border: 2px solid rgba(167, 139, 250, 0.3);
}
```

### 4. Compact Mode for Raspberry Pi
Enable compact styling for the 7" touchscreen:

```python
from ui.stylesheet_loader import set_compact_mode

# Enable compact mode
set_compact_mode(main_window, compact=True)
```

This applies QSS rules like:
```css
QWidget[compact="true"] {
    padding: 16px;  /* Reduced from 24px */
}
```

### 5. Frosted Glass Effect
Phase 4 uses `backdrop-blur-lg` for cards. QSS doesn't support backdrop blur, so we use:
- Semi-transparent backgrounds: `rgba(139, 92, 246, 0.15)`
- Subtle borders: `rgba(167, 139, 250, 0.3)`
- Optional `QGraphicsBlurEffect` for true blur (performance impact)

---

## Testing

### Verify Design Tokens Load
```bash
source venv/bin/activate
python -c "from ui.design_tokens import colors; print(colors.primary)"
```

### Verify Stylesheets Load
```bash
source venv/bin/activate
python -c "from ui.stylesheet_loader import load_stylesheets; print(len(load_stylesheets()))"
```

### Visual Test (Run Example Window)
```bash
source venv/bin/activate
python ui/stylesheet_loader.py
```

This opens a test window with:
- Phase 4 gradient background applied
- All QSS styles loaded
- 1280x720 resolution (target screen size)

---

## Next Steps (Task 5: Begin Development)

With design tokens extracted and stylesheets implemented:

1. **Implement MainWindow** with gradient background
2. **Create Equalizer component** to validate QSS + custom painting
3. **Build Welcome Screen** as first complete screen
4. **Iterate on remaining screens** following Phase 4 specifications

---

## References

- Phase 4 Design Summary: `docs/04-phase4-design-summary.md`
- Phase 4 Prototype: `docs/04-ui-ux-design/`
- Phase 5 Technical Architecture: `docs/05-technical-architecture.md` (Section 4.1-4.3)

---

*Design Tokens Implementation | Phase 6 Task 4 Complete | February 2, 2026*
