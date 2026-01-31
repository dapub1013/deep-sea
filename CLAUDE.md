# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deep-Sea is a desktop music player for streaming Phish concerts from phish.in. This is a learning/hobby project in early stages (Phase 1: Project Charter complete). The project serves dual purposes:
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

**Tech Stack:** TBD (Phase 5) - likely FastAPI + Tailwind + Webview, or PyQt5

## Project Phases & Current Status

**Current Phase:** Phase 2 (Requirements Definition) - Complete

**Phases Overview:**
1. ✓ Project Charter
2. ✓ Requirements Definition
3. API Feasibility & Testing
4. UI/UX Design & Style Guide (MUST complete before coding begins)
5. Technical Architecture Decision
6. Development (Iterative)
7. Audio/Hardware Integration & Testing
8. Packaging & Deployment

**Critical Gate:** No application coding begins until Phase 4 (UI/UX Design & Style Guide) is complete and approved.

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

## Documentation Structure

- `docs/deep-sea-project-charter.md` - Complete project charter defining vision, scope, phases, and governance
- `docs/02-requirements.md` - Requirements definition with must-have, should-have, and nice-to-have features
- `docs/discuss-charter.md` - Initial charter discussion notes
- `notes.txt` - Ongoing project notes and task list

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
