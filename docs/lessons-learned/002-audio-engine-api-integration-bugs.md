# Lessons Learned: Audio Engine API Integration Bugs

**Incident #:** 002
**Date:** February 3, 2026
**Phase:** Phase 6 (Development)
**Severity:** High (Multiple bugs preventing core functionality)

---

## Summary

During verification of Phase 6 subtask 4 ("Integrate miniaudio"), a comprehensive review revealed **6 critical bugs** in the audio engine integration code. All bugs stemmed from writing code based on architecture document examples rather than testing against actual API responses.

**Root Cause:** Code written from documentation assumptions without verification against real data.

**Impact:** Audio engine completely non-functional - would fail immediately when attempting to load any show.

**Resolution:** All 6 bugs fixed and verified with integration tests.

---

## Bugs Discovered

### Bug #1: get_show() - Wrong Response Field
**Location:** `data/api_client.py` line 73
**Symptom:** Returns empty dict `{}` instead of show data
**Root Cause:** Code tried to extract `data.get('data', {})` but API v2 returns show directly

**Before:**
```python
data = response.json()
show = data.get('data', {})  # ❌ No 'data' field exists
return show  # Returns {}
```

**After:**
```python
show = response.json()  # ✓ Response IS the show
return show
```

---

### Bug #2: get_shows() - Wrong Response Field
**Location:** `data/api_client.py` line 47
**Symptom:** Returns empty list `[]` instead of shows
**Root Cause:** Code tried to extract `data.get('data', [])` but API returns `shows` field

**Before:**
```python
shows = data.get('data', [])  # ❌ Field is 'shows' not 'data'
```

**After:**
```python
shows = data.get('shows', [])  # ✓ Correct field name
```

---

### Bug #3: get_tours() - Wrong Response Field
**Location:** `data/api_client.py` line 95
**Symptom:** Returns empty list `[]` instead of tours
**Root Cause:** Same as Bug #2 - wrong field name

**Before:**
```python
tours = data.get('data', [])  # ❌ Field is 'tours' not 'data'
```

**After:**
```python
tours = data.get('tours', [])  # ✓ Correct field name
```

---

### Bug #4: get_tour() - Wrong Response Field
**Location:** `data/api_client.py` line 122
**Symptom:** Returns empty dict `{}` instead of tour data
**Root Cause:** Same as Bug #1 - API returns tour directly

**Before:**
```python
tour = data.get('data', {})  # ❌ No 'data' field exists
```

**After:**
```python
tour = response.json()  # ✓ Response IS the tour
```

---

### Bug #5: search_songs() - Wrong Response Field
**Location:** `data/api_client.py` line 149
**Symptom:** Returns empty list `[]` instead of songs
**Root Cause:** Same as Bug #2 - wrong field name

**Before:**
```python
songs = data.get('data', [])  # ❌ Field is 'songs' not 'data'
```

**After:**
```python
songs = data.get('songs', [])  # ✓ Correct field name
```

---

### Bug #6: load_show() - Wrong Track Field Name
**Location:** `audio/engine.py` line 73
**Symptom:** `KeyError: 'mp3'` when trying to load show
**Root Cause:** Tracks use `mp3_url` field, not `mp3`

**Before:**
```python
track_urls = [track['mp3'] for track in show_data['tracks']]  # ❌ KeyError
```

**After:**
```python
track_urls = [track['mp3_url'] for track in show_data['tracks']]  # ✓ Correct field
```

---

## Actual API v2 Response Structure

### Individual Resources (get_show, get_tour)
Response IS the resource directly (not wrapped):

```json
{
  "id": 893,
  "date": "1997-12-31",
  "tracks": [...],
  "venue_name": "Madison Square Garden",
  ...
}
```

### List Endpoints (get_shows, get_tours, search_songs)
Response has pagination wrapper with resource-specific field name:

```json
{
  "shows": [...],           // or "tours", "songs"
  "total_pages": 150,
  "current_page": 1,
  "total_entries": 1500
}
```

