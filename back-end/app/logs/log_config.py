""" this file configure the logger system of the application """
from logging.config import dictConfig


def init_logger():
    """Function that init the logger object that's properly setup"""

    LOG_LEVEL: str = "DEBUG"
    FORMAT: str = "%(levelprefix)s%(pathname)s:%(lineno)d - %(asctime)s |"\
                  " %(message)s"
    logging_config = {
        "version": 1,  # mandatory field
        "disable_existing_loggers": False,
        "formatters": {
            "basic": {
                "()": "uvicorn.logging.DefaultFormatter",
                "format": FORMAT,
            }
        },
        "handlers": {
            "console": {
                "formatter": "basic",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "level": LOG_LEVEL,
            }
        },
        "loggers": {
            "vibraphile": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                # "propagate": False
            }
        },
    }
    dictConfig(logging_config)
