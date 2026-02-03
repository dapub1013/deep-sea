#!/usr/bin/env python3
"""
Audio Integration Demo

Demonstrates miniaudio + HTTPStreamSource working with a public MP3 file.
Note: phish.in API now requires authentication, so we use a public test file.
"""

import logging
import time
import miniaudio

from audio.http_source import HTTPStreamSource

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def demo_audio_playback():
    """Demo audio playback with public MP3."""
    logger.info("=" * 60)
    logger.info("Deep-Sea Audio Integration Demo")
    logger.info("=" * 60)

    # Use a public domain test MP3 (5 seconds of audio)
    # This is just for testing the integration works
    test_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

    try:
        logger.info("Step 1: Creating HTTP stream source...")
        stream = HTTPStreamSource(test_url, timeout=30)

        logger.info("Step 2: Downloading MP3 data (first 1MB)...")
        # Download first 1MB
        data = stream.read(1024 * 1024)
        stream.close()

        logger.info(f"✓ Downloaded {len(data)} bytes")

        logger.info("Step 3: Decoding MP3 with miniaudio...")
        decoded = miniaudio.decode(data, output_format=miniaudio.SampleFormat.SIGNED16)

        logger.info("✓ Decoded successfully:")
        logger.info(f"  - Sample rate: {decoded.sample_rate} Hz")
        logger.info(f"  - Channels: {decoded.nchannels}")
        logger.info(f"  - Samples: {len(decoded.samples)}")

        duration = len(decoded.samples) / (decoded.sample_rate * decoded.nchannels)
        logger.info(f"  - Duration: {duration:.2f} seconds")

        logger.info("")
        logger.info("Step 4: Creating playback device...")
        device = miniaudio.PlaybackDevice(
            sample_rate=decoded.sample_rate,
            nchannels=decoded.nchannels,
            output_format=decoded.sample_format
        )

        logger.info("Step 5: Starting playback (10 seconds)...")
        logger.info(">>> You should hear audio now <<<")
        logger.info("")

        # Create generator that yields chunks on demand
        # miniaudio sends framecount requests to the generator
        def audio_generator():
            samples = decoded.samples
            position = 0
            chunk_size = 4096  # Yield in chunks

            while position < len(samples):
                # Yield next chunk
                end = min(position + chunk_size, len(samples))
                yield samples[position:end]
                position = end

        # Start playback
        device.start(audio_generator())

        # Play for 10 seconds
        for i in range(10):
            time.sleep(1)
            logger.info(f"  Playing... {i+1}/10 seconds")

        # Stop
        logger.info("")
        logger.info("Stopping playback...")
        device.stop()
        device.close()

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ DEMO COMPLETE - Audio integration is working!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Configure phish.in API key for actual show data")
        logger.info("2. Test with real Phish concert MP3s")
        logger.info("3. Implement gapless playback across multiple tracks")

        return True

    except Exception as e:
        logger.error(f"✗ Demo failed: {e}", exc_info=True)
        return False


def main():
    """Run demo."""
    success = demo_audio_playback()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
