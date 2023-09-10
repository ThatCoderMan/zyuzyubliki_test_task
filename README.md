# Zyuzyubliki Test Task
![workflows](https://github.com/ThatCoderMan/zyuzyubliki_test_task/actions/workflows/workflow.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.11
- Python Telegram Bot
- AIOHTTP
- LXML
- SQLAlchemy (async)
- Pydantic
- Alembic
- Pandas
- PrettyTable
- Logging
- GitHub Actions

</details>

## Описание

Данный код представляет собой парсер документации Python. Он предоставляет возможность получить информацию о новых версиях Python, скачать архив с документацией, получить информацию о PEP (Python Enhancement Proposal) и их статусах.

## Установка
Клонируйте репозиторий и перейдите в папку проекта:
```bash
git clone git@github.com:ThatCoderMan/zyuzyubliki_test_task.git
cd zyuzyubliki_test_task
```

Скачайте `poetry` и установите зависимости из `pyproject.toml`:
```bash
poetry install
```

Активируйте виртуальное окружение Poetry, выполнив команду:
```bash
poetry shell
```

Создайте файл `.env` на подобие файла `.env.example` в корневой папке проекта папке:
```bash
touch .env
nano .env
```

Выполните миграции
```bash
alembic upgrade head  
```

Запустите бота:
```bash
python app/main.py
```

### Автор проекта:

[Artemii Berezin](https://github.com/ThatCoderMan)

