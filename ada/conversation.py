"""Conversation handler."""
import logging
from typing import Optional

from .homeassistant import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Conversation:
    """Conversation handler."""

    def __init__(self, homeassistant: HomeAssistant) -> None:
        """Initialize conversation processing."""
        self.homeassistant: HomeAssistant = homeassistant

    def process(self, text: str) -> Optional[str]:
        """Process Speech to Text."""
        answer = self.homeassistant.send_conversation(text)

        if not answer:
            _LOGGER.error("Can't start a conversation")
            return None
        conversation = answer["speech"]["plain"]["speech"]

        _LOGGER.info("Retrieve follow answer: %s", conversation)
        return conversation
