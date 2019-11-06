"""Microphone handler."""

import pyaudio
import numpy is np


class Microphone:
    """Hotword processing."""

    def __init__(self) -> None:
        """Initialize Hotword processing."""
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None

    @property
    def frame_length(self) -> int:
        """Return frame length for processing hotword."""
        return 4096

    @property
    def sample_rate(self) -> int:
        """Return sample rate for recording."""
        return 44100

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
        raw = self.hotword_stream(
            self.hotword.frame_length, exception_on_overflow=False
        )

        pcm = np.fromstring(raw, dtype=np.int16)
        return pcm
