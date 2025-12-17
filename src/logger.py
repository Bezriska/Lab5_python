import logging


def setup_info_logger():
    logger = logging.getLogger("INFO_logger")
    logger.setLevel(logging.INFO)

    logger_handler = logging.FileHandler("logs.log")
    logger_handler.setLevel(logging.INFO)

    logger_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logger_handler.setFormatter(logger_formatter)

    logger.addHandler(logger_handler)

    return logger


logger = setup_info_logger()
