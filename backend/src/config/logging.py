import logging
import sys
from src.middleware.request_id import request_id_context

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_context.get()
        return True


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(RequestIdFilter())

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | [%(request_id)s] | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplicate logs
    root_logger.handlers.clear()

    root_logger.addHandler(handler)

    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s | %(levelname)s | %(request_id)s | %(name)s | %(message)s",
    #     handlers=[
    #         logging.StreamHandler(sys.stdout)
    #     ], 
    # )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)    



# from src.core.logging import get_logger

# logger = get_logger(__name__)