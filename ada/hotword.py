"""Ada hotword enginge."""
import sys
from pathlib import Path
import platform
from typing import TYPE_CHECKING, List, cast

import pyaudio
import numpy as np
import importlib_metadata

if TYPE_CHECKING:
    from pvporcupine.binding.python.porcupine import Porcupine


class Hotword:
    """Hotword processing."""

    def __init__(self) -> None:
        """Initialize Hotword processing."""
        loader = PorcupineLoader()
        self.porcupine = loader.load()

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


class PorcupineLoader:
    """Class to help loading Porcupine."""

    def load(self) -> "Porcupine":
        """Load Porcupine object."""
        dist = importlib_metadata.distribution("pvporcupine")
        porcupine_paths = [
            f
            for f in cast(List[importlib_metadata.PackagePath], dist.files)
            if f.name == "porcupine.py"
        ]

        if not porcupine_paths:
            raise RuntimeError("Unable to find porcupine.py in pvporcupine package")

        porcupine_path = porcupine_paths[0].locate().parent
        lib_path = porcupine_path.parent.parent

        sys.path.append(str(porcupine_path))

        if not TYPE_CHECKING:
            # pylint: disable=import-outside-toplevel, import-error
            from porcupine import Porcupine

        return Porcupine(
            library_path=str(self._library_path(lib_path)),
            model_file_path=str(self._model_file_path(lib_path)),
            keyword_file_path=str(self._keyword_file_path(lib_path)),
            sensitivity=0.5,
        )

    @staticmethod
    def _library_path(lib_path: Path) -> Path:
        """Return Path to library."""
        machine = platform.machine()

        if machine == "x86_64":
            return lib_path / "lib/linux/x86_64/libpv_porcupine.so"
        if machine == "armv7l":
            return lib_path / "lib/raspberry-pi/cortex-a53/libpv_porcupine.so"
        if machine == "armv6l":
            return lib_path / "lib/raspberry-pi/arm11/libpv_porcupine.so"

        raise RuntimeError("Architecture is not supported by Hotword")

    @staticmethod
    def _model_file_path(lib_path: Path) -> Path:
        """Return Path to Model file."""
        return lib_path / "lib/common/porcupine_params.pv"

    @staticmethod
    def _keyword_file_path(lib_path: Path) -> Path:
        """Return Path to hotword keyfile."""
        machine = platform.machine()

        if machine == "x86_64":
            return lib_path / "resources/keyword_files/linux/hey pico_linux.ppn"
        if machine in ("armv7l", "armv6l"):
            return (
                lib_path
                / "resources/keyword_files/raspberrypi/hey pico_raspberrypi.ppn"
            )

        raise RuntimeError("Architecture is not supported by Hotword")
