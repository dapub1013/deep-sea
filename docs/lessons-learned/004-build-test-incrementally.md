# Lesson 004: Build and Test Incrementally

**Date:** 2026-02-03
**Phase:** Phase 6 (Development)
**Status:** Failed attempt, rolled back

## What Went Wrong

Built all 7 application screens (Welcome, Browse, Tours, Tour Detail, Collections, History, Player) in a single session without testing any of them. This resulted in a cascade of runtime errors that compounded on each other:

1. **Data structure mismatch** - API returns `venue` as a dict, UI expected string
2. **Type mismatches** - API returns `duration` as int (seconds), UI expected string ("MM:SS")
3. **Missing data** - Browse screen returns show list without tracks, player needs full show details
4. **pygame initialization** - Event system required full pygame.init(), not just mixer
5. **Load order issues** - Player screen selected tracks before audio engine loaded show
6. **Float formatting** - Position updates passed floats to int-only formatters

Each fix revealed another error. After 5+ crashes, rolled back entire attempt.

## Root Cause

**Violated incremental development**: Built all screens without running the application once. Made assumptions about data structures instead of validating with actual API responses.

## What Should Have Happened

### Correct Approach: Build-Test-Validate Loop

1. **Build ONE screen** (e.g., Welcome)
2. **Run the app** - verify it loads without errors
3. **Test navigation** - click buttons, verify console output
4. **Add NEXT screen** (e.g., Browse)
5. **Run the app** - verify new screen loads
6. **Test integration** - verify navigation between screens works
7. **Repeat** for each additional screen

### Data Structure Validation

Before building UI components:
1. Make actual API call in Python REPL or test script
2. Print/inspect the response structure
3. Document exact field names and types
4. Build UI to match actual data, not assumptions

Example:
```python
# Test FIRST, build SECOND
>>> from data import PhishInAPI
>>> show = PhishInAPI.get_show('1997-12-31')
>>> print(show.keys())
>>> print(show['venue'])  # Is this a string or dict?
>>> print(show['tracks'][0])  # What fields exist?
>>> print(type(show['tracks'][0]['duration']))  # int or string?
```

## Specific Errors to Avoid

### 1. Don't assume data types
❌ **Wrong:** Assume duration is a string because UI needs "MM:SS"
✅ **Right:** Check API response, transform int → string in data layer

### 2. Don't build everything at once
❌ **Wrong:** Build 7 screens, wire up navigation, then test
✅ **Right:** Build screen 1 → test → build screen 2 → test

### 3. Don't skip integration testing
❌ **Wrong:** Unit test each component in isolation, assume integration works
✅ **Right:** Test actual user flow (select show → load player → play audio)

### 4. Don't trust partial API data
❌ **Wrong:** Assume `get_shows()` list items have all fields
✅ **Right:** Verify what fields exist, fetch full details with `get_show(date)` if needed

## Prevention Checklist

Before writing UI code:
- [ ] Have I made an actual API call and inspected the response?
- [ ] Do I know the exact field names and types?
- [ ] Have I tested the previous screen before building this one?
- [ ] Can I run the app and see my changes working?

## Recovery Strategy

When errors cascade (3+ errors in a row):
1. **Stop coding**
2. **Roll back** to last known working state
3. **Identify smallest working unit** (one screen, one feature)
4. **Build incrementally** with testing at each step

## Application to This Project

Next attempt should:
1. Build Welcome screen only
2. Run app, verify it displays
3. Add Browse screen
4. Run app, verify navigation works
5. Test API call with real show selection
6. Add Player screen
7. Test full flow: browse → select → player → audio
8. Only then add remaining screens

## Related Issues

- API authentication requirements (see 001-api-version-documentation-error.md)
- Need to document actual API v2 response structure
- pygame vs miniaudio decision needs revisiting (pygame requires video system init)
