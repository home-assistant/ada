"""The Ada Module."""
import logging
import struct
from typing import Optional

from .homeassistant import HomeAssistant
from .hotword import Hotword
from .microphone import Microphone
from .speech import Speech

_LOGGER = logging.getLogger(__name__)


class Ada:
    """Hey Ada assistant."""

    def __init__(self):
        """Initialize ada."""
        self.homeassistant = HomeAssistant()
        self.hotword: Hotword = Hotword()
        self.speech: Speech = Speech(self.homeassistant)
        self.microphone: Microphone = Microphone(
            self.hotword.frame_length, self.hotword.sample_rate
        )

    def run(self) -> None:
        """Run Ada in a loop."""
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

            text = self.speech.process(self.microphone)
            if not text:
                continue

            answer = self.homeassistant.send_conversation(text)
            print(answer)
