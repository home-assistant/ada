"""Voice of Ada."""
import subprocess
import logging

from .homeassistant import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Voice:
    """Voice of ada."""

    def __init__(self, homeassistant: HomeAssistant) -> None:
        """Initialize Voice output processing."""
        self.homeassistant: HomeAssistant = homeassistant

    @staticmethod
    def _ffplay(audio: bytes) -> bool:
        """Play Audio file from buffer."""
        ffplay = subprocess.Popen(
            ["ffplay", "-nodisp", "-"], stdin=subprocess.PIPE, stderr=None, stdout=None
        )

        ffplay.communicate(audio)
        return ffplay.returncode == 0

    def process(self, answer: str) -> bool:
        """Process text to voice."""
        url = self.homeassistant.send_tts(answer)
        if not url:
            _LOGGER.warning("Not able to get an TTS URL")
            return False

        filename = url["url"].split("/")[-1]
        _LOGGER.info("TTS is available as %s", filename)

        audio = self.homeassistant.get_tts_audio(filename)
        if not audio:
            _LOGGER.warning("Fails to retrieve the audio file")
            return False

        return self._ffplay(audio)
