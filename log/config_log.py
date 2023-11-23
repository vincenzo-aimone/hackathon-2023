import logging


def set_logger() -> logging.Logger:
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)

    file_log = logging.FileHandler("log/log.log")
    file_log.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_log.setFormatter(formatter)
    file_log.setFormatter(formatter)

    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)

    _logger.addHandler(console_log)
    _logger.addHandler(file_log)

    return _logger


logger = set_logger()
