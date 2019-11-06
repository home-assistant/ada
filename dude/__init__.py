"""The Dude Module."""
import logging
import struct
from typing import Optional

from .hotword import Hotword
from .speech import Speech
from .microphone import Microphone
from .utils import divide_chunks

_LOGGER = logging.getLogger(__name__)


class Dude:
    """Hey Dude assistant."""

    def __init__(self):
        """Initialize dude."""
        self.hotword: Hotword = Hotword()
        self.speech: Speech = Speech()
        self.microphone: Microphone = Microphone(
            self.hotword.frame_length, self.hotword.sample_rate
        )

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

            if not self.hotword.process(pcm):
                continue

            _LOGGER.info("Detect hotword")
