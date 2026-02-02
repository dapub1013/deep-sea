# Deep-Sea

A modern desktop music player for streaming Phish concerts from phish.in.

## Project Status

**Current Phase:** Phase 5 (Technical Architecture) - Complete ✓

All planning phases are complete. Ready to begin development (Phase 6) upon approval.

**Completed Phases:**
1. ✓ Project Charter
2. ✓ Requirements Definition
3. ✓ API Feasibility & Testing
4. ✓ UI/UX Design & Style Guide
5. ✓ Technical Architecture Decision

## Description

Deep-Sea is a desktop music player for streaming Phish concerts from phish.in. This is a learning/hobby project serving dual purposes:
1. Create a polished, daily-use application for streaming Phish concerts
2. Establish reusable framework and patterns to refactor an existing Grateful Dead concert streaming application

**Target Platforms:**
- Development: macOS laptop
- Production: Raspberry Pi 4 with IQAudio DAC

## Technologies

**Final Tech Stack (Phase 5):**
- **Audio Engine:** miniaudio (pyminiaudio Python wrapper)
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
- Stream concerts from phish.in API
- Browse shows by date, venue, tour, and year
- Core playback features: play/pause, track navigation, volume control
- Gapless playback between tracks
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

- `docs/deep-sea-project-charter.md` - Complete project charter
- `docs/02-requirements.md` - Requirements definition
- `docs/03-phase3-findings.md` - API feasibility findings
- `docs/04-phase4-design-summary.md` - Design system documentation
- `docs/04-phase4-complete.md` - Phase 4 completion document
- `docs/05-technical-architecture.md` - Technical architecture decision (Phase 5)
- `CLAUDE.md` - Project guidance for Claude Code

## UI Prototype

A functional React + TypeScript prototype demonstrating the design system is located in `docs/04-ui-ux-design/`. This serves as a reference implementation for the PyQt5 application.

To run the prototype:

```bash
cd docs/04-ui-ux-design
npm install
npm run dev
```

**Note:** The prototype uses React for design implementation. The final application will use PyQt5 with design tokens and component specifications translated to QSS.
