# Deep-Sea: A Phish.in Stream Player - Project Charter

## Project Overview

**Project Name:** Deep-Sea

**Project Manager:** Claude (AI Assistant)

**Developer:** human

**Project Type:** Personal hobby project, open-source upon completion

**Start Date:** January 30, 2026

**Target Completion:** No fixed deadline (quality over speed)

---

## Purpose & Vision

Develop a modern desktop music player that streams Phish concerts from phish.in, serving two primary objectives:

1. Create a polished, daily-use application for personal enjoyment
2. Establish a reusable framework and patterns to refactor an existing Grateful Dead concert streaming application

This is a learning project focused on improving development skills with Claude Code while building something functional and enjoyable.

---

## Scope

### In Scope
- Desktop application for streaming Phish concerts via phish.in API
- Modern, slick UI/UX (significant improvement over previous Grateful Dead app)
- Cross-platform support: macOS (development) and Raspberry Pi 4 with IQAudio DAC (production)
- Core playback features: play/pause, track navigation, volume control
- Concert browsing and selection
- Integration with phish.in's data (shows, setlists, venues, tours, etc.)

### Out of Scope (for v1)
- Mobile applications
- Offline playback/downloading
- Social features or user accounts
- Multi-user support
- Writing to phish.in (read-only access only)

### Open Questions (to be determined in Requirements phase)
- Playlist management
- Favorites/bookmarking
- Search functionality depth
- Queue management
- Local data caching strategy

---

## Success Criteria

**The project is successful when:**

1. **Daily Use Ready:** Application runs reliably on both macOS and Raspberry Pi 4 with IQAudio DAC
2. **Quality Playback:** Audio streams smoothly with proper DAC integration
3. **Polished UI:** Modern interface that reflects design vision and style guide
4. **Framework Documented:** Patterns and decisions documented for Grateful Dead app refactor
5. **Open Source Ready:** Code is clean, documented, and ready for public GitHub repository
6. **Personal Satisfaction:** Developer is proud of the work and enjoys using the application

---

## Target Platforms & Technical Context

**Development Environment:**
- macOS laptop
- Visual Studio Code as IDE
- Claude Code for development assistance

**Production Environment:**
- Raspberry Pi 4 with IQAudio DAC

**Technical Background:**
- Python-based application (PyQt5 + pygame.mixer, decided in Phase 5)
- phish.in API for data and streaming
- Previous similar project: Grateful Dead streaming app (Python + PyQt5)

---

## Project Phases

### Phase 1: Project Charter ✓
**Deliverable:** This document

### Phase 2: Requirements Definition ✓
**Deliverables:**
- Feature list (must-haves vs nice-to-haves)
- User stories/use cases
- Functional requirements document

### Phase 3: API Feasibility & Testing ✓
**Deliverables:**
- API endpoint testing results
- Audio streaming validation
- Data structure documentation
- Rate limit and constraint analysis
- Proof of concept code snippets

### Phase 4: UI/UX Design & Style Guide ✓
**Deliverables:**
- Wireframes/mockups for all major screens
- Comprehensive style guide (colors, typography, spacing, components)
- User flow diagrams
- Design system documentation
**Gate:** No coding begins until this phase is complete and approved

### Phase 5: Technical Architecture Decision ✓
**Deliverables:**
- Tech stack evaluation (PyQt5 + pygame.mixer)
- Architecture documentation
- Development environment setup guide
- Dependency list

### Phase 6: Development (Iterative) ⧗ IN PROGRESS
**Status:** Restarting with incremental approach (Feb 2026)

**Previous Attempt:**
- ✗ miniaudio integration attempted but abandoned (too complex, unreliable)
- ✓ Lessons learned documented (see docs/lessons-learned/004-build-incrementally.md)
- ✓ Audio engine decision revised to pygame.mixer (see docs/07-audio-engine-decision.md)

**Current Status:**
- Starting at: Task 1 (Minimal Application Window)
- Approach: Strict incremental development (one task at a time)
- Audio engine: pygame.mixer (simple, reliable, "good enough" gapless)
- See docs/06-phase6-task-plan.md for complete task breakdown

**Next Steps:**
- Task 1: Create minimal PyQt5 window
- Task 2-5: Build walking skeleton (window + nav + one screen)
- Task 6-12: Implement playable audio (browse → select → play)
- Task 13-18: Add core features (favorites, history, date picker)
- Task 19+: Remaining features (collections, tours, now playing bar)

