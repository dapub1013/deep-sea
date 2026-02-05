# Lesson Learned: Redefine "Gapless" Playback

**Date:** February 2026
**Phase:** Phase 6 (Development)
**Context:** Audio engine decision (miniaudio → pygame.mixer)

## Summary

See **docs/07-audio-engine-decision.md** for the complete rationale and lesson learned.

## Key Takeaway

"Gapless" for streaming MP3s doesn't mean frame-perfect (<10ms). It means "smooth enough that gaps don't disrupt the listening experience" (~100-300ms).

**The Realization:**
- We're streaming MP3s from the internet (not local FLAC files)
- This is casual listening, not audiophile playback
- phish.in web player has small gaps but they're acceptable
- That's the benchmark, not studio-quality gapless

**The Decision:** Accept "good enough" gapless (pygame.mixer) over "perfect but broken" (miniaudio).

## Reference

- **Full Documentation:** docs/07-audio-engine-decision.md
- **Audio Engine Decision:** docs/07-audio-engine-decision.md (Section: "Rationale")
- **Gap Characteristics:** docs/07-audio-engine-decision.md (Section: "Technical Details - Gap Characteristics")
