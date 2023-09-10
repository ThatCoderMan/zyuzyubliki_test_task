import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

LOG_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'

DT_FORMAT = '%d.%m.%Y %H:%M:%S'


class Settings(BaseSettings):
    telegram_token: str
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    product: str = "зюзюбликов"
    debug: bool = False

    class Config:
        env_file = ".env"


def configure_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "bot.log"
    if settings.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=level,
        handlers=(rotating_handler, logging.StreamHandler())
    )


settings = Settings()
