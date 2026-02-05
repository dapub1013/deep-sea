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
- Audio Engine: **pygame.mixer** (simple, reliable, "good enough" gapless)
- UI Framework: **PyQt5 6.x** (decided in Phase 5)
- Styling: **QSS** (Qt Style Sheets) - CSS-like declarative styling
- HTTP Client: **requests** - phish.in API integration
- Data Storage: **SQLite** - local favorites, collections, history

## Project Phases & Current Status

**Current Phase:** Phase 6 (Development) - Restarting with Incremental Approach

**Phases Overview:**
1. ✓ Project Charter
2. ✓ Requirements Definition
3. ✓ API Feasibility & Testing
4. ✓ UI/UX Design & Style Guide
5. ✓ Technical Architecture Decision
6. **Development (Iterative)** - STARTING FRESH
   - Starting at Task 1: Minimal Application Window
   - See docs/06-phase6-task-plan.md for complete task breakdown
7. Audio/Hardware Integration & Testing
8. Packaging & Deployment

**Phase 6 Status:**
- Previous attempt with miniaudio failed (see docs/lessons-learned/004-build-incrementally.md)
- Audio engine decision made: pygame.mixer (see docs/07-audio-engine-decision.md)
- Restarting with strict incremental development (one task at a time)
- Current task: Task 1 (Minimal Application Window)

## Core Development Principles

1. **Build Incrementally:** Never write more than 100 lines without running the app
2. **Test Before Commit:** App must run without errors before marking task complete
3. **One Task at a Time:** Never combine tasks or add "bonus features"
4. **Design Before Code:** UI/UX must be fully designed and approved before writing application code
5. **Quality Over Speed:** No timeline pressure; focus on learning and building something excellent
6. **Document for Reusability:** Capture patterns and decisions for future Grateful Dead app refactor
7. **Developer Authority:** Developer has final say on all decisions; Claude serves as advisor
8. **Design-First Implementation:** Phase 4 design files are the source of truth - always verify against them before implementing

## Design-First Development (CRITICAL)

**Lesson Learned:** In Tasks 1-5, we implemented components based on the task plan without cross-referencing the actual Phase 4 design, resulting in wrong navigation structure and wasted effort. See `docs/lessons-learned/005-design-implementation-mismatch.md` for full details.

### Before Implementing ANY UI Component

**MANDATORY Design Verification Steps:**

1. **Read the Phase 4 Component File:**
   - Location: `docs/04-ui-ux-design/src/app/components/[ComponentName].tsx`
   - Note layout structure (flex-col → QVBoxLayout, flex-row → QHBoxLayout)
   - Note all children/content elements
   - Note icons used (plan Qt equivalents: Unicode, images, or fonts)
   - Note interactions (map to Qt signals)

2. **Check Existing QSS Styles:**
   - Search `styles/*.qss` for the component's objectName
   - Verify objectName casing (camelCase in QSS: `topNav`, `bottomNav`)
   - Check what styles exist vs. what needs to be created

3. **Verify Task Plan vs. Design:**
   - If task plan conflicts with Phase 4 design: **STOP and ask user**
   - Phase 4 design wins unless user explicitly overrides
   - Never assume task plan is more current than design files

4. **Plan Qt Implementation:**
   - What Qt widgets are needed?
   - What layout managers? (QVBoxLayout, QHBoxLayout, QGridLayout)
   - What signals/slots for interactions?
   - What objectNames for QSS styling?

### Design-to-Qt Translation Guide

**React → Qt Widget Mapping:**
- `<div>` → `QWidget`
- `<button>` → `QPushButton`
- `<label>` or `<span>` → `QLabel`
- `<input>` → `QLineEdit`
- `flex-col` (column) → `QVBoxLayout`
- `flex-row` (row) → `QHBoxLayout`

**Common Patterns:**
- Icon above text → QVBoxLayout with QLabel(icon) + QLabel(text)
- Inline icon+text → QHBoxLayout with QLabel(icon) + QLabel(text)
- Stacking elements → QVBoxLayout
- Side-by-side elements → QHBoxLayout

**ObjectName Rules:**
- QSS uses camelCase: `topNav`, `bottomNav`, `nowPlayingBar`
- Set in Qt: `widget.setObjectName("topNav")`
- Match exactly what's in QSS files

