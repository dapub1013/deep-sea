# Deep-Sea — Phase 4 Complete

**Phase 4 Deliverable | February 2, 2026**

---

## 1. Purpose

This document confirms completion of Phase 4 (UI/UX Design & Style Guide). It validates that the design system deliverables meet the requirements defined in Phase 2, documents key design decisions, and provides developer approval to proceed to Phase 5 (Technical Architecture Decision).

Phase 4 was identified in the Project Charter as a **critical gate** — no application coding begins until this phase is complete and approved.

---

## 2. Phase 4 Deliverables

### 2.1 Design System Documentation

**Location:** `docs/04-phase4-design-summary.md`

This document provides:
- Complete inventory of delivered design assets
- Extracted design specifications (color palette, typography, spacing, etc.)
- Mapping of design system to Must-Have features from Phase 2
- Technology stack evaluation and Phase 5 implications

### 2.2 Functional Prototype

**Location:** `docs/04-ui-ux-design/`

A fully functional React + TypeScript prototype demonstrating:
- **6 application screens** (Welcome, Player, Browse, Collections, History, Tour Detail)
- **13+ custom components** (Equalizer, PlayerControls, TrackList, NowPlayingBar, etc.)
- **Complete design token system** (colors, typography, spacing, shadows)
- **Touch-optimized UI** (44px minimum touch targets throughout)
- **Navigation architecture** (bottom nav + screen routing)
- **State management patterns** (Zustand store for player state)
- **Animation system** (Motion library for visual feedback)

**Figma Source:** [Placeholder - URL to be provided by developer]

### 2.3 Runnable Prototype

The prototype can be run locally for review:
```bash
cd docs/04-ui-ux-design
npm install
npm run dev
```

Access at `http://localhost:5173`

---

## 3. Design Decisions

### 3.1 Visual Identity — Purple Theme

**Decision:** Deep-Sea adopts a purple-based color palette with deep gradient backgrounds.

**Rationale:**
- **Visual differentiation** from the existing Grateful Dead app (likely warmer tones)
- **Phish brand association** — purple is a recognizable Phish color
- **Dark theme optimization** — reduces eye strain during extended listening sessions on RPi touchscreen
- **Distinctive identity** — the deep purple gradient creates a unique visual signature for the app

The color palette ranges from near-black (`#1a0b2e`) at the top of the gradient to deep purple (`#4c1d95`) at the bottom, with primary interactive elements in brighter purple (`#a78bfa`).

### 3.2 iOS-Inspired Design Language

**Decision:** The design system draws heavily from iOS design patterns and typography.

**Rationale:**
- **Touch-first optimization** — iOS design guidelines are battle-tested for touch interfaces
- **44px minimum touch targets** — Apple's standard for reliable touch input
- **System font stack** — native feel across macOS and Linux
- **Generous spacing** — prevents mis-taps and creates visual breathing room on small 7" screen
- **Smooth animations** — reinforces app responsiveness and provides visual feedback

This choice aligns with the developer's stated goal of creating a "polished, daily-use application."

### 3.3 Component Library — shadcn/ui

**Decision:** The prototype uses shadcn/ui (Radix UI primitives + Tailwind CSS).

**Rationale:**
- **Touch-friendly by default** — Radix UI components are accessibility-focused and work well with touch
- **Fully customizable** — components are copied into the project, not imported as a dependency
- **Tailwind integration** — seamless styling with utility classes
- **Production-ready** — 40+ components cover all UI patterns needed for Deep-Sea
- **No runtime overhead** — components are just React + CSS, no heavy framework

This decision does **not** lock Phase 5 into a specific architecture. The components demonstrate design patterns that can be reimplemented in PyQt5 if needed, or used directly if a web-based UI (FastAPI + webview) is chosen.

### 3.4 Equalizer as Signature Element

**Decision:** The animated Equalizer component serves as the "heartbeat" of the app, appearing in both compact (40px) and large (120px) forms.

**Rationale:**
- **Visual confirmation** — users immediately know when audio is playing
- **Brand identity** — the 5-bar purple gradient equalizer becomes a recognizable app icon element
- **Future-proof** — the animation is placeholder in v1 but designed to accept real-time audio data in v2 (real-time visualizer upgrade)
- **Performance-conscious** — uses lightweight Motion library for smooth 60fps animation without excessive CPU/GPU load

The Equalizer appears in:
- Now Playing Bar (compact)
- Player Screen (large)
- App icon (potential)

### 3.5 Two-Column Player Screen Layout

**Decision:** The Player Screen uses a two-column layout — left column shows metadata and track list, right column shows now-playing card with controls.

**Rationale:**
- **Information density** — 1280x720 screen has enough horizontal space to show metadata alongside the player
- **No context switching** — user can see the full setlist while viewing playback controls
- **Touch-friendly** — large controls in the right column remain easy to tap without interfering with scrollable track list on the left
- **Scalable to desktop** — layout works equally well on macOS with mouse/trackpad

This layout is specific to the full Player Screen. The Now Playing Bar (compact) uses a single-row horizontal layout for non-player screens.

---

## 4. Feature Coverage Validation

All Must-Have features from Phase 2 are addressed in the design system. See `docs/04-phase4-design-summary.md` Section 7 for detailed mapping.

**Summary:**

✓ Date-Based Show Lookup
✓ Gapless Playback (UI design complete; backend implementation in Phase 6)
✓ Full Player Screen
✓ Persistent Now Playing Bar
✓ Animated Visual Indicator
✓ Track List with Jump-to-Track
✓ Favorites
✓ Random Show Selection
✓ Resume on Reconnect
✓ Filter Unavailable Shows
✓ Touch-Friendly UI
✓ Personal Curation System

