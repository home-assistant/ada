"""Dude speech enginge."""

import pyaudio


class Speech:
    """Speech processing."""

    def __init__(self) -> None:
        """Initialize Hotword processing."""

    @property
    def sample_rate(self) -> int:
        """Return sample rate for recording."""
        return 16000

    @property
    def bit_rate(self) -> int:
        """Return bit rate for recording."""
        return pyaudio.paInt16

    @property
    def channel(self) -> int:
        """Return channel for recording."""
        return 1
