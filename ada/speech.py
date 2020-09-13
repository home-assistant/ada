"""Ada speech enginge."""
import io
import logging
import wave
from time import monotonic
from typing import Generator, Optional

import pyaudio

from .homeassistant import HomeAssistant
from .microphone import Microphone

_LOGGER = logging.getLogger(__name__)


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

    def _get_voice_data(
        self, microphone: Microphone, wait_time: int
    ) -> Generator[bytes, None, None]:
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
            pcm = microphone.get_frame().tostring()

            # Handle silent
            if microphone.detect_silent():
                if silent_time is None:
                    silent_time = monotonic()
                elif monotonic() - silent_time > wait_time:
                    _LOGGER.info("Voice command ended")
                    return
            else:
                wait_time = 1
                silent_time = None

            yield pcm

    def process(self, microphone: Microphone, wait_time: int) -> Optional[str]:
        """Process Speech to Text."""
        if self.homeassistant.options.pixels:
            self.homeassistant.options.pixels.listen()
        speech_gen = self._get_voice_data(microphone, wait_time)
        speech = self.homeassistant.send_stt(speech_gen)

        if not speech or speech["result"] != "success":
            _LOGGER.error("Can't detect speech on audio stream")
            return None
        if not speech["text"]:
            _LOGGER.info("No new command given")
            return None

        _LOGGER.info("Retrieved text: %s", speech["text"])
        return speech["text"]