**Should-Have features:**

✓ Listening History
✓ Band's Recent Shows
✓ Tour Browsing

**Nice-to-Have features:**

✓ Real-Time Audio Visualizer (architecture path established via Equalizer component)
- Song-Version Search (deferred to v2)
- Bluetooth on RPi (deferred to Phase 7)

No features were descoped or removed.

---

## 5. Recommendations for Phase 5

### 5.1 Critical Architectural Questions

Phase 5 must resolve the following technical architecture questions:

1. **UI Framework Integration:** How does the React prototype integrate with the Python backend and miniaudio audio engine?
   - FastAPI serving a React build + webview wrapper?
   - PyQt5 webview embedding the React app?
   - Tauri-like approach (unlikely given Python audio engine)?

2. **State Management Bridge:** How does the React UI communicate with the Python audio engine?
   - WebSocket connection for real-time state sync?
   - REST API with polling?
   - IPC mechanism?

3. **Asset Handling:** How are album art, waveform images, and API data fetched and cached?
   - React app makes direct API calls to phish.in?
   - Python backend proxies API requests (better for caching, error handling)?

4. **Build & Packaging:** How is the React app bundled and distributed with the Python backend for Raspberry Pi?
   - Static React build included in Python package?
   - Vite dev server for development, static build for production?

### 5.2 Prototype as Reference Implementation

The Phase 4 prototype should be treated as a **reference implementation** for Phase 6 development, not a throwaway mockup. The component structure, state management patterns, and animation timing are production-ready and should be preserved wherever feasible.

If the architecture decision results in a different UI framework (e.g., PyQt5 instead of React), the design tokens, spacing system, and component behavior should be replicated exactly to maintain design fidelity.

### 5.3 Consideration of Web-Based UI

The prototype demonstrates that a web-based UI (React + Tailwind) is a strong candidate for Deep-Sea. Benefits include:

- **Design system portability** — the prototype becomes the implementation with minimal changes
- **Faster development** — no need to translate the design to a different framework
- **Modern tooling** — Vite, TypeScript, Tailwind, and React have excellent developer experience
- **Easier iteration** — UI changes don't require Python recompilation or app restart

The primary challenge is bridging the web UI with the Python audio engine and API layer. This is solvable (FastAPI + WebSocket or REST API), but Phase 5 must validate the approach for both macOS and Raspberry Pi targets.

---

## 6. Known Limitations and Deferred Items

### 6.1 Placeholder Content

The prototype uses:
- **Mock data** for shows, tracks, and metadata (not live API calls)
- **Placeholder images** from Unsplash (not real album art from phish.in)
- **Simulated audio playback** (no actual MP3 streaming or miniaudio integration)

This is expected for Phase 4. The design system is complete; data integration happens in Phase 6.

### 6.2 Responsive Breakpoints

The prototype is optimized for the target 1280x720 touchscreen resolution. Responsive breakpoints for smaller or larger screens are not fully tested. This is acceptable — the primary target is Raspberry Pi 4 with a 7" touchscreen, and the design works well on macOS at similar aspect ratios.

If future versions target mobile phones or tablets, additional breakpoints may be needed.

### 6.3 Real-Time Visualizer

The Equalizer component uses placeholder animation (random bar heights) in Phase 4. Upgrading to real-time audio data (FFT-based visualization) is a Nice-to-Have feature deferred to v2. The architecture path is clear (miniaudio's `frame_process_method` callback), but implementation is not required for v1.

### 6.4 Accessibility (A11y)

The prototype uses Radix UI primitives, which provide baseline accessibility (keyboard navigation, ARIA attributes, focus management). However, comprehensive accessibility testing (screen reader support, high contrast mode, etc.) is not part of Phase 4.

Given the project's solo developer context and target platform (personal RPi touchscreen), full A11y compliance is not a v1 requirement. If the app is made public or distributed widely, A11y should be revisited.

---

## 7. Approval

This document is approved when the developer confirms the design system is complete, accurate, and ready to inform Phase 5 (Technical Architecture Decision).

**Developer Approval:** _____________________________________ &nbsp; **Date:** _______________

**PM Acknowledgment:** Claude (AI) &nbsp; | &nbsp; **Date:** February 2, 2026

---

## 8. Transition to Phase 5

Phase 4 (UI/UX Design & Style Guide) is complete. Phase 5 (Technical Architecture Decision) may now begin.

**Phase 5 Objectives:**
1. Evaluate UI framework integration options (React + FastAPI + webview vs. PyQt5 webview)
2. Design the Python ↔ JavaScript bridge architecture
3. Define state management and communication protocols (WebSocket, REST, IPC)
4. Establish build and packaging strategy for macOS and Raspberry Pi
5. Document the approved architecture for Phase 6 implementation

**Phase 5 Input Documents:**
- `docs/deep-sea-project-charter.md` (project vision and constraints)
- `docs/02-requirements.md` (feature requirements)
- `docs/03-phase3-findings.md` (audio engine decision and API validation)
- `docs/04-phase4-design-summary.md` (design system specifications)
- `docs/04-ui-ux-design/` (functional prototype)

**Phase 5 Output:**
- `docs/05-architecture-decision.md` (approved technical architecture)

---

*Phase 4 Complete v1.0 | Deep-Sea Project | Phase 4 Complete*
