# Deep-Sea — Phase 3 Findings

**Phase 3 Deliverable | February 2, 2026**

---

## 1. Purpose

This document consolidates all findings from Phase 3 (API Feasibility & Testing). It resolves the five open items deferred from Section 7 of the requirements document, records a priority shift, and documents one early architecture decision that Phase 3 investigation forced.

All findings are intended to inform Phase 4 (UI/UX Design) and Phase 5 (Technical Architecture Decision).

---

## 2. Resolution of Phase 2 Open Items

The requirements document (Section 7) deferred five items to Phase 3. All five are resolved below.

### 2.1 Tour Data Availability

**Question:** Does the phish.in API surface tour boundaries and metadata in a way that supports tour browsing without manual curation?

**Finding:** Yes. Tours are a first-class entity in the API. The `/tours` endpoint returns 42 pages of tour objects, each containing `name`, `slug`, `starts_on`, `ends_on`, `shows_count`, and `shows_with_audio_count`. Crucially, `tour_name` is also embedded directly on every show object, meaning tour context is available without a secondary lookup.

**Decision:** Tour browsing is promoted from Should-Have to Must-Have. The data cost is zero — the API already provides everything needed. See Section 3.

### 2.2 Song Ratings and Notable Performances

**Question:** What data does the API provide for show ratings, community highlights, and historically notable performances?

**Finding:** The API includes a tags system comprising 22 tags across five groups. The standout tag is **Jamcharts**, categorized under "Community Picks", which covers 5,008 tracks. This is a community-curated highlight system already baked into the data. Individual tracks also carry a `likes_count` field and, significantly, a `jam_starts_at_second` field that provides a direct timestamp pointer to the highlight moment within a track's audio.

Show-level ratings (star ratings on phish.net) are not surfaced through the phish.in API. This is not a gap — Jamcharts and per-track likes provide a more useful signal for a listening application than aggregate star ratings.

**Decision:** No action required. The curation layer exists. Surface Jamcharts and `jam_starts_at_second` in the UI design (Phase 4).

### 2.3 Audio Stream Format and Gapless Feasibility

**Question:** What audio formats does phish.in serve? What playback engines support gapless transitions with those formats?

**Finding:** phish.in serves MP3 only. Audio files are hosted on phish.in's blob storage and cached via Cloudflare CDN. Each track object includes a direct `mp3_url`.

Gapless playback was validated as the critical technical risk of the project. The existing Grateful Dead streaming app (deadstream) on identical hardware (RPi 4 + IQAudio DAC) uses VLC's `MediaListPlayer` for this purpose. Testing on both macOS and RPi confirmed that VLC introduces a brief silence between tracks when streaming MP3s over HTTP. The root cause is architectural: `MediaListPlayer` is designed for local playlists and does not pre-buffer the next HTTP stream before the current one ends. Network latency on the first fetch of each new stream creates the gap. This is consistent across formats (MP3, FLAC, SHN) and platforms, ruling out codec or hardware causes.

An alternative engine was investigated. See Section 4 (Early Architecture Decision).

### 2.4 Visualizer Feasibility

**Question:** Can we access real-time audio stream data (e.g., FFT bins) for a future real-time visualizer?

**Finding:** This is resolved as a direct consequence of the audio engine decision in Section 4. The recommended engine (miniaudio) exposes raw PCM frames through a Python generator. A `frame_process_method` callback is available via `stream_with_callbacks()` that receives every buffer of PCM data before it reaches the DAC. This is exactly the tap point needed for FFT-based visualization — no additional plumbing required.

**Decision:** Real-time visualizer remains Nice-to-Have for v1. The architectural path to it is clear and costs nothing to preserve. The animated visual indicator (Must-Have) ships in v1; the real-time version is a v2 upgrade that slots in at the same design position.

### 2.5 New Capabilities

**Question:** Did Phase 3 exploration surface features not yet anticipated?

**Finding:** Three items worth noting for Phase 4 design:

