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
- Python-based application (likely FastAPI + Tailwind + Webview, pending architecture decision)
- phish.in API for data and streaming
- Previous similar project: Grateful Dead streaming app (Python + PyQt5)

---

## Project Phases

### Phase 1: Project Charter ✓
**Deliverable:** This document

### Phase 2: Requirements Definition
**Deliverables:**
- Feature list (must-haves vs nice-to-haves)
- User stories/use cases
- Functional requirements document

### Phase 3: API Feasibility & Testing
**Deliverables:**
- API endpoint testing results
- Audio streaming validation
- Data structure documentation
- Rate limit and constraint analysis
- Proof of concept code snippets

### Phase 4: UI/UX Design & Style Guide
**Deliverables:**
- Wireframes/mockups for all major screens
- Comprehensive style guide (colors, typography, spacing, components)
- User flow diagrams
- Design system documentation
**Gate:** No coding begins until this phase is complete and approved

### Phase 5: Technical Architecture Decision
**Deliverables:**
- Tech stack evaluation (PyQt5 vs FastAPI+Tailwind+Webview)
- Architecture documentation
- Development environment setup guide
- Dependency list

### Phase 6: Development (Iterative)
**Deliverables:**
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

### Decision-Making
- Developer has final authority on all decisions
- PM serves as advisor and mentor, expected to push back on risks and challenge assumptions
- Scope changes and "nice-to-have" features discussed in regular meetings

### Progress Tracking
- Simple living roadmap document tracking phase completion
- Checklist of deliverables per phase
- Current status indicator

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
- phish.in API availability and stability
- Claude Code for development assistance
- Third-party libraries (to be determined in architecture phase)

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| phish.in API limitations or changes | High | Early API testing phase to validate capabilities |
| Audio streaming quality/format issues | High | Proof of concept testing before full development |
| Cross-platform compatibility problems | Medium | Test on both platforms throughout development |
| Scope creep (feature additions) | Medium | Regular check-ins to evaluate and prioritize |
| Tech stack choice proves limiting | High | Thorough architecture evaluation phase with prototyping |
| Repeating UI redesign mistake | High | Complete UI/UX phase with approval gate before coding |

---

## Communication & Collaboration

**Regular Meetings:** 
- Frequency to be determined based on phase needs
- Agenda: progress review, blockers, decisions needed, next steps

**Documentation:**
- Phase deliverables documented as completed
- Key decisions logged for future reference
- Patterns documented for Grateful Dead app refactor

**Tools:**
- Visual Studio Code
- Claude Code
- GitHub (for version control and eventual open-sourcing)
- Markdown files for documentation

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

**Developer Approval:** //signed human  Date: _________

**PM Acknowledgment:** Claude (AI)  Date: January 30, 2026

---

**Charter Version:** 1.0  
**Last Updated:** January 30, 2026
