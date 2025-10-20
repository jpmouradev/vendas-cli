import logging


def get_logger() -> logging.Logger:
    """Return a configured logger instance for the CLI tool.

    The logger is identified by the name vendas-cli and uses a StreamHandler
    to output human-readable log messages to stdout. If the logger already has
    handlers attached, no new handler is added.

    Returns
    -------
    logging.Logger
        A logger object configured with level INFO and a simple formatter.

    """

    logger = logging.getLogger("vendas-cli")

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
