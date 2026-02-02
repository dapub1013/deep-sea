# Deep-Sea — Requirements Definition

**Phase 2 Deliverable | January 31, 2026**

---

## 1. Purpose

This document defines the functional requirements for Deep-Sea v1. It translates the project vision established in the Project Charter into a concrete, prioritized feature list that will guide UI/UX design (Phase 4), API feasibility testing (Phase 3), and eventual development (Phase 6).

Requirements are organized into three priority tiers: **Must-Have** (v1 is not complete without these), **Should-Have** (v1 is weaker without these, but shippable), and **Nice-to-Have** (candidates for v2 and beyond). These tiers are living categories — Phase 3 API exploration may surface new capabilities that shift priorities or add features.

---

## 2. Platform Context

Deep-Sea runs on two platforms simultaneously, and requirements must account for both. **macOS (development)** is a standard desktop environment with mouse and keyboard input. **Raspberry Pi 4 (production)** pairs with a 7" touchscreen at 1280x720 resolution and an IQAudio DAC for stereo output via RCA.

The touchscreen constraint is the more restrictive of the two — any UI that works well on touch will work well with a mouse, but not vice versa. All interactive elements must be sized and spaced for reliable finger input from the first design iteration.

---

## 3. Feature Requirements

### Must-Have

| Feature | Description | Notes |
|---|---|---|
| Date-Based Show Lookup | Primary method for finding a show. Touch-optimized selector that prevents selection of dates with no available show in the database. | Solves the 3-column year/month/day pain point from the GD app. Design exploration required in Phase 4. |
| Gapless Playback | Audio transitions between tracks within a show play without gaps or silence. | Known pain point from the GD app. Must be addressed from the start — do not defer. |
| Full Player Screen | Dedicated now-playing view displaying show metadata: date, venue, source info, rating, and denoted highlights. Includes media controls and track list. | Primary listening interface. Rich metadata display is a key differentiator. |
| Persistent Now Playing Bar | A compact bar visible while navigating the app. Displays current show info and media controls. Can be hidden by the user. | Ensures the user always knows what is playing. Hideable to maximize screen real estate on the 7" touchscreen. |
| Animated Visual Indicator | A visual animation in both the Player screen and the Now Playing bar that confirms audio is actively playing. Does not need to be driven by real-time audio data in v1. | Acts as a "heartbeat" for the player. Must be designed as a signature UI element — not an afterthought. See linked note on real-time visualizer in Section 4. |
| Track List with Jump-to-Track | A visible list of all tracks in the current show. User can tap any track to jump directly to it. | Essential for navigating within a show, especially on a touchscreen. |
| Favorites | User can save shows they attended in person to a dedicated favorites collection. Quick access to this collection from the main navigation. | Personal and persistent. Local storage only — no account or sync required. |
| Random Show Selection | A "pick something for me" option that selects a random available show for playback. | Reduces decision paralysis. Should feel like a feature, not just a button — design may include a brief reveal or animation. |
| Resume on Reconnect | If the app is closed or the stream drops, playback resumes from the last known position and state when the app is reopened or connectivity is restored. | Critical for the RPi use case where the app may run for extended periods. |
| Filter Unavailable Shows | Only shows with available audio streams are surfaced in browse, search, and date navigation. Unavailable shows are never displayed. | Users should never encounter a dead end. Validation happens at the data layer before any UI is rendered. |
| Touch-Friendly UI | All interactive elements are sized and spaced for reliable touch input on a 7" 1280x720 touchscreen. The app is equally usable via mouse on macOS. | Non-negotiable given the RPi + touchscreen production target. Must be considered from the first design mockup. |
| Personal Curation System | User can create and manage personal collections and playlists. Collections can contain shows or be organized around themes (e.g., tours, attended shows). | Foundation for making the app feel personal. Also the key enabler for tour browsing to become compelling. See linked note in Section 4. |

### Should-Have

| Feature | Description | Notes |
|---|---|---|
| Listening History | The app tracks a history of shows the user has played. Accessible from the main navigation for quick replay. | Local state only. Distinct from "Band's Recent Shows" — this is the user's own history. |
| Band's Recent Shows | A list of the most recent concerts Phish has actually performed, sourced from the API. Count is determined by what the UI can display gracefully. | Useful for fans who want to catch up on recent performances. Count is flexible — UI-driven, not hard-coded. |
| Tour Browsing | User can browse shows within a specific tour. Becomes significantly more compelling when paired with the personal curation system. | Priority is linked to curation feasibility. Nice-to-have if relying on API data alone; should-have if personal curation works well; potential must-have if the combination becomes a standout feature. Evaluate together in Phase 3 and 4. |

