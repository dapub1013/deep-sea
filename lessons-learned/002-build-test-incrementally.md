# Lesson Learned: Build and Test Incrementally

**Date:** February 2026
**Phase:** Phase 6 (Development)
**Context:** Miniaudio implementation attempt

## Summary

See **docs/07-audio-engine-decision.md** for the complete post-mortem and lesson learned.

## Key Takeaway

Never build multiple screens or complex features without running and testing the app. The miniaudio attempt failed because too much code was written without validation, leading to cascading errors that were difficult to debug.

**The Solution:** Incremental development with strict testing:
1. Write < 100 lines of code
2. Run the app
3. Test the feature
4. Commit if working
5. Repeat

## Reference

- **Full Documentation:** docs/07-audio-engine-decision.md (Section: "Lessons Learned")
- **Audio Engine Decision:** docs/07-audio-engine-decision.md
- **Task Plan:** docs/06-phase6-task-plan.md (enforces incremental approach)
