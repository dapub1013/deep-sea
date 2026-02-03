# Player Screen Implementation

**Date:** February 3, 2026
**Phase:** Phase 6 Development - Subtask 3
**Reference:** docs/05-technical-architecture.md, line 1943, Section 11, Task 5.3

---

## Overview

Implemented the **Player Screen** as specified in the Phase 5 Technical Architecture document. The Player Screen is the main playback interface with a two-column layout that composes multiple components to create a cohesive music playback experience.

---

## Architecture

### Two-Column Layout

```
┌─────────────────────────────────────────────────────────┐
│                    Player Screen                        │
├───────────────────────────┬─────────────────────────────┤
│  Left Column (50%)        │  Right Column (50%)         │
│                           │                             │
│  ┌─────────────────────┐  │  ┌───────────────────────┐ │
│  │  Show Metadata      │  │  │                       │ │
│  │  • Album Art        │  │  │   Now Playing Card    │ │
│  │  • Venue            │  │  │   • Equalizer         │ │
│  │  • Date/Location    │  │  │   • Track Info        │ │
│  │  • Source           │  │  │   • Progress Bar      │ │
│  └─────────────────────┘  │  │   • Controls          │ │
│                           │  │                       │ │
│  ┌─────────────────────┐  │  │                       │ │
│  │                     │  │  │                       │ │
│  │   Track List        │  │  │                       │ │
│  │   (Scrollable)      │  │  │                       │ │
│  │                     │  │  │                       │ │
│  │                     │  │  └───────────────────────┘ │
│  └─────────────────────┘  │                             │
└───────────────────────────┴─────────────────────────────┘
```

---

## Components Created

### 1. ShowMetadataWidget (`ui/components/show_metadata.py`)

Displays show information in the left column.

**Features:**
- Album art (120x120px with placeholder support)
- Venue name (H2 typography)
- Show date (H3 typography, purple accent)
- Location (caption style)
- Source information (caption style, optional)
- Favorite button (44px touch target, heart icon)

**Styling:**
- Card background with border (`colors.card`, `colors.border`)
- Rounded corners (`border_radius.radius_lg`)
- Proper spacing using design tokens
- Hover states on favorite button

**Methods:**
- `set_show_data(show_data: dict)` - Update with show information
- `load_placeholder_data()` - Load test data

---

### 2. TrackListWidget (`ui/components/track_list.py`)

Scrollable list of tracks in the current show.

**Features:**
- Custom track list items with:
  - Track number (dimmed text)
  - Track title (foreground color)
  - Duration (caption style)
- Scrollable container for long track lists
- Visual selection state
- Hover effects

**Styling:**
- Card-style items with rounded corners
- Border highlights on hover/selection
- Proper spacing between items
- Semi-transparent backgrounds

**Signals:**
- `track_selected(int)` - Emitted when user selects a track

**Methods:**
- `set_tracks(tracks: list)` - Update track list
- `set_current_track(track_index: int)` - Highlight playing track

---

### 3. NowPlayingCardWidget (`ui/components/now_playing_card.py`)

Composite widget for the now playing interface in the right column.

**Sub-components:**

#### PlayerControlsWidget
- Previous/play-pause/next buttons
- 44px minimum touch targets
- Large play button (60x60px)
- Visual states (playing/paused)

**Signals:**
- `play_clicked()`, `pause_clicked()`
- `previous_clicked()`, `next_clicked()`

#### ProgressBarWidget
- Current time / total duration labels
- Horizontal slider for seeking
- Custom styling with purple accent
- Formatted time display (MM:SS)

**Signals:**
- `seek_requested(float)` - Position 0.0-1.0

#### NowPlayingCardWidget (Main)
Composes the above components with:
- Large equalizer (120x120px)
- Track title (H1 typography)
- Track subtitle (set/track info)
- Progress bar
- Player controls

**Features:**
- Animated equalizer (starts/stops with playback)
- Card background with border and rounded corners
- Proper spacing and padding
- All signals forwarded from sub-components

**Signals:**
- `play_clicked()`, `pause_clicked()`
- `previous_clicked()`, `next_clicked()`
- `seek_requested(float)`

**Methods:**
- `set_track_data(track_data: dict)` - Update track info
- `start_playback()` - Start equalizer animation
- `stop_playback()` - Stop equalizer animation
- `update_position(position_seconds: int)` - Update progress

---

### 4. PlayerScreen (`ui/screens/player.py`)

Main screen that composes all components.

**Layout:**
- Two-column horizontal layout (50/50 split)
- Left: ShowMetadataWidget + TrackListWidget (vertical)
- Right: NowPlayingCardWidget + stretch
- Proper margins and spacing using design tokens

