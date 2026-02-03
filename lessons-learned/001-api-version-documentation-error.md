# Lessons Learned: API Version Documentation Error

**Incident #:** 001  
**Date:** February 3, 2026  
**Phase:** Phase 6 (Development)  
**Severity:** Medium (Low technical impact, high process learning value)

---

## Summary

During Phase 6 development, the API client returned 401 Unauthorized errors when attempting to fetch show data from phish.in. Investigation revealed that the implemented code correctly followed Phase 5 architecture specifications, but those specifications incorrectly documented the API as v1 when Phase 3 testing had actually been conducted against v2.

**Root Cause:** Documentation error in Phase 3 findings that propagated to Phase 5 architecture specs.

**Impact:** ~2 hours of investigation time; one-line code fix required (BASE_URL change).

**Resolution:** API client updated to v2, documentation corrected, post-mortem written.

---

## Timeline

**February 2, 2026 (Phase 3):**
- PM (Claude) conducted API feasibility testing
- Successfully retrieved show data from phish.in
- **Error:** Documented API version as v1 despite testing v2
- Phase 3 findings approved and signed off

**February 2, 2026 (Phase 5):**
- Technical architecture document created
- **Error:** Propagated incorrect v1 API reference from Phase 3
- Phase 5 architecture approved and signed off
- Code examples in documentation specified `BASE_URL = "https://phish.in/api/v1"`

**February 3, 2026 (Phase 6 - Discovery):**
- Developer (human) began implementation
- Claude Code implemented API client per Phase 5 specifications
- API client returned 401 Unauthorized errors
- Claude Code correctly diagnosed authentication requirement
- Created API-AUTHENTICATION-REQUIRED.md incident report

**February 3, 2026 (Phase 6 - Investigation):**
- Developer questioned whether phish.net API key was needed
- PM researched phish.in API documentation
- Discovered API v2 (September 2024) requires no authentication
- Discovered API v1 (legacy) does require authentication
- Browser testing confirmed v2 returns complete setlist data without auth

**February 3, 2026 (Phase 6 - Resolution):**
- Developer updated API client: `BASE_URL = "https://phish.in/api/v2"`
- PM corrected Phase 3 and Phase 5 documentation
- Post-mortem written

---

## Root Cause Analysis

### What Happened

**Phase 3 Testing (The Actual Work):**
- PM tested phish.in API endpoints successfully
- Likely used v2 endpoints (current recommended version)
- Retrieved complete show data including tracks, metadata, etc.
- Confirmed no authentication required

**Phase 3 Documentation (The Error):**
- PM wrote findings document referencing "the phish.in API"
- Did not explicitly document which version was tested
- Section 5 stated "Authentication: None. All endpoints are publicly accessible."
- This was factually correct for v2, but version was not specified

**Phase 5 Architecture (The Propagation):**
- PM created architecture document with code examples
- Included `BASE_URL = "https://phish.in/api/v1"` in API client example
- **Why v1?** Likely assumption based on common API versioning patterns (v1 = first/default)
- Did not verify which version Phase 3 actually tested
- Documentation propagated incorrect version

**Phase 6 Implementation (Correct Behavior):**
- Claude Code followed specifications exactly as documented
- Implemented `BASE_URL = "https://phish.in/api/v1"`
- Encountered 401 errors because v1 requires authentication
- Correctly diagnosed the issue and created incident report

### Contributing Factors

1. **Lack of Version Specificity:** Phase 3 findings did not explicitly state "API v2" anywhere
2. **Assumption Without Verification:** Phase 5 specified v1 without verifying Phase 3 test logs
3. **No Cross-Check:** Documentation was not validated against actual browser testing
4. **API Version Ambiguity:** phish.in has two API versions with different auth requirements but similar functionality

### Why the Error Persisted

- Phase 3 approval focused on feature findings, not implementation details
- Phase 5 approval focused on architecture patterns, assumed API version was verified
- No automated testing caught the discrepancy before Phase 6
- The error was only discovered when code was actually executed

---

## Impact Assessment

### Technical Impact: **Low**

- **Code Changes Required:** One line (BASE_URL update)
- **Functionality Affected:** API client (not yet integrated into UI)
- **Data Loss:** None
- **Deployment Impact:** None (discovered pre-deployment)
- **Rework Required:** Minimal (documentation corrections only)

### Process Impact: **Medium**

- **Time Lost:** ~2 hours (investigation + documentation corrections)
- **Trust Impact:** Low (caught early, quickly resolved)
- **Deliverable Quality:** Medium (documentation accuracy impacted)
- **Phase Delay:** None (caught during Phase 6 dev, before UI integration)

### Learning Value: **High**

- Highlighted importance of version specificity in API documentation
- Demonstrated value of questioning documentation when issues arise
- Reinforced design-before-code principle (error caught before major work built on it)
- Validated phase-gate process (prevented error from reaching production)

---

## What Went Right

1. **Developer Vigilance:** Human questioned the phish.net API key requirement despite documentation
2. **Design-Before-Code Principle:** Error discovered before building UI dependent on API structure
3. **Phase Gates:** Prevented building extensive functionality on incorrect API version
4. **Collaborative Investigation:** PM and developer worked together to diagnose root cause
5. **Quick Resolution:** Once identified, fix was trivial (one-line change)
6. **Documentation Culture:** All findings and corrections documented for future reference

