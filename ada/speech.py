"""Dude speech enginge."""
import audioop
import logging
from typing import Optional, Generator
from time import monotonic

import pyaudio

from .microphone import Microphone
from .homeassistant import HomeAssistant

_LOGGER = logging.getLogger(__name__)

SILENT_WAIT_SECONDS = 2


class Speech:
    """Speech processing."""

    def __init__(self, homeassistant: HomeAssistant) -> None:
        """Initialize Hotword processing."""
        self.homeassistant: HomeAssistant = homeassistant

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

    def _get_voice_data(self, microphone: Microphone) -> Generator[bytes, None, None]:
        """Process voice speech."""
        silent_time = None
        while True:
            pcm = microphone.get_frame()
            pcm = pcm.tostring()

            # Handle silent
            if self._detect_silent(pcm):
                if silent_time is None:
                    silent_time = monotonic()
                elif monotonic() - silent_time > SILENT_WAIT_SECONDS:
                    _LOGGER.info("Voice command ends")
                    return
            else:
                silent_time = None

            yield pcm

    def process(self, microphone: Microphone) -> Optional[str]:
        """Process Speech to Text."""
        _LOGGER.info("Send voice to Home Assistant STT")
        speech = self.homeassistant.send_stt(self._get_voice_data(microphone))

        if speech["result"] != "success":
            _LOGGER.error("Can't detect speech on audio stream")
            return None

        _LOGGER.info("Retrieve follow Voice: %s", speech["text"])
        return speech["text"]

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
