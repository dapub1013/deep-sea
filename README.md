# Deep-Sea

A modern desktop music player for streaming Phish concerts from phish.in.

## Project Status

**Current Phase:** Phase 6 (Development) - Restarting with Incremental Approach ⧗

**Completed Phases:**
1. ✓ Project Charter
2. ✓ Requirements Definition
3. ✓ API Feasibility & Testing
4. ✓ UI/UX Design & Style Guide
5. ✓ Technical Architecture Decision
6. ⧗ **Development (Iterative)** - IN PROGRESS
   - Previous miniaudio attempt rolled back (see docs/07-audio-engine-decision.md)
   - Repository cleaned up, ready for Task 1 (Feb 4, 2026)
   - Audio engine decision revised to pygame.mixer (see docs/07-audio-engine-decision.md)
   - Currently at: Task 1 (Minimal Application Window)
   - Next: Incremental screen-by-screen development with testing at each step

**Recent Decision (Feb 2026):**
Audio engine changed from miniaudio to **pygame.mixer** for simpler, more reliable implementation. Accepts ~100-300ms gaps between tracks (matches phish.in web player quality) in exchange for dramatically reduced complexity.

## Description

Deep-Sea is a desktop music player for streaming Phish concerts from phish.in. This is a learning/hobby project serving dual purposes:
1. Create a polished, daily-use application for streaming Phish concerts
2. Establish reusable framework and patterns to refactor an existing Grateful Dead concert streaming application

**Target Platforms:**
- Development: macOS laptop
- Production: Raspberry Pi 4 with IQAudio DAC

## Technologies

**Final Tech Stack (Phase 5, revised Feb 2026):**
- **Audio Engine:** pygame.mixer (simple, reliable, "good enough" gapless)
- **UI Framework:** PyQt5 6.x
- **Styling:** QSS (Qt Style Sheets) - CSS-like declarative styling
- **HTTP Client:** requests - phish.in API integration
- **Data Storage:** SQLite - local favorites, collections, history

**Build & Deployment:**
- **macOS:** PyInstaller single-file app bundle
- **Raspberry Pi:** Direct Python execution with systemd service + kiosk mode
- **Development:** Python 3.11+ with virtual environment

## Features

**Must-Have:**
- Stream concerts from phish.in API (v2, no authentication required)
- Browse shows by date, venue, tour, and year
- Core playback features: play/pause, track navigation, volume control
- Smooth playback transitions (~100-300ms gaps, "good enough" gapless)
- "Jump to Highlight" for jamchart-tagged moments

**Should-Have:**
- Favorites and collections management
- Recently played history
- Search functionality across shows, venues, tours

**Nice-to-Have:**
- Animated equalizer visualization
- Audio waveform display
- Show/track notes and ratings

## Documentation

**Planning Phase:**
- `docs/01-project-charter.md` - Complete project charter
- `docs/02-requirements.md` - Requirements definition
- `docs/03-phase3-findings.md` - API feasibility findings
- `docs/04-phase4-design-summary.md` - Design system documentation
- `docs/04-phase4-complete.md` - Phase 4 completion document
- `docs/05-technical-architecture.md` - Technical architecture decision (NOTE: Section 5 outdated, see warning banner)

**Development Phase:**
- `docs/06-phase6-task-plan.md` - Complete task breakdown with acceptance criteria
- `docs/07-audio-engine-decision.md` - pygame.mixer decision rationale
- `docs/06-design-tokens-implementation.md` - QSS design token mapping

**Lessons Learned:**
- `lessons-learned/002-build-test-incrementally.md` - Build and test incrementally (see docs/07-audio-engine-decision.md)
- `lessons-learned/003-redefine-gapless-playback.md` - Redefine "gapless" expectations (see docs/07-audio-engine-decision.md)
- **Full Context:** `docs/07-audio-engine-decision.md` - Complete lessons learned from miniaudio attempt

**Project Context:**
- `CLAUDE.md` - Project guidance for Claude Code (always current)

## UI Prototype

A functional React + TypeScript prototype demonstrating the design system is located in `docs/04-ui-ux-design/`. This serves as a reference implementation for the PyQt5 application.

To run the prototype:

```bash
cd docs/04-ui-ux-design
npm install
npm run dev
```

**Note:** The prototype uses React for design implementation. The final application will use PyQt5 with design tokens and component specifications translated to QSS.

## Development Setup

**Prerequisites:**
- Python 3.11+
- Virtual environment recommended

**Quick Start:**

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Current status: No runnable application yet
# Task 1 (Minimal Application Window) is next
```

**API Note:** phish.in API v2 requires **no authentication**. All endpoints are publicly accessible.

## Current Development Task

**Task 1: Minimal Application Window**

Create the absolute minimum PyQt5 application:
- QMainWindow with fixed size 1280x720
- Single QLabel with "Deep-Sea v1.0" text
- White text, centered
- No gradient, no navigation, no other widgets

See `docs/06-phase6-task-plan.md` for complete task breakdown and acceptance criteria.

## Development Principles

1. **Build Incrementally:** Never write more than 100 lines without running the app
2. **Test Before Commit:** App must run without errors before marking task complete
3. **One Task at a Time:** Never combine tasks or add "bonus features"
4. **Design Before Code:** UI/UX fully designed before writing application code
5. **Quality Over Speed:** No timeline pressure; focus on learning and building something excellent

## Project Governance

- **Developer Authority:** Developer (human) has final say on all decisions
- **PM Role:** Claude serves as advisor, mentor, and structured pushback when needed
- **Phase Gates:** No phase begins until previous phase is complete and approved
- **Documentation:** All decisions, patterns, and lessons learned documented for reusability

## License

To be determined upon open-source release.