**`jam_starts_at_second`** — Every track object optionally includes a timestamp (in seconds) for where the jam or highlight moment begins. This could inform a "jump to highlight" control in the player UI, distinct from jump-to-track. A small feature with outsized impact on the listening experience.

**Waveform images** — Every track includes a `waveform_image_url` (PNG). These are pre-rendered by phish.in. Free visual content for the track list or player screen — no client-side audio analysis needed.

**Community playlists** — phish.in hosts user-created playlists (public, browsable via API, read-only without auth). Deep-Sea's personal curation system remains local as designed, but importing a community playlist as a starting point is a low-effort feature worth considering in Phase 4.

---

## 3. Priority Shift

The following change to the requirements document is recommended based on Phase 3 findings:

| Feature | Previous Priority | New Priority | Rationale |
|---|---|---|---|
| Tour Browsing | Should-Have | **Must-Have** | Tour data is first-class in the API at zero additional cost. Combined with the personal curation system (already Must-Have), tour browsing becomes a core navigation pattern, not an add-on. |

---

## 4. Early Architecture Decision — Audio Engine

Phase 3 was intended to inform the architecture decision in Phase 5, not make one. The audio engine investigation forced an exception. The gapless playback requirement — the most technically risky Must-Have in the project — cannot be adequately addressed by VLC when streaming MP3s over HTTP. Waiting until Phase 5 to resolve this would mean designing the UI (Phase 4) without knowing whether the primary listening experience actually works.

**Recommendation: Replace VLC with miniaudio as the playback engine.**

The case for miniaudio:

miniaudio is a Python wrapper around the miniaudio C library (dr-soft/miniaudio). It provides native MP3 and FLAC decoding, runs on macOS and Linux (including Raspberry Pi, with pre-built wheels on PiWheels), and requires no external dependencies.

The key architectural difference is how playback works. miniaudio's `PlaybackDevice` runs a continuous callback loop that pulls audio frames from a Python generator. The application controls that generator. When one track's decoder runs out of frames, the generator simply begins yielding frames from the next track's decoder. The playback device never stops, never reinitializes, never creates a boundary event. There is no gap to introduce. This is fundamentally different from VLC's `MediaListPlayer`, which manages discrete media objects and must open each new HTTP stream as a separate operation.

The one component that needs to be built is an HTTP streaming adapter — a thin `StreamableSource` subclass that wraps an HTTP URL download into the interface miniaudio expects for network audio. This is approximately 30 lines of code and is a reusable component for both Deep-Sea and the future Grateful Dead app refactor.

This decision does not affect the rest of the Phase 5 architecture evaluation. The UI layer (FastAPI + Tailwind + webview) remains under consideration as designed. Only the audio engine is resolved early.

**Maintenance note:** The pyminiaudio package (v1.61, last released July 2024) shows no recent commits, which prompted a health check. The underlying C library (dr-soft/miniaudio) is actively maintained. The Python bindings are a thin cffi wrapper around a stable C API — the absence of recent Python-layer commits reflects maturity, not abandonment. The library is MIT licensed.

---

## 5. Validated Data Layer Summary

For reference during Phase 4 design, the following data is available per API call with no authentication required:

**Per show:** date, venue, tour name, taper notes, cover art (three sizes), album zip, tags, likes count, previous/next show dates (with and without audio), ordered track list.

**Per track:** title, position, set name, duration, direct MP3 URL, waveform image URL, `jam_starts_at_second`, tags, likes count, audio status.

**Filtering:** Server-side filtering via `audio_status=complete` returns only streamable shows. The date picker requirement (only dates with available shows are selectable) can be enforced by querying available show dates from the API.

**Authentication:** None. All endpoints are publicly accessible.

---

## 6. Approval

This document is approved when the developer confirms the findings are complete and the recommended decisions are accepted. Phase 4 may not begin until this approval is given.

**Developer Approval:** _____________________________________ &nbsp; **Date:** _______________

**PM Acknowledgment:** Claude (AI) &nbsp; | &nbsp; **Date:** February 2, 2026

---

*Phase 3 Findings v1.0 | Deep-Sea Project | Phase 3 Complete*