### If Phase 4 Design Doesn't Exist for Component

Some components may not have Phase 4 equivalents (new features, etc). In this case:
1. Ask user for design direction first
2. Reference similar components from Phase 4 for style consistency
3. Use existing design tokens and QSS patterns
4. Get user approval on visual appearance before proceeding

## Critical Rules for Claude Code

### The Three Laws of Development

1. **ONE TASK AT A TIME** - Never combine tasks. Never add "bonus features."
2. **RUN BEFORE COMMIT** - App must run without errors before marking task complete.
3. **TEST WHAT YOU BUILD** - Every feature must be manually tested before moving on.

### Red Lines - Automatic Stop Conditions

If you encounter ANY of these, **STOP IMMEDIATELY** and consult with human:

- ❌ More than 2 errors in a row without a successful run
- ❌ Building multiple screens in one task
- ❌ Assuming API data structure without validation
- ❌ Changing architecture decisions without approval
- ❌ Adding features not in the current task scope

### Task Workflow

**Before starting any task:**
1. Read the task completely in docs/06-phase6-task-plan.md
2. Understand the scope and stop conditions
3. Check acceptance criteria
4. **DESIGN VERIFICATION (for UI components):**
   - Read corresponding Phase 4 component file in `docs/04-ui-ux-design/src/`
   - Verify task plan matches Phase 4 design
   - Check QSS files for existing styles
   - If conflict: STOP and ask user

**During the task:**
1. Write code as specified (following Phase 4 design if UI component)
2. Run the app frequently (every 50 lines)
3. Stay within task scope
4. Do NOT add features beyond the task
5. Add design reference comments in code

**After completing the task:**
1. Run the app - must work without errors
2. Test manually - verify acceptance criteria
3. **For UI components:** Verify visual appearance matches Phase 4 design
4. Commit working code
5. Wait for human approval before next task

## Phish.in API

The application will integrate with phish.in's API (read-only access).

**API Documentation:** https://phish.in/api-docs

