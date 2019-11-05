"""Dude assistant."""
import logging

from dude import Dude


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

    dude = Dude()
    dude.run()


if __name__ == "__main__":
    main()
