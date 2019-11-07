"""Voice of Ada."""
import logging
import os
import subprocess

from .homeassistant import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Voice:
    """Voice of ada."""

    def __init__(self, homeassistant: HomeAssistant) -> None:
        """Initialize Voice output processing."""
        self.homeassistant: HomeAssistant = homeassistant

    @staticmethod
    def _play(audio_url: str) -> bool:
        """Play Audio file from buffer."""
        play = subprocess.Popen(
            [
                "mplayer",
                "-quiet",
                "-http-header-fields",
                f"Authorization: Bearer {os.environ.get('HASSIO_TOKEN')}",
                audio_url,
            ],
            stdin=None,
            stderr=None,
            stdout=None,
        )

        play.wait()
        return play.returncode == 0

    def process(self, answer: str) -> bool:
        """Process text to voice."""
        url = self.homeassistant.send_tts(answer)
        if not url:
            _LOGGER.warning("Not able to get an TTS URL")
            return False

        filename = url["url"].split("/")[-1]
        _LOGGER.info("TTS is available as %s", filename)

        return self._play(f"{self.homeassistant.url}/tts_proxy/{filename}")
