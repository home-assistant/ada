"""Microphone handler."""
from typing import Optional

import pyaudio
import numpy as np
import webrtcvad


class Microphone:
    """Hotword processing."""

    def __init__(self, frame_length: int, sample_rate: int) -> None:
        """Initialize Microphone processing."""
        self.audio = pyaudio.PyAudio()
        self.vad = webrtcvad.Vad(1)
        self.stream: Optional[pyaudio.Stream] = None

        self._frame_length = frame_length
        self._sample_rate = sample_rate
        self._last_frame: Optional[np.ndarray] = None

    @property
    def frame_length(self) -> int:
        """Return frame length for processing hotword."""
        return self._frame_length

    @property
    def sample_rate(self) -> int:
        """Return sample rate for recording."""
        return self._sample_rate

    @property
    def bit_rate(self) -> int:
        """Return bit rate for recording."""
        return pyaudio.paInt16

    @property
    def channel(self) -> int:
        """Return channel for recording."""
        return 1

    def start(self):
        """Open Audio stream."""
        self.stream = self.audio.open(
            rate=self.sample_rate,
            channels=self.channel,
            format=self.bit_rate,
            input=True,
            frames_per_buffer=self.frame_length,
        )

    def stop(self):
        """Close Audio stream."""
        self.stream.close()
        self.stream = None

    def get_frame(self) -> np.ndarray:
        """Read from audio stream."""
        raw = self.stream.read(self.frame_length, exception_on_overflow=False)

        self._last_frame = np.fromstring(raw, dtype=np.int16)
        return self._last_frame.copy()

    def detect_silent(self) -> bool:
        """Return True if on last frame it detect silent."""
        return not self.vad.s_speech(
            self._last_frame[0:480].tostring(), self.sample_rate
        )
