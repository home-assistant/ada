"""Voice of Ada."""
import logging
import subprocess

from .homeassistant import HomeAssistant
from .options import Options

_LOGGER = logging.getLogger(__name__)


class Voice:
    """Voice of ada."""

    def __init__(self, homeassistant: HomeAssistant, options: Options) -> None:
        """Initialize Voice output processing."""
        self.homeassistant: HomeAssistant = homeassistant
        self.options: Options = options

    def _play(self, audio_url: str) -> bool:
        """Play Audio file from buffer."""
        play = subprocess.Popen(
            [
                "mplayer",
                "-quiet",
                "-prefer-ipv4",
                "-http-header-fields",
                f"Authorization: Bearer {self.options.hass_token}",
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
            _LOGGER.warning("Not able to get a TTS URL")
            return False

        filename = url["url"].split("/")[-1]
        _LOGGER.info("TTS is available as %s", filename)

        return self._play(f"{self.options.hass_api_url}/tts_proxy/{filename}")
