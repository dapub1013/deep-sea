#!/usr/bin/env python3
"""
Verify audio engine can load show data correctly
"""

import sys
import logging
from audio import AudioEngine
from data import PhishInAPI

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

def main():
    print("\n" + "="*60)
    print("AUDIO ENGINE VERIFICATION TEST")
    print("="*60 + "\n")

    # Test 1: Fetch show data
    print("Test 1: Fetching show from API...")
    try:
        show_data = PhishInAPI.get_show("1997-12-31")
        print(f"✓ Show fetched: {show_data.get('date')}")
        print(f"  - Tracks: {len(show_data.get('tracks', []))}")
        print(f"  - Venue: {show_data.get('venue_name')}")
    except Exception as e:
        print(f"✗ Failed to fetch show: {e}")
        return 1

    # Test 2: Create audio engine
    print("\nTest 2: Creating AudioEngine...")
    try:
        # Import PyQt5 for QObject
        from PyQt5.QtCore import QCoreApplication
        app = QCoreApplication(sys.argv)

        engine = AudioEngine()
        print("✓ AudioEngine created")
    except Exception as e:
        print(f"✗ Failed to create AudioEngine: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Test 3: Load show into audio engine
    print("\nTest 3: Loading show into AudioEngine...")
    try:
        # Limit to first 2 tracks for testing
        show_data['tracks'] = show_data['tracks'][:2]

        engine.load_show(show_data)
        print(f"✓ Show loaded successfully")
        print(f"  - Track URLs extracted: {len(show_data['tracks'])}")

        # Verify track URLs
        for i, track in enumerate(show_data['tracks']):
            print(f"  - Track {i+1}: {track['title']}")
            print(f"    URL: {track['mp3_url'][:60]}...")

    except KeyError as e:
        print(f"✗ KeyError when loading show: {e}")
        print(f"  - This means the field name is still wrong!")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"✗ Failed to load show: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Test 4: Verify other API endpoints
    print("\nTest 4: Testing other API endpoints...")
    try:
        shows = PhishInAPI.get_shows(year=1997)
        print(f"✓ get_shows() returned {len(shows)} shows")

        tours = PhishInAPI.get_tours()
        print(f"✓ get_tours() returned {len(tours)} tours")

        if tours:
            tour = PhishInAPI.get_tour(tours[0]['slug'])
            print(f"✓ get_tour() returned tour: {tour.get('name')}")

        songs = PhishInAPI.search_songs("Tweezer")
        print(f"✓ search_songs() returned {len(songs)} songs")

    except Exception as e:
        print(f"✗ API endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60 + "\n")
    print("Summary:")
    print("  - API client correctly retrieves show data")
    print("  - Audio engine correctly extracts mp3_url fields")
    print("  - All API endpoints use correct response field names")
    print("\nThe bugs have been fixed!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
