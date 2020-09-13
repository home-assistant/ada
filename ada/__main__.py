"""Ada assistant."""
import logging

import click

from . import Ada
from .options import Options


def init_logger():
    """Initialize python logger."""
    logging.basicConfig(level=logging.INFO)
    fmt = "%(asctime)s %(levelname)s (%(threadName)s) " "[%(name)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # stdout handler
    logging.getLogger().handlers[0].setFormatter(
        logging.Formatter(fmt, datefmt=datefmt)
    )


@click.command()
@click.option("--url", required=True, type=str, help="URL to Home Assistant.")
@click.option(
    "--key", required=True, type=str, help="API access Key to Home Assistant."
)
@click.option(
    "--stt", required=True, type=str, help="Name of Home Assistant STT provider."
)
@click.option(
    "--tts", required=True, type=str, help="Name of Home Assistant TTS provider."
)
@click.option("--ring/--no-ring", type=bool, default=False,)
def main(url, key, stt, tts, ring):
    """Run Application."""
    init_logger()
    if ring:
        from pixel_ring import pixel_ring
        ring = pixel_ring
    options = Options(
        hass_api_url=url,
        hass_token=key,
        stt_platform=stt,
        tts_platform=tts,
        pixels=ring
    )

    ada = Ada(options)
    ada.run()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