### Track Structure
Each track object in the `tracks` array:

```json
{
  "id": 17745,
  "title": "Emotional Rescue",
  "mp3_url": "https://phish.in/blob/plc3ikf1n5pv2pq2zl9d2jz19jxb.mp3",
  "waveform_image_url": "https://phish.in/blob/...",
  "duration": 1036722,
  "set_name": "Set 1",
  ...
}
```

**Key field:** `mp3_url` (NOT `mp3`)

---

## Root Cause Analysis

### How These Bugs Happened

1. **Architecture Document Had Generic Examples**
   Phase 5 doc (section 6.1) showed simplified code examples with placeholder field names like `track['mp3_url']` but also used inconsistent `data.get('data', {})` patterns.

2. **No API Response Validation During Architecture Phase**
   Phase 5 didn't include actual API response samples - examples were written from memory of Phase 3.

3. **Code Written From Docs, Not From Tests**
   Developer (Claude Code) implemented the architecture doc examples directly without first fetching real API data to validate structure.

4. **Tests Written But Never Run**
   File `test_audio_engine.py` existed but was never executed before marking subtask "complete". If run, it would have immediately caught all bugs.

5. **Premature "Complete" Checkmark**
   Phase 6 progress tracker marked audio integration as "✓ PhishInAPI client" without integration testing.

### Why Bugs Weren't Caught Earlier

- No curl/API testing before writing code
- No unit tests run before completion
- No integration test between API client and audio engine
- Completion status based on "code written" not "code tested"

---

## Impact Assessment

### Technical Impact: **Critical**

- **Functionality:** 100% broken - no show could be loaded
- **Error Mode:** Silent failure (empty dicts/lists) OR immediate crash (KeyError)
- **Detection:** Would be caught on first manual test attempt
- **Code Quality:** 6 bugs across 2 files, all from same root cause

### Process Impact: **High**

- Reveals gap in verification workflow
- Demonstrates need for test-first approach
- Shows documentation can't be trusted without validation
- Highlights premature completion declarations

### Learning Value: **Critical**

This incident perfectly demonstrates Lesson #1 from incident 001:
> "Code examples must match testing" - Architecture docs should contain only **verified** code snippets copied from working tests, not written from scratch.

---

## What Went Right

1. **Early Catch:** Bugs discovered during Phase 6 review, before building UI on top of broken foundation
2. **Comprehensive Fix:** All 6 bugs fixed in single session
3. **Verification Created:** New test scripts ensure bugs are actually fixed
4. **Pattern Recognition:** Identified this as the same issue from incident 001

---

## Lessons Learned

### 1. Never Trust Documentation - Verify With Real Data

**Problem:** Code was written based on architecture doc examples that were never validated against actual API responses.

**Solution:** Before writing ANY code that consumes an API:
1. Use curl to fetch actual responses
2. Save responses as test fixtures (JSON files)
3. Write code against the fixtures
4. Verify code works with live API

**Implementation:** Create `test-fixtures/` directory with real API responses.

---

### 2. Test-First Development (Actually Do It)

**Problem:** Tests were written but never run before marking code "complete".

**Solution:** Code is NOT complete until:
1. Tests are written
2. Tests are run
3. Tests pass
4. Evidence of passing tests is documented

**Implementation:** Update Phase 6 workflow - require test output screenshot or log before checking "✓".

---

### 3. Integration Tests Are Critical

**Problem:** Individual components might work in isolation but fail when integrated.

**Solution:** For every subtask:
1. Write unit tests (individual functions)
2. Write integration tests (components working together)
3. Run both before marking complete

**Implementation:** Created `verify_audio_engine.py` - integration test covering API → AudioEngine flow.

---

### 4. Architecture Docs Must Use Verified Code

**Problem:** Phase 5 architecture doc contained code examples written from scratch, not from working tests.

**Solution:** Architecture document code examples must be:
1. Copy-pasted from actual working code
2. Tested against real APIs/data
3. Marked with "Verified against [API/data source]" comment

