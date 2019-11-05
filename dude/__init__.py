"""The Dude Module."""
import logging
import struct
from typing import Optional

import pyaudio

from .hotword import Hotword
from .speech import Speech

_LOGGER = logging.getLogger(__name__)


class Dude:
    """Hey Dude assistant."""

    def __init__(self):
        """Initialize dude."""
        self.hotword: Hotword = Hotword()
        self.speech: Speech = Speech()

        self.audio: Optional[pyaudio.PyAudio] = None
        self.hotword_stream: Optional[pyaudio.Stream] = None
        self.speech_stream: Optional[pyaudio.Stream] = None

    def _open_audio(self):
        """Open Audio stream."""
        self.audio = pyaudio.PyAudio()

        self.hotword_stream = self.audio.open(
            rate=self.hotword.sample_rate,
            channels=self.hotword.channel,
            format=self.hotword.bit_rate,
            input=True,
            frames_per_buffer=self.hotword.frame_length,
        )
        self.speech_stream = self.audio.open(
            rate=self.speech.sample_rate,
            channels=self.speech.channel,
            format=self.speech.bit_rate,
            input=True,
            frames_per_buffer=self.hotword.frame_length,
        )

    def _close_audio(self):
        """Close Audio stream."""
        if self.hotword_stream:
            self.hotword_stream.close()
            self.hotword_stream = None
        if self.speech_stream:
            self.speech_stream.close()
            self.speech_stream = None
        if self.audio:
            self.audio.terminate()
            self.audio = None

    def _read_audio(self):
        """Read from audio stream."""
        pcm_hotword = self.hotword_stream(
            self.hotword.frame_length, exception_on_overflow=False
        )
        pcm_speech = self.speech_stream(
            self.hotword.frame_length, exception_on_overflow=False
        )

        return (pcm_hotword, pcm_speech)

    def run(self) -> None:
        """Run Dude in a loop."""
        self._open_audio()
        try:
            self._run()
        finally:
            self._close_audio()

    def _run(self) -> None:
        """Internal Runner."""
        while True:
            pcm, _ = self._read_audio()
            pcm = struct.unpack_from("h" * self.hotword.frame_length, pcm)

            if not self.hotword.process(pcm):
                continue

            _LOGGER.info("Detect hotword")
