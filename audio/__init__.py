"""
Audio module for Deep-Sea

Provides audio playback functionality using miniaudio for streaming
Phish concerts from phish.in.
"""

from .engine import AudioEngine
from .gapless_player import GaplessPlayer
from .http_source import HTTPStreamSource

__all__ = ['AudioEngine', 'GaplessPlayer', 'HTTPStreamSource']
