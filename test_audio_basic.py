#!/usr/bin/env python3
"""
Basic Audio Integration Test

Tests miniaudio with HTTPStreamSource at a fundamental level.
This is a command-line test that verifies:
1. HTTP streaming works
2. MP3 decoding works
3. Basic miniaudio playback works
"""

import logging
import time
import miniaudio

from audio.http_source import HTTPStreamSource

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_http_stream_download():
    """Test 1: HTTP stream download."""
    logger.info("=" * 60)
    logger.info("TEST 1: HTTP Stream Download")
    logger.info("=" * 60)

    # Use a short track from a famous show
    # This is the first track from 1997-12-31 (Down with Disease)
    test_url = "https://phish.in/audio/000/035/199/35199.mp3"

    try:
        logger.info(f"Creating HTTP stream for: {test_url}")
        stream = HTTPStreamSource(test_url, timeout=30)

        logger.info("Reading first 1KB of data...")
        data = stream.read(1024)

        if data:
            logger.info(f"✓ Successfully read {len(data)} bytes")
            logger.info(f"✓ First bytes: {data[:16].hex()}")

            # Check for MP3 signature
            if data[0:3] == b'ID3' or data[0:2] == b'\xff\xfb':
                logger.info("✓ Valid MP3 data detected")
            else:
                logger.warning("! Data doesn't look like MP3")

            stream.close()
            return True
        else:
            logger.error("✗ No data received")
            return False

    except Exception as e:
        logger.error(f"✗ HTTP stream test failed: {e}", exc_info=True)
        return False


def test_mp3_decode():
    """Test 2: MP3 decoding with miniaudio."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 2: MP3 Decoding")
    logger.info("=" * 60)

    # Use first 10 seconds of a track
    test_url = "https://phish.in/audio/000/035/199/35199.mp3"

    try:
        logger.info("Downloading MP3 data...")
        stream = HTTPStreamSource(test_url, timeout=30)

        # Read first 512KB (should be enough for ~10 seconds at 320kbps)
        data = stream.read(512 * 1024)
        stream.close()

        logger.info(f"Downloaded {len(data)} bytes")

        logger.info("Decoding MP3...")
        decoded = miniaudio.decode(data, output_format=miniaudio.SampleFormat.SIGNED16)

        logger.info(f"✓ Decoded successfully:")
        logger.info(f"  - Sample rate: {decoded.sample_rate} Hz")
        logger.info(f"  - Channels: {decoded.nchannels}")
        logger.info(f"  - Sample format: {decoded.sample_format}")
        logger.info(f"  - Sample count: {len(decoded.samples)}")

        duration = len(decoded.samples) / (decoded.sample_rate * decoded.nchannels)
        logger.info(f"  - Duration: {duration:.2f} seconds")

        return True

    except Exception as e:
        logger.error(f"✗ MP3 decode test failed: {e}", exc_info=True)
        return False


def test_playback():
    """Test 3: Actual audio playback."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST 3: Audio Playback (5 seconds)")
    logger.info("=" * 60)

    test_url = "https://phish.in/audio/000/035/199/35199.mp3"

    try:
        logger.info("Setting up playback...")

        # Download first chunk
        stream = HTTPStreamSource(test_url, timeout=30)
        data = stream.read(512 * 1024)  # 512KB
        stream.close()

        # Decode
        decoded = miniaudio.decode(data, output_format=miniaudio.SampleFormat.SIGNED16)

        logger.info(f"Creating playback device...")
        device = miniaudio.PlaybackDevice(
            sample_rate=decoded.sample_rate,
            nchannels=decoded.nchannels,
            output_format=decoded.sample_format
        )

        logger.info("Starting playback for 5 seconds...")
        logger.info("(You should hear audio now)")

        # Create generator
        def audio_generator():
            yield decoded.samples

        # Start playback
        device.start(audio_generator())

        # Play for 5 seconds
        time.sleep(5)

        # Stop
        device.stop()
        device.close()

        logger.info("✓ Playback test completed")
        return True

    except Exception as e:
        logger.error(f"✗ Playback test failed: {e}", exc_info=True)
        return False


def main():
    """Run all tests."""
    logger.info("Starting Deep-Sea Audio Integration Tests")
    logger.info("")

    results = []

    # Run tests
    results.append(("HTTP Stream Download", test_http_stream_download()))
    results.append(("MP3 Decoding", test_mp3_decode()))
    results.append(("Audio Playback", test_playback()))

    # Print summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        logger.info(f"{test_name}: {status}")

    all_passed = all(result[1] for result in results)

    logger.info("")
    if all_passed:
        logger.info("✓ All tests passed! Audio integration is working.")
    else:
        logger.info("✗ Some tests failed. Check logs above for details.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
