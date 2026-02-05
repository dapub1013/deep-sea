# Deep-Sea Audio Engine Decision

**Decision Date:** February 4, 2026  
**Phase:** Phase 6 (Development)  
**Decision:** Use pygame.mixer for audio playback  
**Status:** Final

---

## Executive Summary

After attempting to implement gapless audio playback with miniaudio and encountering implementation complexity that blocked progress, the decision has been made to use **pygame.mixer** for the Deep-Sea v1 audio engine.

This represents a pragmatic shift from "perfect gapless" to "good enough gapless" - accepting ~100-300ms gaps between tracks in exchange for dramatically simpler, more maintainable code.

---

## Context

### Original Plan (Phase 5)
- **Audio Engine:** miniaudio (pyminiaudio Python wrapper)
- **Rationale:** True gapless playback via continuous PCM buffer feeding
- **Architecture:** HTTPStreamSource + Python generator for seamless track transitions

### What Actually Happened
- miniaudio implementation proved complex and unreliable in practice
- HTTPStreamSource + generator pattern required deep understanding of audio internals
- Debugging was difficult, progress stalled
- "Perfect" gapless became the enemy of "working"

### The Realization
From docs/lessons-learned/003-gapless-redefined.md:
> "let's define what 'gapless' means... we're working with MP3s, this is not audiophile-level stuff"

**Reality check:**
- We're streaming MP3s from the internet (not local FLAC files)
- This is casual listening, not critical audio production
- phish.in web player has small gaps but they're "almost imperceptible"
- That's the benchmark, not studio-quality gapless playback

---

## The Decision

### Chosen Solution: pygame.mixer

**What it provides:**
- Simple, well-documented API
- Pre-download tracks to cache directory
- Play from disk (no streaming complexity)
- Automatic track end detection
- ~100-300ms gaps between tracks (acceptable)

**What it doesn't provide:**
- Frame-perfect gapless (<10ms)
- On-demand streaming
- Real-time buffer management
- PCM frame access (no built-in visualizer support)

### Architecture

```python
class PygamePlayer(QObject):
    """Simple audio player using pygame.mixer."""
    
    # Qt Signals
    track_changed = pyqtSignal(int)
    position_changed = pyqtSignal(float)
    playback_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        pygame.mixer.init()
        self.track_urls = []
        self.current_track_index = 0
        self.cache_dir = Path.home() / ".deep-sea" / "cache" / "audio"
    
    def play(self):
        """Download track to cache and play."""
        url = self.track_urls[self.current_track_index]
        cache_file = self.cache_dir / f"track_{index}.mp3"
        
        # Download if not cached
        if not cache_file.exists():
            response = requests.get(url)
            cache_file.write_bytes(response.content)
        
        # Play from cache
        pygame.mixer.music.load(str(cache_file))
        pygame.mixer.music.play()
        
        # Auto-advance on track end
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
```

**Key patterns:**
- Download before play (uses cache, no re-download)
- Qt signals for UI integration
- Simple state management (is_playing, current_track_index)
- Auto-advance to next track

---

## Rationale

### Why pygame.mixer?

**1. Simplicity**
- 5-10 lines of code to play a track
- Well-documented, mature library
- Easy to understand and debug
- No complex streaming architecture

**2. Reliability**
- Proven in production (used in many Python projects)
- Known behavior, predictable failure modes
- Simple error handling

**3. "Good Enough" Quality**
- 100-300ms gaps between tracks
- Matches phish.in web player quality
- Acceptable for casual listening
- Natural song boundaries in concerts mask the gaps

**4. Pragmatism**
- Unblocks development immediately
- Can always upgrade to better engine in v2
- Delivers working product faster
- Reduces project risk

### Trade-offs Accepted

