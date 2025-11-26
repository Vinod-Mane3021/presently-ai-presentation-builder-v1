import logging
import logging.config
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

import logging
import logging.config
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s [%(asctime)s] %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
        },
    },

    "loggers": {
        "uvicorn.error": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["access_console"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console"],   # ✅ ONLY console
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
