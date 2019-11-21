"""Handle Home Assistant requests."""
import logging
from typing import Dict, Optional, Generator

import requests

from .options import Options

_LOGGER = logging.getLogger(__name__)


class HomeAssistant:
    """Handle Home Assistant API requests."""

    def __init__(self, options: Options):
        """Initialize Home Assistant API."""
        self.options = options
        self.headers = {"Authorization": f"Bearer {options.hass_token}"}

    def send_stt(
        self, data_gen: Generator[bytes, None, None]
    ) -> Optional[Dict[str, Optional[str]]]:
        """Send audio stream to STT handler."""
        headers = {
            **self.headers,
            "X-Speech-Content": "format=wav; codec=pcm; sample_rate=16000; bit_rate=16; channel=1; language=en-US",
        }

        _LOGGER.info("Sending audio stream to Home Assistant STT")
        req = requests.post(
            f"{self.options.hass_api_url}/stt/{self.options.stt_platform}",
            data=data_gen,
            headers=headers,
        )

        if req.status_code != 200:
            return None
        return req.json()

    def send_conversation(self, text: str) -> Optional[dict]:
        """Send Conversation text to API."""
        _LOGGER.info("Send text to Home Assistant conversation")
        req = requests.post(
            f"{self.options.hass_api_url}/conversation/process",
            json={"text": text, "conversation_id": "ada"},
            headers=self.headers,
        )

        if req.status_code != 200:
            return None
        return req.json()

    def send_tts(self, text: str) -> Optional[dict]:
        """Send a text for TTS."""
        _LOGGER.info("Send text to Home Assistant TTS")
        req = requests.post(
            f"{self.options.hass_api_url}/tts_get_url",
            json={"platform": self.options.tts_platform, "message": text},
            headers=self.headers,
        )

        if req.status_code != 200:
            return None
        return req.json()