| Aspect | pygame.mixer | miniaudio (attempted) |
|--------|--------------|----------------------|
| **Gap Duration** | ~100-300ms | Theoretical <10ms |
| **Code Complexity** | Very simple | Very complex |
| **Reliability** | High (proven) | Low (didn't work for us) |
| **Debugging** | Easy | Difficult |
| **Time to Working** | Hours | Days/weeks |
| **Maintainability** | High | Low |

**Bottom line:** We accept slightly longer gaps in exchange for code that actually works.

---

## Technical Details

### Gap Characteristics

**What causes the gaps:**
1. pygame.mixer.music.play() initializes new track
2. Small delay between track end and next track start
3. Network latency (mitigated by pre-download to cache)
4. Audio system reinitialization

**Gap duration:**
- Typical: 100-200ms
- Maximum: ~300ms
- Context: Human perception threshold ~50ms, but in music context gaps <300ms feel natural

**Comparison:**
- VLC MediaListPlayer: 500-1000ms gaps (unacceptable)
- pygame.mixer: 100-300ms gaps (acceptable)
- miniaudio generator: Theoretical <10ms (if we could make it work)
- phish.in web player: Similar to pygame.mixer

### Cache Strategy

**Why cache?**
- Eliminates network latency during playback
- Enables reliable track start timing
- Disk space is cheap (RPi has plenty)
- Cache persists across sessions (faster on replay)

**Cache location:** `~/.deep-sea/cache/audio/`

**Cache naming:** `track_{index}.mp3`

**Cache invalidation:** Manual cleanup only (v1), future feature for cache management

### UI Integration

**Qt Signals emitted:**
```python
track_changed(int)        # When track switches (index 0-based)
position_changed(float)   # Current position in seconds (1Hz)
playback_finished()       # When all tracks complete
error_occurred(str)       # On download or playback errors
```

**UI signal handlers:**
```python
# Connect signals in PlayerScreen.__init__
self.player.track_changed.connect(self.on_track_changed)
self.player.error_occurred.connect(self.on_error)

# Update UI state
def on_track_changed(self, index):
    self.highlight_track(index)
    self.update_now_playing_label()
    
def on_error(self, error):
    self.show_error_message(error)
```

---

## Alternatives Considered

### 1. miniaudio (Original Plan)
**Pros:**
- True gapless via generator
- PCM frame access (visualizer support)
- Elegant architecture

**Cons:**
- Too complex to implement reliably
- Difficult to debug
- Blocked progress for days
- **Decision:** Rejected due to implementation challenges

### 2. VLC (Existing GD App)
**Pros:**
- Already used in Grateful Dead app
- Known quantity

**Cons:**
- MediaListPlayer has 500-1000ms gaps
- Why we started this project (to fix gaps)
- Not an improvement
- **Decision:** Rejected - doesn't solve the problem

### 3. Just-Audio / Other Libs
**Pros:**
- Various other Python audio libraries exist

**Cons:**
- Unknown reliability
- Additional research/learning required
- pygame.mixer is proven and simple
- **Decision:** Rejected - pygame.mixer is sufficient

### 4. Build Custom Streamer
**Pros:**
- Full control over every detail

**Cons:**
- Massive scope increase
- High complexity, low reliability
- Defeats purpose (build a music player, not an audio engine)
- **Decision:** Rejected - over-engineering

---

## Implementation Plan

### Phase 6 Task Integration

**Task 7: Audio Engine Decision & Implementation**
- Implement PygamePlayer class
- Create test script with public MP3
- Verify audio plays
- Document API

**Task 10: Integrate Audio with Player Screen**
- Connect PygamePlayer to UI
- Wire up Play/Pause/Next buttons
- Handle track changes
- Display errors

**Future Enhancement (v2):**
- If gaps become annoying in real use, revisit miniaudio
- Consider pre-buffering next track for shorter gaps
- Explore fade in/out for smoother transitions

---

## Success Criteria

**Must satisfy:**
- [ ] Audio plays without crashes
- [ ] Tracks advance automatically
- [ ] Gaps are <300ms (not jarring)
- [ ] UI updates on track change
- [ ] Errors are handled gracefully
- [ ] Code is simple and maintainable

**Does NOT need to satisfy:**
- [ ] Frame-perfect gapless (<10ms)
- [ ] Real-time streaming (pre-download is fine)
- [ ] Built-in visualizer support (can add separately)

---

## Lessons Learned

### What We Learned

1. **Perfection is the enemy of progress**
   - "True gapless" was a technical goal, not a user need
   - Users care about "smooth enough", not "technically perfect"

2. **Match the baseline**
   - phish.in web player is the benchmark
   - If our gaps match theirs, we're successful

3. **Complexity has a cost**
   - Complex code is harder to debug
   - Complex code blocks progress
   - Simple code ships

4. **Know when to pivot**
   - Spent days on miniaudio with no progress
   - pygame.mixer working in hours
   - Sunk cost fallacy avoided

### Applying to Future Decisions

**Questions to ask when tempted to over-engineer:**
1. Who is the user? (Me, casual listening)
2. What's the use case? (Streaming concerts while working/relaxing)
3. What's good enough? (phish.in quality is the baseline)
4. What's the cost? (Complexity, debugging time, maintainability)

**Decision framework:**
- Simple and working > perfect and broken
- Match the baseline, don't exceed it (unless trivial)
- Ship working code, iterate later if needed

---

## Approval

**Decision approved by:** Developer (human)  
**Date:** February 4, 2026  
**PM Acknowledgment:** Claude (AI)  
**Status:** Final for v1

**Future review:** If gaps prove annoying in actual daily use, this decision can be revisited for v2.

---

## References

- docs/lessons-learned/004-build-incrementally.md - Process failure that led to this decision
- docs/lessons-learned/003-gapless-redefined.md - Technical expectations adjustment
- docs/06-phase6-task-plan.md - Task 7 implements this decision
- docs/05-technical-architecture.md - Original miniaudio architecture (now outdated)

---

*Audio Engine Decision | Deep-Sea Project | February 4, 2026*