**Deliverables (to be completed):**
- Working application code
- Progressive feature implementation
- Code documentation
- Pattern documentation (for framework reuse)

### Phase 7: Audio/Hardware Integration & Testing
**Deliverables:**
- Raspberry Pi deployment
- IQAudio DAC integration and testing
- Performance optimization
- Cross-platform validation

### Phase 8: Packaging & Deployment
**Deliverables:**
- Installation/setup documentation
- Distribution package (if applicable)
- User documentation
- GitHub repository preparation

---

## Governance & Working Principles

### Core Principles
1. **Design Before Code:** UI/UX Design & Style Guide must be completed and approved before any application coding begins
2. **Quality Over Speed:** No timeline pressure; focus on learning and building something excellent
3. **Regular Check-ins:** Ongoing collaboration between developer and PM to review progress and make decisions
4. **Document for Reusability:** Capture patterns, decisions, and framework elements that enable portability to Grateful Dead app refactor
5. **Phase Completion:** Informal agreement that a phase is "done" before proceeding to next phase
6. **Build Incrementally:** Never write more than 100 lines without running the app (added Feb 2026)
7. **Test Before Commit:** App must run without errors before marking task complete (added Feb 2026)

### Decision-Making
- Developer has final authority on all decisions
- PM serves as advisor and mentor, expected to push back on risks and challenge assumptions
- Scope changes and "nice-to-have" features discussed in regular meetings

### Progress Tracking
- Simple living roadmap document tracking phase completion
- Checklist of deliverables per phase
- Current status indicator
- Task-by-task tracking in Phase 6 (see docs/06-phase6-task-plan.md)

---

## Constraints & Dependencies

**Technical Constraints:**
- Must work on both macOS and Raspberry Pi 4
- Must integrate with IQAudio DAC
- Read-only access to phish.in (no write operations)
- Solo developer (no team resources)

**Developer Constraints:**
- Strong HTML/CSS skills
- Comfortable with code but relies on Claude Code for Python/JavaScript
- Limited programming experience outside web development

**Dependencies:**
- phish.in API availability and stability (v2, no authentication required)
- Claude Code for development assistance
- Third-party libraries (PyQt5, pygame.mixer, requests, SQLite)

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| phish.in API limitations or changes | High | Early API testing phase to validate capabilities (✓ Complete) |
| Audio streaming quality/format issues | High | Proof of concept testing before full development (✓ Complete - pygame.mixer chosen) |
| Cross-platform compatibility problems | Medium | Test on both platforms throughout development |
| Scope creep (feature additions) | Medium | Regular check-ins to evaluate and prioritize |
| Tech stack choice proves limiting | High | Thorough architecture evaluation phase with prototyping (✓ Complete) |
| Repeating UI redesign mistake | High | Complete UI/UX phase with approval gate before coding (✓ Complete) |
| Building too much without testing | High | Strict incremental development with task-by-task approval (New - Feb 2026) |

---

## Communication & Collaboration

**Regular Meetings:** 
- Frequency to be determined based on phase needs
- Agenda: progress review, blockers, decisions needed, next steps

**Documentation:**
- Phase deliverables documented as completed
- Key decisions logged for future reference
- Patterns documented for Grateful Dead app refactor
- Lessons learned captured in dedicated directory (docs/lessons-learned/)

**Tools:**
- Visual Studio Code
- Claude Code
- GitHub (for version control and eventual open-sourcing)
- Markdown files for documentation

---

## Lessons Learned (Added Feb 2026)

The project maintains a lessons-learned directory documenting all major incidents and process improvements:

1. **001: API Version Documentation Error** - Importance of explicit version documentation
2. **002: Audio Engine API Integration Bugs** - Never trust documentation without testing
3. **003: Redefine Gapless Playback** - Don't over-engineer for perfection
4. **004: Build Incrementally** - Build-test-validate loop is critical

See `docs/lessons-learned/` for complete post-mortems and action items.

---

## Future Considerations

**Post-v1 Possibilities:**
- Grateful Dead app refactor using this framework
- Additional streaming sources
- Enhanced features based on user feedback (if open-sourced)
- Mobile versions
- Community contributions (if open-sourced)

---

## Approval

**Developer Approval:** //signed human  Date: January 30, 2026

**PM Acknowledgment:** Claude (AI)  Date: January 30, 2026

**Phase 6 Status Update:** Claude (AI)  Date: February 4, 2026

---

**Charter Version:** 1.1 (Updated Feb 4, 2026)  
**Last Updated:** February 4, 2026
