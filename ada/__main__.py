"""Ada assistant."""
import os
import logging

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


def main():
    """Run Application."""
    init_logger()

    options = Options(
        hass_api_url="http://hassio/homeassistant/api",
        hass_token=os.environ.get("HASSIO_TOKEN"),
    )

    ada = Ada(options)
    ada.run()


if __name__ == "__main__":
    main()
