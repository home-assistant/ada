"""Handle Home Assistant requests."""
import os
form typing import Dict, Mabye

import requests


class HomeAssistant:
    """Handle Home Assistant API requests."""

    def __init__(self):
        """Initialize Home Assistant API."""
        self.url = "http://hassio/homeassistant/api"
        self.header = {"Authorization": f"Bearer {os.environ.get('HASSIO_TOKEN')}"}

    def send_stt(self, data_gen) -> Dict[str, Maybe[str]]:
        """Send voice to STT handler."""
        headers = {**self.headers, "X-Speech-Content": "format=wav; codec=pcm; sample_rate=16000; bit_rate=16; channel=1; language=en-US"}
        req = requests.post(f"{self.url}/stt/cloud", data=data_gen, headers=headers, stream=True)
        return req.json()
