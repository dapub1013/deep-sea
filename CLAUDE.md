# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deep-Sea is a desktop music player for streaming Phish concerts from phish.in. This is a learning/hobby project with complete planning phase (Phases 1-5: Charter, Requirements, API Testing, UI/UX Design, and Technical Architecture). The project serves dual purposes:
1. Create a polished, daily-use application for streaming Phish concerts
2. Establish reusable framework and patterns to refactor an existing Grateful Dead concert streaming application

## Development Context

**Developer Profile:**
- Strong HTML/CSS skills with an eye for design
- Comfortable with code but relies on Claude Code for Python/JavaScript
- Solo developer working with Visual Studio Code
- Previous project: Similar Grateful Dead streaming app (Python + PyQt5)

**Target Platforms:**
- Development: macOS laptop
- Production: Raspberry Pi 4 with IQAudio DAC

**Tech Stack:**
- Audio Engine: **miniaudio** (pyminiaudio Python wrapper)
- UI Framework: **PyQt5 6.x** (decided in Phase 5)
- Styling: **QSS** (Qt Style Sheets) - CSS-like declarative styling
- HTTP Client: **requests** - phish.in API integration
- Data Storage: **SQLite** - local favorites, collections, history

## Project Phases & Current Status

**Current Phase:** Phase 5 (Technical Architecture Decision) - Complete

**Phases Overview:**
1. ✓ Project Charter
2. ✓ Requirements Definition
3. ✓ API Feasibility & Testing
4. ✓ UI/UX Design & Style Guide
5. ✓ Technical Architecture Decision
6. Development (Iterative)
7. Audio/Hardware Integration & Testing
8. Packaging & Deployment

**Critical Gate:** Phase 5 (Technical Architecture Decision) is now complete. Ready to begin Phase 6 (Development) upon developer approval.

## Core Development Principles

1. **Design Before Code:** UI/UX must be fully designed and approved before writing application code
2. **Quality Over Speed:** No timeline pressure; focus on learning and building something excellent
3. **Document for Reusability:** Capture patterns and decisions for future Grateful Dead app refactor
4. **Phase Completion:** Get informal agreement that a phase is "done" before proceeding
5. **Developer Authority:** Developer has final say on all decisions; Claude serves as advisor

## Phish.in API

The application will integrate with phish.in's API (read-only access).

**API Documentation:** https://phish.in/api-docs

**MCP Server:** Available at `https://phish.in/mcp` for AI assistant integration

**Key Tools:**
- search, list_shows, list_songs, list_venues, list_tours, list_years
- get_song, get_venue, get_tour, get_playlist
- stats (gaps/bustouts, transitions, predictions, geographic patterns, etc.)

## Phase 3 Key Findings

**Audio Format & Streaming:**
- phish.in serves MP3 only via direct URLs (Cloudflare CDN)
- Gapless playback validated using miniaudio (replaces VLC which introduced gaps)
- Real-time audio access available via PCM frame callbacks (enables future visualizer)

**API Data Availability:**
- Tours are first-class entities (promoted to Must-Have feature)
- Jamcharts tag covers 5,008 tracks (community-curated highlights)
- Per-track `jam_starts_at_second` field enables "jump to highlight" feature
- Pre-rendered waveform images available for every track
- No authentication required for any endpoints

**Notable Features Addressed in Phase 4:**
- `jam_starts_at_second` timestamps for highlight moments (implemented as "Jump to Highlight" button)
- Waveform images for visual content (supported in design system)
- Community playlists (potential import feature for future consideration)

## Phase 4 Key Deliverables

**Design System:**
- Purple-based color palette (#1a0b2e → #4c1d95 gradient background)
- iOS-inspired typography scale and design language
- 8pt spacing grid (4px → 64px) with 44px minimum touch targets
- Functional React + TypeScript prototype with 6 screens and 13+ custom components

**Signature Elements:**
- Animated Equalizer component (5-bar purple gradient, compact + large sizes)
- Two-column Player Screen (metadata + track list | now playing + controls)
- Persistent Now Playing Bar (compact, hideable)
- TouchDatePicker for date-based show lookup

**Technology Stack:**
- React 18.3.1 + TypeScript + Vite 6.3.5
- Tailwind CSS 4.1.12 + shadcn/ui component library
- Zustand state management + Motion animation library
- All Must-Have and Should-Have features addressed in design

**Figma Source:** https://www.figma.com/make/SzayRR0qTKkMH1FFxC4HGr/Phish-Concert-Streaming-App

**Important Note:** The Phase 4 prototype uses React + TypeScript as the design implementation framework. This serves as a reference implementation demonstrating design patterns, component behavior, and interactions. The design tokens and component specifications will be replicated in PyQt5/QSS to maintain design fidelity.

## Phase 5 Key Deliverables

**Architecture Decisions:**
- **UI Framework:** PyQt5 6.x with QSS styling (native desktop feel, proven for music apps)
- **Design Translation:** Phase 4 CSS specifications → PyQt5/QSS implementation
- **State Management:** Qt Signals/Slots (built-in event system, no external dependencies)
- **Audio Integration:** Custom HTTPStreamSource adapter + gapless playback via Python generator

**Core Architecture Layers:**
- **UI Layer:** PyQt5 screens and components implementing Phase 4 design system
- **Audio Engine:** miniaudio with custom HTTP streaming and gapless queue management
- **State Manager:** Python data models with Qt signals for UI updates
- **Data Layer:** API client (requests), cache manager (disk), database (SQLite)

**Build & Deployment:**
- **macOS:** PyInstaller single-file app bundle
- **Raspberry Pi:** Direct Python execution with systemd service + kiosk mode
- **Development:** Python 3.11+ with virtual environment

**Implementation Patterns Defined:**
- Design token mapping (CSS custom properties → QSS/QPalette)
- Component translation (React components → PyQt5 custom widgets)
- Gapless HTTP streaming architecture
- Error handling and logging framework
- Resume on reconnect (state persistence)

## Documentation Structure

- `docs/deep-sea-project-charter.md` - Complete project charter defining vision, scope, phases, and governance
- `docs/02-requirements.md` - Requirements definition with must-have, should-have, and nice-to-have features
- `docs/03-phase3-findings.md` - Phase 3 API feasibility findings and early architecture decisions
- `docs/04-phase4-design-summary.md` - Complete design system documentation with extracted specifications
- `docs/04-phase4-complete.md` - Phase 4 completion document with design decisions and approval
- `docs/04-ui-ux-design/` - Functional React + TypeScript prototype (Figma export - DO NOT MODIFY)
- `docs/05-technical-architecture.md` - Complete technical architecture decision (Phase 5 deliverable)
- `docs/discuss-charter.md` - Initial charter discussion notes

## Key Constraints

- Must work on both macOS and Raspberry Pi 4
- Must integrate with IQAudio DAC
- Read-only access to phish.in (no write operations)
- Solo developer project

## Success Criteria

The project is successful when:
1. Application runs reliably on macOS and Raspberry Pi 4 with IQAudio DAC
2. Audio streams smoothly with proper DAC integration
3. Modern UI reflects design vision and style guide
4. Patterns documented for Grateful Dead app refactor
5. Code is clean, documented, and ready for public GitHub repository
6. Developer is proud of the work and enjoys using the application
