import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.append(str(Path(__file__).parent.parent))

from app.bot.bot import main  # noqa
from app.core.config import configure_logging  # noqa

if __name__ == '__main__':
    configure_logging()
    main()
