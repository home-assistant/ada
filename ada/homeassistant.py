"""Handle Home Assistant requests."""
import logging
import os
from typing import Dict, Optional, Generator

import requests

_LOGGER = logging.getLogger(__name__)


class HomeAssistant:
    """Handle Home Assistant API requests."""

    def __init__(self):
        """Initialize Home Assistant API."""
        self.url = "http://hassio/homeassistant/api"
        self.headers = {"Authorization": f"Bearer {os.environ.get('HASSIO_TOKEN')}"}

    def send_stt(
        self, data_gen: Generator[bytes, None, None]
    ) -> Optional[Dict[str, Optional[str]]]:
        """Send voice to STT handler."""
        headers = {
            **self.headers,
            "X-Speech-Content": "format=wav; codec=pcm; sample_rate=16000; bit_rate=16; channel=1; language=en-US",
        }

        _LOGGER.info("Send voice to Home Assistant STT")
        req = requests.post(f"{self.url}/stt/cloud", data=data_gen, headers=headers)

        if req.status_code != 200:
            return None
        return req.json()

    def send_conversation(self, text: str) -> Optional[str]:
        """Send Conversation text to API."""
        _LOGGER.info("Send text to Home Assistant conversation")
        req = requests.post(
            f"{self.url}/conversation/process",
            json={"text": text},
            headers=self.headers,
        )

        if req.status_code != 200:
            return None
        return req.json()

    def send_tts(self, text: str) -> Optional[str]:
        """Send a text for TTS."""
        _LOGGER.info("Send text to Home Assistant TTS")
        req = requests.post(
            f"{self.url}/tts_get_url",
            json={"platform": "cloud", "message": text},
            headers=self.headers,
        )

        if req.status_code != 200:
            return None
        return req.json()

    def get_tts_audio(self, filename: str) -> Optional[bytes]:
        """Retrieve audio file."""
        _LOGGER.info("Retrieve speech from Home Assistant TTS")
        req = requests.post(f"{self.url}/tts_proxy/{filename}", headers=self.headers)

        if req.status_code != 200:
            return None
        return req.content
