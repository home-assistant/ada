"""Helper to hold options for Ada."""
from collections import namedtuple


Options = namedtuple(
    "Options", ["hass_api_url", "hass_token", "stt_platform", "tts_platform", "pixels"]
)