---

## Lessons Learned

### 1. Always Document API Version Explicitly

**Problem:** Phase 3 said "the phish.in API" without version number.

**Solution:** Always document API version explicitly, even if there's only one version:
- **Good:** "Testing conducted against phish.in API v2 (https://phish.in/api/v2)"
- **Bad:** "Testing conducted against phish.in API"

**Implementation:** Update Phase 3 and Phase 5 document templates to include explicit version fields for all external APIs.

### 2. Verify Documentation Against Test Artifacts

**Problem:** Phase 5 specified v1 without checking what Phase 3 actually tested.

**Solution:** Before propagating technical details across phases:
1. Review actual test commands/URLs from previous phase
2. Cross-reference documentation against browser history or test logs
3. If uncertain, re-test to confirm before documenting

**Implementation:** PM should maintain test logs during API exploration phases for future reference.

### 3. Code Examples Must Match Testing

**Problem:** Architecture document included code examples with unverified API version.

**Solution:** All code examples in architecture docs should be directly copy-pasted from working test code, not written from scratch.

**Implementation:** During Phase 5, create a "tested-snippets" directory with validated code that can be directly copied into architecture docs.

### 4. Trust But Verify Developer Questions

**Problem:** Developer questioned phish.net API key requirement, which seemed odd.

**Solution:** When developer questions documentation, treat it as a potential signal of error:
1. Take the question seriously (don't dismiss as confusion)
2. Investigate the original source (API docs, test results)
3. Verify current documentation against source of truth
4. Update documentation immediately if error found

**Implementation:** Add "Developer Questions Log" to track questions that challenge documented specs.

### 5. API Version Changes Are High-Risk

**Problem:** phish.in had two API versions with different auth requirements.

**Solution:** When external APIs have multiple versions:
1. Document which version is used and why
2. Note differences between versions (auth, features, deprecation status)
3. Include API documentation links in project docs
4. Set calendar reminder to check for API deprecation notices

**Implementation:** Create "External Dependencies" section in architecture doc listing all APIs with versions, last verified date, and deprecation status.

---

## Action Items

### Immediate (Completed)

- [x] Update API client to v2
- [x] Correct Phase 3 findings document
- [x] Correct Phase 5 architecture document
- [x] Write post-mortem
- [x] Delete API-AUTHENTICATION-REQUIRED.md (no longer relevant)

### Short-Term (This Project)

- [ ] Add "API Versions" section to CLAUDE.md for future reference
- [ ] Update Phase 3 and Phase 5 document templates to require explicit API versions
- [ ] Create "External Dependencies" section in architecture template

### Long-Term (Process Improvements)

- [ ] Develop "Tested Snippets" practice for architecture phase
- [ ] Create "Developer Questions Log" template for tracking spec challenges
- [ ] Add "Verify Against Test Artifacts" step to phase transition checklist

---

## Recommendations for Similar Projects

### For Grateful Dead App Refactor

1. **Verify API Version First:** Before any coding, confirm which archive.org API version is currently supported
2. **Document Version Explicitly:** State "archive.org API v2" (or whatever version) in requirements
3. **Test Before Documenting:** Run actual API calls in browser/curl, then document what was tested
4. **Cross-Check Documentation:** Before Phase 6, verify all API examples match actual working calls

### For Any External API Integration

1. **Read the Docs First:** Check official API documentation for version info and auth requirements
2. **Test All Endpoints:** Don't assume consistency - test each endpoint you'll use
3. **Document Test URLs:** Keep a log of actual URLs tested during exploration
4. **Version Sunset Tracking:** Set reminders to check for API deprecation announcements

---

## Conclusion

This incident was a **documentation error** that propagated from Phase 3 through Phase 5, caught early in Phase 6. The technical impact was minimal (one-line fix), but the process learning value is high.

**Key Takeaway:** Explicit version documentation and verification against test artifacts would have prevented this error entirely.

**Positive Outcome:** The design-before-code principle and phase-gate process prevented this documentation error from becoming a significant rework issue. Discovering the error before UI integration meant minimal impact.

**Developer Credit:** The developer's instinct to question the phish.net API key requirement was correct and led to catching the documentation error. This reinforces the value of collaborative verification when something doesn't feel right.

---

## Appendix: API Version Comparison

For future reference, here are the key differences between phish.in API versions:

### API v1 (Legacy - 2013)

- **Base URL:** `https://phish.in/api/v1`
- **Authentication:** Required (Bearer token via email request)
- **Catalog:** Shows with available audio only
- **Status:** Legacy, still available but not recommended
- **Use Case:** Existing applications built before 2024

### API v2 (Current - September 2024)

- **Base URL:** `https://phish.in/api/v2`
- **Authentication:** None required
- **Catalog:** Complete catalog including shows without recordings
- **Status:** Current recommended version
- **Use Case:** All new applications (including Deep-Sea)
- **Documentation:** https://phish.in/api-docs

**Deep-Sea uses API v2.**

---

**Document Version:** 1.0  
**Author:** Claude (AI Project Manager)  
**Reviewed By:** human (Developer)  
**Date:** February 3, 2026