### Nice-to-Have

| Feature | Description | Notes |
|---|---|---|
| Real-Time Audio Visualizer | A true visualizer driven by real-time audio stream data (e.g., FFT frequency spectrum). Replaces or enhances the animated visual indicator. | Requires deep access to the audio pipeline. Feasibility depends on the chosen tech stack and playback engine. Evaluate in Phase 3. |
| Song-Version Search | User can search for a specific song and be presented with a curated list of well-regarded versions from historically notable performances. | Data source TBD. May require human curation if the API does not surface this directly. Deferred to v2. |
| Bluetooth on RPi | RPi can output audio via Bluetooth to wireless speakers or headphones in addition to the IQAudio DAC. | Hardware capability exists on RPi 4. Implementation complexity and priority TBD. |

---

## 4. Feature Dependencies

Several features are not independent — their priority and feasibility are linked to other features. These relationships must be evaluated together during Phase 3 (API Feasibility) and Phase 4 (UI/UX Design).

| Feature | Dependency & Rationale |
|---|---|
| Tour Browsing | **Personal Curation System** — tour browsing becomes compelling only when the user can build and manage collections around tours. These features should be evaluated together in Phase 3 and 4. |
| Real-Time Audio Visualizer | **Animated Visual Indicator** — the real-time visualizer is an enhancement of the must-have animated indicator. The base visual must ship in v1; the real-time version is a v2 upgrade, not a replacement. |
| Song-Version Search | **Personal Curation System** — if the API does not surface curated song versions natively, human curation becomes the data source. Feasibility depends on how well the curation system works. |

---

## 5. Error Handling & Edge Cases

Three failure scenarios were identified during requirements discussion. The design philosophy is consistent across all three: **prevent the error from surfacing to the user where possible**, and degrade gracefully where prevention is not feasible.

| Scenario | Expected Behavior | Rationale |
|---|---|---|
| Show is unavailable | This scenario is prevented at the data layer. Only shows with available streams are surfaced in the UI. The user should never be able to select an unavailable show. | Filtering happens before rendering — no reactive error state needed for this case. |
| Stream fails mid-playback | Playback pauses and the app attempts to reconnect. When connectivity is restored, playback resumes from the last known position. The user is informed of the interruption via a subtle status indicator. | Critical for the RPi use case. Graceful degradation, not a crash or hard stop. |
| Date lookup returns no results | This scenario is prevented at the input layer. The date picker only allows selection of dates that have a show in the database. Invalid dates are visually indicated and not selectable. | Constraint enforced in the UI — the user cannot navigate to a dead end. |

---

## 6. Out of Scope (v1)

The following items were explicitly excluded from v1 during requirements discussion. They are retained here for future reference.

- Mobile applications
- Offline playback or downloading
- Social features, user accounts, or community curation
- Multi-user support
- Writing to phish.in (read-only access only)

---

## 7. Open Items for Phase 3

The following items are unresolved at the close of Phase 2 and are explicitly deferred to Phase 3 (API Feasibility & Testing) for investigation. Findings may shift feature priorities or introduce new requirements.

- **Tour data availability** — Does the phish.in API surface tour boundaries and metadata in a way that supports tour browsing without manual curation? This determines whether tour browsing stays a should-have or can be promoted.
- **Song ratings and notable performances** — What data does the API provide for show ratings, community highlights, and historically notable performances? This determines how much of the "data-driven curation" layer we get for free versus need to build.
- **Audio stream format and gapless feasibility** — What audio formats does phish.in serve? What playback engines support gapless transitions with those formats? This is a core technical risk.
- **Visualizer feasibility** — If VLC or another engine is used for playback, can we access real-time audio stream data (e.g., FFT bins) for a future real-time visualizer? This informs the architecture decision in Phase 5.
- **New capabilities** — The API may expose features not yet anticipated. Phase 3 exploration should flag anything that could become a compelling addition to the feature set.

---

## 8. Approval

This document is approved when the developer confirms the requirements are complete and accurate. Phase 3 may not begin until this approval is given.

**Developer Approval:** //signed human &nbsp; **Date:** January 31, 2026

**PM Acknowledgment:** Claude (AI) &nbsp; | &nbsp; **Date:** January 31, 2026

---

*Requirements Definition v1.0 | Deep-Sea Project | Phase 2 Complete*
