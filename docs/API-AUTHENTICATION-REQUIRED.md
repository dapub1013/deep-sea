# phish.in API Authentication Update

**Date:** February 3, 2026
**Status:** Action Required

---

## Issue

The phish.in API now requires authentication with an API key. This is a change from the Phase 3 findings which indicated no authentication was required.

## Evidence

```bash
$ curl "https://phish.in/api/v1/shows/1997-12-31"
{"success":false,"error":"No API key provided"}
```

All API endpoints return `401 Unauthorized` without an API key.

## Impact

- Cannot fetch show data from phish.in API
- Audio integration testing limited to public MP3 files
- Full application testing blocked until authentication configured

## Resolution Steps

### 1. Obtain API Key

Contact phish.in to request API access:
- Check phish.in website for API documentation
- Look for API key registration/request process
- Inquire about authentication method (header, query param, OAuth, etc.)

### 2. Update API Client

Modify `data/api_client.py` to include authentication:

```python
class PhishInAPI:
    BASE_URL = "https://phish.in/api/v1"
    API_KEY = None  # Set from environment variable or config

    @staticmethod
    def _get_headers():
        """Get request headers with API key."""
        return {
            "Authorization": f"Bearer {PhishInAPI.API_KEY}",
            # Or: "X-API-Key": PhishInAPI.API_KEY
        }

    @staticmethod
    def get_show(show_date: str) -> Dict:
        url = f"{PhishInAPI.BASE_URL}/shows/{show_date}"
        headers = PhishInAPI._get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()['data']
```

### 3. Configuration

Store API key securely:
- Environment variable: `export PHISHIN_API_KEY="your-key-here"`
- Config file: `~/.deep-sea/config.json` (not in git)
- Application settings (future feature)

### 4. Documentation

Update user documentation with:
- How to obtain API key
- How to configure authentication
- Error messages if key is missing/invalid

## Temporary Workaround

For development and testing, the audio integration can be tested with public MP3 URLs:
- See `test_audio_demo.py` which uses a public domain test file
- This verifies the audio engine works independently of API access

## References

- Phase 3 Findings: docs/03-phase3-findings.md (documented no auth required - now outdated)
- API Documentation: https://phish.in/api-docs
- Audio Integration: docs/06-audio-integration-complete.md

---

**Action Required**: Developer must obtain phish.in API key before proceeding with full application testing.
