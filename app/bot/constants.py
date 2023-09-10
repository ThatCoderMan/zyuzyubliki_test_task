from app.core.config import settings

START_MESSAGE = f"Привет! Я бот по парсингу {settings.product}."
AVG_PRICE_MESSAGE = (
    "Средняя цена: {price_avg}\n"
    "Успейшный парсинг сайтов: {count}\n"
    "Всего сайтов: {total}"
)
SEND_FILE_HELP_MESSAGE = (
    "Пришли мне excel файл, где первый столбец - название, "
    "второй - URL, третий - xpath запрос."
)
GET_FILE_ERROR_MESSAGE = (
    "Файл не соответсвует формату.\n"
    f"{SEND_FILE_HELP_MESSAGE}"
)
GET_FILE_MESSAGE = (
    "Добавленные файлы:\n"
    "<pre>{table_new}</pre>\n"
    "Уже существуют в БД:\n"
    "<pre>{table_exists}</pre>\n"
    "Неверный формат данных:\n"
    "<pre>{table_not_valid}</pre>\n"
)

KEYBOARD_UPLOAD_FILE = "Загрузить файл"
KEYBOARD_PARSE_DATA = "парсинг товара"

FILE_PATH = "downloads/file_"
