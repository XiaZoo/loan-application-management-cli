
import logging
from pathlib import Path


# --------------------------------------------------
# 1. Logging configuration
# --------------------------------------------------

LOG_LEVEL = logging.INFO

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"

LOG_FILES = {
    "application": "application.log",
    "customer": "customer.log",
    "loan": "loan.log",
    "eligibility": "eligibility.log",
    "repayment": "repayment.log",
}


# --------------------------------------------------
# 2. Log message formatter
# --------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT
)


# --------------------------------------------------
# 3. Logger factory
# --------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Create and return a named logger with its own log file.

    Args:
        name: Logger name (application, customer, loan,
              eligibility, or repayment).

    Returns:
        Configured logging.Logger instance.
    """

    if name not in LOG_FILES:
        raise ValueError(f"Unknown logger name: {name}")

    # Ensure the log directory exists.
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Create a named logger.
    logger = logging.getLogger(f"loan_management.{name}")

    # Set the logger's minimum logging level.
    logger.setLevel(LOG_LEVEL)

    # Prevent duplicate handlers and root logger propagation.
    logger.propagate = False

    if not logger.handlers:

        log_file_path = LOG_DIR / LOG_FILES[name]

        file_handler = logging.FileHandler(
            log_file_path,
            encoding="utf-8"
        )

        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
