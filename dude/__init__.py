"""The Dude Module."""
import logging
import struct
from typing import Optional

import pyaudio
import samplerate
import numpy as np

from .hotword import Hotword
from .speech import Speech
from .microphone import Microphone

_LOGGER = logging.getLogger(__name__)


class Dude:
    """Hey Dude assistant."""

    def __init__(self):
        """Initialize dude."""
        self.hotword: Hotword = Hotword()
        self.speech: Speech = Speech()
        self.microphone: Microphone = Microphone()
        self.resampler: samplerate.Resampler = samplerate.Resampler(
            "sinc_best", channels=1
        )

        self.resampler_ratio: float = self.hotword.sample_rate / self.microphone.sample_rate

    def run(self) -> None:
        """Run Dude in a loop."""
        self.microphone.start()
        try:
            self._run()
        finally:
            self.microphone.stop()

    def _run(self) -> None:
        """Internal Runner."""
        while True:
            pcm = self.microphone.get_frame()

            # Need resampling
            if self.resampler_ratio != 1:
                pcm = self.resampler.process(pcm, self.resampler_ratio)

            found: bool = False
            for frame in np.array_split(pcm, self.hotword.frame_length):
                if not self.hotword.process(frame):
                    continue
                found = True
                break

            # Found hotword?
            if not found:
                continue
            _LOGGER.info("Detect hotword")
