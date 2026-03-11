import logging
from pathlib import Path

from app.utils.config import BASE_DIR


def setup_logging(log_level: str = "INFO") -> None:
    logs_dir = Path(BASE_DIR / "logs")
    logs_dir.mkdir(exist_ok=True)
    log_path = logs_dir / "app.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    root = logging.getLogger()
    root.setLevel(log_level)

    root.handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root.addHandler(console_handler)
    root.addHandler(file_handler)
