"""Ada hotword enginge."""
import sys
from pathlib import Path
import platform

import pyaudio
import numpy as np

BASE_DIR = Path("/usr/local/lib/python3.7/dist-packages/pvporcupine")

sys.path.append(str(Path(BASE_DIR, "binding/python")))

from porcupine import Porcupine


class Hotword:
    """Hotword processing."""

    def __init__(self) -> None:
        """Initialize Hotword processing."""
        self.porcupine = Porcupine(
            library_path=str(self._library_path),
            model_file_path=str(self._model_file_path),
            keyword_file_path=str(self._keyword_file_path),
            sensitivity=0.5,
        )

    @property
    def frame_length(self) -> int:
        """Return frame length for processing hotword."""
        return self.porcupine.frame_length

    @property
    def sample_rate(self) -> int:
        """Return sample rate for recording."""
        return self.porcupine.sample_rate

    @property
    def bit_rate(self) -> int:
        """Return bit rate for recording."""
        return pyaudio.paInt16

    @property
    def channel(self) -> int:
        """Return channel for recording."""
        return 1

    def process(self, pcm: np.ndarray) -> bool:
        """Process audio frame."""
        return self.porcupine.process(pcm)

    @property
    def _library_path(self) -> Path:
        """Return Path to library."""
        machine = platform.machine()

        if machine == "x86_64":
            return Path(BASE_DIR, "lib/linux/x86_64/libpv_porcupine.so")
        if machine == "armv7l":
            return Path(BASE_DIR, "lib/raspberry-pi/cortex-a53/libpv_porcupine.so")
        if machine == "armv6l":
            return Path(BASE_DIR, "lib/raspberry-pi/arm11/libpv_porcupine.so")
        raise RuntimeError("Architecture is not supported by Hotword")

    @property
    def _model_file_path(self) -> Path:
        """Return Path to Model file."""
        return Path(BASE_DIR, "lib/common/porcupine_params.pv")

    @property
    def _keyword_file_path(self) -> Path:
        """Return Path to hotword keyfile."""
        machine = platform.machine()

        if machine == "x86_64":
            return Path(BASE_DIR, "resources/keyword_files/linux/hey pico_linux.ppn")
        if machine in ("armv7l", "armv6l"):
            return Path(
                BASE_DIR, "resources/keyword_files/raspberrypi/hey pico_raspberrypi.ppn"
            )
        raise RuntimeError("Architecture is not supported by Hotword")
