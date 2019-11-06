"""Dude speech enginge."""
import audioop
import logging
from typing import Optional
from time import monotonic

import pyaudio

from .microphone import Microphone

_LOGGER = logging.getLogger(__name__)

SILENT_WAIT_SECONDS = 3


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

    def process(self, microphone: Microphone) -> Optional[str]:
        """Process speech to text."""
        silent_time = None
        while True:
            pcm = microphone.get_frame()

            if self._detect_silent(pcm.tostring()):
                if silent_time is None:
                    silent_time = monotonic()
                elif monotonic() - silent_time > SILENT_WAIT_SECONDS:
                    _LOGGER.info("Command end")
                    return

    @staticmethod
    def _detect_silent(pcm) -> bool:
        """Detect audio silent."""
        # compute RMS of debiased audio
        energy = -audioop.rms(pcm, 2)
        energy_bytes = bytes([energy & 0xFF, (energy >> 8) & 0xFF])
        debiased_energy = audioop.rms(
            audioop.add(pcm, energy_bytes * (len(pcm) // 2), 2), 2
        )

        if debiased_energy > 30:  # probably actually audio
            return False
        else:
            return True