**API Version:** v2 (https://phish.in/api/v2)
- No authentication required
- Complete catalog including shows without recordings

**Key Endpoints:**
- GET /shows - List shows (filter by year, audio_status)
- GET /shows/{date} - Get specific show details
- GET /tours - List all tours
- GET /tours/{slug} - Get specific tour

**Important Notes:**
- API v1 requires authentication (DO NOT USE)
- API v2 is public and requires no auth (USE THIS)
- See docs/03-phase3-findings.md for detailed API structure validation

## Phase 3 Key Findings

**Audio Format & Streaming:**
- phish.in serves MP3 only via direct URLs (Cloudflare CDN)
- "Gapless" means smooth transitions (~100-300ms gaps acceptable)
- Network streaming inherently has small gaps - this is expected
- See docs/lessons-learned/003-gapless-redefined.md

**API Data Availability:**
- Tours are first-class entities (promoted to Must-Have feature)
- Jamcharts tag covers 5,008 tracks (community-curated highlights)
- Per-track `jam_starts_at_second` field enables "jump to highlight" feature
- Pre-rendered waveform images available for every track
- API v2 requires no authentication

**Data Structure Validation:**
- ALWAYS validate API responses before building UI
- Use scripts/validate_api.py to inspect actual data structures
- Venue field type: dict with 'name', 'city', 'state' keys
- Duration field type: int (seconds)
- Track mp3 URL field: 'mp3' (not 'mp3_url')

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

**Design Reference:**
- All design specs: docs/04-phase4-design-summary.md
- QSS stylesheets: ui/styles/ (main.qss, components.qss, screens.qss)
- Design tokens: ui/design_tokens.py

**Important Note:** 
The Phase 4 prototype uses React + TypeScript as the design implementation framework. This serves as a reference for visual design, component behavior, and interactions. The design tokens and component specifications are replicated in PyQt5/QSS for the actual application.

## Phase 5 Key Decisions

**Architecture:**
- UI Framework: PyQt5 6.x with QSS styling
- Audio Engine: pygame.mixer (decided Feb 2026, see docs/07-audio-engine-decision.md)
- State Management: Qt Signals/Slots (built-in event system)
- Data Layer: PhishInAPI client, local SQLite database, disk cache for images

**Implementation Patterns:**
- Design token mapping (CSS custom properties → QSS/QPalette)
- Component translation (React components → PyQt5 custom widgets)
- Qt signals for UI ↔ audio communication
- Error handling and logging framework

**Build & Deployment:**
- macOS: PyInstaller single-file app bundle
- Raspberry Pi: Direct Python execution with systemd service + kiosk mode

**Note:** Original Phase 5 architecture specified miniaudio. This was revised in Feb 2026 to pygame.mixer after implementation challenges. See docs/07-audio-engine-decision.md for rationale.

## Audio Engine Decision (Feb 2026)

**Choice: pygame.mixer**

**Rationale:**
- Simpler API, well-documented, proven in production
- "Good enough" gapless (~100-300ms gaps between tracks)
- Matches phish.in web player quality (baseline expectation)
- Easy to debug and maintain
- No complex streaming architecture required

**Trade-offs Accepted:**
- Slightly longer gaps than theoretical "perfect" gapless
- Pre-download tracks to cache (not streaming on-demand)
- Simpler implementation over technical perfection

**Implementation:**
- PygamePlayer class in audio/pygame_player.py
- Download MP3 to cache, play from disk
- Qt signals for UI integration
- Auto-advance to next track on completion

See docs/07-audio-engine-decision.md for complete decision rationale.

## Current Development Task

**Task:** Task 1 - Minimal Application Window  
**Goal:** Create the absolute minimum PyQt5 application  
**Files:** main.py (< 50 lines)  
**Scope:** Window + centered label ONLY

**What to build:**
- QMainWindow with fixed size 1280x720
- Single QLabel with "Deep-Sea v1.0" text
- White text, centered
- No gradient, no navigation, no other widgets

**Acceptance Criteria:**
- [ ] Window opens when running `python main.py`
- [ ] Window is 1280x720 pixels
- [ ] White text "Deep-Sea v1.0" appears centered
- [ ] Window closes cleanly without errors

**Stop Conditions:**
- DO NOT add gradient background yet (that's Task 2)
- DO NOT load QSS stylesheets yet (that's Task 3)
- DO NOT add navigation
- DO NOT add any other widgets

**What You CAN Use:**
- Existing design token values from `ui/design_tokens.py` (for hardcoded colors if needed)
- Standard PyQt5 widgets and layouts
- Nothing else

**Next Steps After Task 1:**
- Get human approval
- Proceed to Task 2 (Apply Gradient Background)
- Task 3 will load the existing QSS stylesheets
- See docs/06-phase6-task-plan.md for full task sequence

## Repository Status

**Code Status (as of Feb 4, 2026):** Clean slate - design system implemented, ready for Task 1

**What EXISTS and is TRUSTED:**
- ✅ **Design Tokens:** `ui/design_tokens.py` - Complete Python module with all Phase 4 color, typography, spacing values
- ✅ **QSS Stylesheets:** `styles/main.qss`, `styles/components.qss`, `styles/screens.qss` - Complete QSS implementation of Phase 4 design
- ✅ **Stylesheet Loader:** `ui/stylesheet_loader.py` - Utility for loading and applying QSS
- ✅ **API Client:** `data/api_client.py` - Verified working with phish.in API v2
- ✅ **Equalizer Component:** `ui/components/equalizer.py` - Animated 5-bar equalizer widget (Phase 4 signature element)
- ✅ **Documentation:** All Phase 1-5 planning documents complete and approved

**What does NOT exist (will be built in Phase 6):**
- ❌ **No Application Entry Point:** No `main.py` yet (Task 1 will create)
- ❌ **No Screens:** Empty `ui/screens/` directory (Tasks 5, 8, 9, 14, 16 will create screens)
- ❌ **No Other Components:** Only Equalizer exists in `ui/components/` (other components built as needed)
- ❌ **No Audio Engine:** Empty `audio/` directory (Task 7 will create pygame.mixer player)
- ❌ **No Database/Cache Implementations:** `data/database.py` and `data/cache.py` are empty stubs (Tasks 13, 15 will implement)

**Previous Work Status (Cleanup Complete):**
- All code from the failed miniaudio attempt has been deleted (Feb 4, 2026)
- Design tokens and QSS files were created BEFORE the miniaudio attempt and are audio-engine-agnostic
- These files are reusable for the pygame.mixer implementation without modification
- Deleted files: `audio/engine.py`, `audio/gapless_player.py`, `audio/http_source.py`, `ui/main_window.py`, `ui/screens/player.py`, and all experimental test files

**Starting Point for Task 1:**
- Create `main.py` from scratch (does not exist yet)
- Do NOT load QSS stylesheets yet (that's Task 3)
- Do NOT use design tokens yet (Task 2 uses them for gradient)
- Start with the absolute minimum PyQt5 application

## Lessons Learned

**002: Build and Test Incrementally**
- Never build multiple screens without testing
- Validate data structures before building UI
- Run app every 100 lines of code maximum
- If 3+ errors cascade, STOP and rollback

**003: Redefine Gapless Playback**
- "Gapless" for streaming MP3s means ~100-300ms gaps (acceptable)
- Don't over-engineer for perfection
- Match the baseline (phish.in web player)
- Simple and working beats perfect and broken

See docs/lessons-learned/ directory for complete post-mortems.

## Important Files Reference

**Planning Documents:**
- docs/01-project-charter.md - Project vision and governance
- docs/02-requirements.md - Feature requirements (must/should/nice-to-have)
- docs/03-phase3-findings.md - API validation and early architecture decisions
- docs/04-phase4-design-summary.md - Complete design system documentation
- docs/05-technical-architecture.md - Technical architecture (NOTE: audio engine section outdated)

**Current Development:**
- docs/06-phase6-task-plan.md - **ACTIVE TASK LIST** (read this first)
- docs/07-audio-engine-decision.md - pygame.mixer decision rationale

**Lessons Learned (Complete Post-Mortems):**
- docs/lessons-learned/001-api-version-error.md - API v1/v2 documentation mismatch
- docs/lessons-learned/002-audio-engine-api-integration-bugs.md - 6 critical bugs from untested code
- docs/lessons-learned/003-gapless-redefined.md - Redefining "gapless" expectations
- docs/lessons-learned/004-build-incrementally.md - Build-test-validate loop failure

**Design Reference:**
- docs/04-ui-ux-design/ - React prototype (DO NOT MODIFY - reference only)
- ui/design_tokens.py - Design token values
- ui/styles/ - QSS stylesheets

**Archived/Superseded:**
- docs/06-audio-integration-complete.md - OUTDATED (miniaudio attempt)
- docs/06-design-tokens-implementation.md - Still valid (QSS implementation)

**Design System (Completed):**
- ui/design_tokens.py - Python design token values (colors, typography, spacing)
- styles/main.qss - Global QSS styles (11,000+ characters)
- styles/components.qss - Component-specific QSS (9,000+ characters)
- styles/screens.qss - Screen layout QSS (10,000+ characters)
- ui/stylesheet_loader.py - QSS loading utilities
- docs/06-design-tokens-implementation.md - Design token documentation

## Success Criteria

**Daily Success:**
- At least 3 tasks completed with working code committed
- No cascade of errors (max 2 in a row before rollback)
- Every commit is runnable code
- Human approval received before advancing

**Project Success:**
The project is successful when:
1. Application runs reliably on macOS and Raspberry Pi 4 with IQAudio DAC
2. Audio streams smoothly with acceptable gaps between tracks
3. Modern UI reflects Phase 4 design vision
4. Patterns documented for Grateful Dead app refactor
5. Code is clean, documented, and ready for public GitHub repository
6. Developer is proud of the work and enjoys using the application

## Key Constraints

- Must work on both macOS and Raspberry Pi 4
- Must integrate with IQAudio DAC
- Read-only access to phish.in (no write operations)
- Solo developer project (no team resources)
- 7" touchscreen target (1280x720, touch-optimized UI)
- All interactive elements must meet 44px minimum touch target

## Getting Started (For New Sessions)

1. Read docs/06-phase6-task-plan.md - Find current task
2. Read the current task completely
3. Understand scope and stop conditions
4. Check previous task is committed and working
5. Begin task implementation
6. Test frequently (run app every 50 lines)
7. Commit working code
8. Get approval before next task

**Remember:** Progress = working code, not lines written. One feature working > ten features broken.
