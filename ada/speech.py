"""Ada speech enginge."""
import audioop
import io
import logging
import wave
from time import monotonic
from typing import Generator, Optional

import pyaudio

from .homeassistant import HomeAssistant
from .microphone import Microphone

_LOGGER = logging.getLogger(__name__)

SILENT_WAIT_SECONDS = 2


class Speech:
    """Speech processing."""

    def __init__(self, homeassistant: HomeAssistant) -> None:
        """Initialize Audio processing."""
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

        # Send Wave header
        wave_buffer = io.BytesIO()
        wav = wave.open(wave_buffer, "wb")
        wav.setnchannels(self.channel)
        wav.setsampwidth(2)
        wav.setframerate(self.sample_rate)
        wav.close()
        yield wave_buffer.getvalue()

        # Process audio stream
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
            elif silent_time:
                silent_time = None

            yield pcm

    def process(self, microphone: Microphone) -> Optional[str]:
        """Process Speech to Text."""
        speech = self.homeassistant.send_stt(self._get_voice_data(microphone))

        if not speech or speech["result"] != "success":
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

        if debiased_energy > 400:  # probably actually audio
            return False
        else:
            return True