**Implementation:** Add "Code Verification" section to Phase 5 template requiring actual test runs.

---

### 5. API Response Structure Must Be Documented

**Problem:** Team assumed API structure without checking actual responses.

**Solution:** For every external API:
1. Document actual response structure (not assumed)
2. Include curl examples showing real responses
3. Save sample responses as test fixtures
4. Link to official API documentation

**Implementation:** Create `docs/api-reference/phish-in-v2-responses.md` with actual response examples.

---

## Action Items

### Immediate (Completed)

- [x] Fix all 6 bugs in api_client.py and engine.py
- [x] Create verification test (verify_audio_engine.py)
- [x] Run tests and confirm all pass
- [x] Write post-mortem

### Short-Term (This Project)

- [ ] Create `test-fixtures/` directory with real API responses
- [ ] Document actual API response structure in `docs/api-reference/`
- [ ] Update Phase 6 workflow to require passing tests before "✓"
- [ ] Create integration test suite for all audio engine features
- [ ] Add curl examples to CLAUDE.md for API verification

### Long-Term (Process Improvements)

- [ ] Update Phase 5 template: require verified code examples
- [ ] Add "API Response Validation" step to architecture phase
- [ ] Create "Test Evidence" template (require screenshots/logs)
- [ ] Develop "Integration Test Checklist" for complex features

---

## Prevention Checklist

Use this checklist for future API integrations:

**Before Writing Code:**
- [ ] Fetch actual API responses with curl
- [ ] Save responses as test fixtures
- [ ] Document response structure
- [ ] Verify field names match documentation

**While Writing Code:**
- [ ] Write tests first (test-driven development)
- [ ] Use actual API data in tests (not mocked)
- [ ] Test each method as you write it
- [ ] Don't move to next method until current one works

**Before Marking Complete:**
- [ ] Run full test suite
- [ ] Run integration tests
- [ ] Save test output (logs/screenshots)
- [ ] Verify with real API (not fixtures only)
- [ ] Code review against actual API docs

---

## Comparison to Incident 001

Both incidents share the same root cause but at different scales:

| Aspect | Incident 001 (API Version) | Incident 002 (Integration Bugs) |
|--------|---------------------------|----------------------------------|
| **Root Cause** | Documentation didn't specify version | Documentation had wrong field names |
| **Verification Gap** | Phase 3 → Phase 5 → Phase 6 | Phase 5 → Phase 6 |
| **Bug Count** | 1 (API version URL) | 6 (response field names) |
| **Detection** | Runtime error (401) | Would be KeyError or empty data |
| **Fix Complexity** | 1 line change | 6 line changes |
| **Pattern** | Assumption without verification | Assumption without verification |

**Meta-Lesson:** Incident 001 should have prompted immediate review of ALL API-related code. The fact that incident 002 happened immediately after shows the lesson wasn't fully internalized.

---

## Conclusion

This incident demonstrates that **documentation is not a substitute for testing**. The architecture document contained 6 incorrect code examples because they were written from assumptions rather than copied from working code.

**Key Takeaway:** Code that hasn't been tested against real data isn't "complete" - it's just "typed".

**Positive Outcome:** These bugs were caught during Phase 6 review before any UI code was built on top of them. The design-before-code principle and phase-gate process prevented these bugs from becoming a major refactor.

**Process Improvement:** Moving forward, no code will be marked "complete" without:
1. Running tests that use real API data
2. Documenting test results
3. Verifying integration with dependent components

---

## Test Evidence

Created `verify_audio_engine.py` - comprehensive integration test covering:
- API client show retrieval
- AudioEngine initialization
- Show loading with correct field names
- All API endpoints (shows, tours, songs)

**Test Results (February 3, 2026):**
```
ALL TESTS PASSED ✓
  - API client correctly retrieves show data
  - Audio engine correctly extracts mp3_url fields
  - All API endpoints use correct response field names
```

---

**Document Version:** 1.0
**Author:** Claude Code
**Reviewed By:** Developer
**Date:** February 3, 2026
