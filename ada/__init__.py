"""The Ada Module."""
import logging
import struct
from typing import Optional

from .conversation import Conversation
from .homeassistant import HomeAssistant
from .hotword import Hotword
from .microphone import Microphone
from .speech import Speech
from .voice import Voice

_LOGGER = logging.getLogger(__name__)


class Ada:
    """Hey Ada assistant."""

    def __init__(self):
        """Initialize ada."""
        self.homeassistant = HomeAssistant()
        self.hotword: Hotword = Hotword()
        self.speech: Speech = Speech(self.homeassistant)
        self.conversation: Conversation = Conversation(self.homeassistant)
        self.voice: Voice = Voice(self.homeassistant)
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

            # Start conversation
            wait_time = 2
            while True:
                text = self.speech.process(self.microphone, wait_time)
                if not text or text == "Stop.":
                    break

                answer = self.conversation.process(text)
                if not answer:
                    break

                if not self.voice.process(answer):
                    break
                wait_time = 3
