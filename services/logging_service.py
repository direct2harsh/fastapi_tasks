import logging
import sys
from enum import Enum


def setup_logger(name=__name__, level=logging.CRITICAL):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter,)
    logger.addHandler(ch)

    # File handler 
    fh = logging.FileHandler('app.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

logger = setup_logger()




