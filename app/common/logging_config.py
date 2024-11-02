import logging
import logging.config
import os

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'app.log')

logging_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file"]
    }
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger("app_logger")