**Features:**
- Complete signal forwarding to parent (for audio engine integration)
- Track selection handling
- Automatic UI updates when tracks change
- Placeholder data support for testing

**Signals:**
- `track_selected(int)` - User selected track from list
- `play_clicked()`, `pause_clicked()` - Playback control
- `previous_clicked()`, `next_clicked()` - Track navigation
- `seek_requested(float)` - User scrubbed progress bar

**Methods:**
- `load_show(show_data: dict)` - Load complete show data
- `start_playback()` - Update UI to playing state
- `stop_playback()` - Update UI to paused state
- `update_position(position_seconds: int)` - Update progress
- `set_current_track(track_index: int)` - Set playing track

---

## Design Token Implementation

All components strictly follow the Phase 4 design system:

**Colors:**
- Purple gradient backgrounds
- Card styling with semi-transparency
- Border colors with proper opacity
- Foreground text colors

**Typography:**
- H1 (32px) - Track titles in now playing card
- H2 (24px) - Venue names
- H3 (20px) - Dates, section headers
- Body (16px) - Track titles in list
- Caption (14px) - Secondary information, durations

**Spacing:**
- 8pt spacing grid (spacing_2 to spacing_6)
- Touch targets minimum 44px
- Proper margins and padding throughout

**Border Radius:**
- radius_lg (12px) - Cards, buttons, album art
- radius_md (10px) - Track list items

---

## Testing

**Test Script:** `test_player_screen.py`

The test script creates a standalone window with the Player Screen and placeholder data.

**Test Data:**
- Madison Square Garden, 1997-12-31
- 10 placeholder tracks
- Test signal handlers for all interactions

**Usage:**
```bash
python3 test_player_screen.py
```

**Test Interactions:**
- Click tracks in list → Track selection signal
- Click play/pause → Playback toggle + equalizer animation
- Click previous/next → Track navigation
- Drag progress bar → Seek signal
- Console output shows all signal emissions

---

## Integration Points

The Player Screen is designed for clean integration with the audio engine:

**Audio Engine → UI:**
- Call `start_playback()` when playback starts
- Call `stop_playback()` when playback pauses
- Call `update_position(seconds)` periodically during playback
- Call `set_current_track(index)` when track changes

**UI → Audio Engine:**
- Connect to `track_selected` signal for user track selection
- Connect to `play_clicked` / `pause_clicked` for playback control
- Connect to `previous_clicked` / `next_clicked` for navigation
- Connect to `seek_requested` for seeking (if supported)

**Example Integration:**
```python
# In main application
player_screen = PlayerScreen()

# UI → Audio Engine
player_screen.track_selected.connect(audio_engine.jump_to_track)
player_screen.play_clicked.connect(audio_engine.play)
player_screen.pause_clicked.connect(audio_engine.pause)

# Audio Engine → UI
audio_engine.playback_started.connect(player_screen.start_playback)
audio_engine.playback_paused.connect(player_screen.stop_playback)
audio_engine.position_changed.connect(player_screen.update_position)
audio_engine.track_changed.connect(player_screen.set_current_track)
```

---

## Files Created

```
ui/components/
├── show_metadata.py        # Show information display
├── track_list.py           # Scrollable track list
└── now_playing_card.py     # Now playing interface

ui/screens/
└── player.py               # Main player screen (composes components)

test_player_screen.py       # Standalone test script
```

---

## Next Steps

1. **Visual Testing:** Launch `test_player_screen.py` to verify layout and styling
2. **Audio Integration:** Connect Player Screen to audio engine (Phase 6 next task)
3. **Data Integration:** Connect to phish.in API client for real show data
4. **Album Art Loading:** Implement image loading and caching
5. **Additional Screens:** Build Browse, Collections, History screens

---

## Phase 4 Alignment

This implementation follows the Phase 4 design specifications:

- ✅ Two-column Player Screen layout
- ✅ Show metadata display with album art
- ✅ Scrollable track list with selection
- ✅ Now playing card with equalizer
- ✅ Player controls (previous/play-pause/next)
- ✅ Progress bar with time labels
- ✅ All design tokens implemented (colors, typography, spacing)
- ✅ Touch-optimized button sizes (44px minimum)
- ✅ Card styling with borders and rounded corners
- ✅ Hover and selection states

---

## Status

**Phase 6 Development - Subtask 3:** ✅ **Complete**

The Player Screen is fully implemented and ready for testing. All components are functional with placeholder data. Next step is audio engine integration.

---

*Player Screen Implementation | Deep-Sea Project | February 3, 2026*
