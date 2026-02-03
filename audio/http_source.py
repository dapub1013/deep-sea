"""
HTTP Streaming Source for miniaudio

Custom source adapter that enables streaming MP3 files from HTTP URLs
directly into miniaudio for decoding and playback.
"""

import logging
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


class HTTPStreamSource:
    """
    Custom source for HTTP MP3 streaming.

    Downloads MP3 data on-demand from HTTP URLs and provides it to
    miniaudio for decoding. Supports streaming but not seeking.

    Attributes:
        url: The HTTP URL of the MP3 file
        timeout: Request timeout in seconds
    """

    def __init__(self, url, timeout=30):
        """
        Initialize HTTP stream source.

        Args:
            url: HTTP URL of the MP3 file to stream
            timeout: Request timeout in seconds (default: 30)
        """
        self.url = url
        self.timeout = timeout
        self.response = None
        self.buffer = BytesIO()
        self.position = 0
        self.chunk_size = 8192  # 8KB chunks

        logger.debug(f"Initializing HTTP stream for {url}")

        # Start streaming download
        try:
            self.response = requests.get(url, stream=True, timeout=timeout)
            self.response.raise_for_status()
            logger.info(f"HTTP stream connected: {url} ({self.response.headers.get('content-length', 'unknown')} bytes)")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to HTTP stream {url}: {e}")
            raise

    def read(self, num_bytes=-1):
        """
        Read bytes from HTTP stream.

        Args:
            num_bytes: Number of bytes to read (-1 for all available)

        Returns:
            Bytes read from the stream
        """
        if not self.response:
            return b''

        try:
            # Read from response iterator
            if num_bytes == -1:
                # Read all remaining data
                data = b''
                for chunk in self.response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        data += chunk
                self.position += len(data)
                return data
            else:
                # Read specific number of bytes
                chunk = self.response.raw.read(num_bytes)
                if not chunk:
                    logger.debug(f"End of stream reached for {self.url}")
                    return b''  # EOF
                self.position += len(chunk)
                return chunk

        except Exception as e:
            logger.error(f"Error reading from HTTP stream: {e}")
            return b''

    def seek(self, offset, whence=0):
        """
        Seek is not supported for HTTP streams.

        Args:
            offset: Byte offset
            whence: Seek mode (0=absolute, 1=relative, 2=from end)

        Raises:
            NotImplementedError: Seeking not supported for HTTP streams
        """
        raise NotImplementedError("Seeking not supported for HTTP streams")

    def tell(self):
        """
        Get current position in stream.

        Returns:
            Current byte position
        """
        return self.position

    def close(self):
        """Close the HTTP connection."""
        if self.response:
            self.response.close()
            logger.debug(f"HTTP stream closed: {self.url}")
            self.response = None
