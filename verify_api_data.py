#!/usr/bin/env python3
"""
Quick verification script to check API data structure
"""

import sys
from data import PhishInAPI

def main():
    print("Fetching show from phish.in API v2...")
    show_data = PhishInAPI.get_show("1997-12-31")

    print(f"\nShow date: {show_data.get('date')}")
    print(f"Number of tracks: {len(show_data.get('tracks', []))}")

    # Check first track structure
    if show_data.get('tracks'):
        track = show_data['tracks'][0]
        print(f"\nFirst track fields:")
        for key in sorted(track.keys()):
            value = track[key]
            if isinstance(value, str) and len(value) > 60:
                value = value[:60] + "..."
            print(f"  - {key}: {value}")

        # Check for mp3 vs mp3_url
        print(f"\n✓ Field check:")
        print(f"  - 'mp3' field exists: {'mp3' in track}")
        print(f"  - 'mp3_url' field exists: {'mp3_url' in track}")

        if 'mp3_url' in track:
            print(f"\n✓ MP3 URL found: {track['mp3_url']}")
        else:
            print(f"\n✗ No mp3_url field found!")

        # This is what the code currently tries to do
        print(f"\n✗ Testing current code behavior:")
        try:
            mp3 = track['mp3']
            print(f"  - track['mp3'] = {mp3}")
        except KeyError as e:
            print(f"  - KeyError: {e} (field does not exist)")
            print(f"  - This would cause the audio engine to fail!")

if __name__ == "__main__":
    main()
