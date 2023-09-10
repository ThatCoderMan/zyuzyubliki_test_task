import logging

import pandas as pd
from prettytable import PrettyTable
from sqlalchemy.exc import IntegrityError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.bot import constants
from app.bot.utils import BotApplication
from app.core.db import AsyncSessionLocal
from app.models import ParsingData
from app.parser.product_parser import parse_products


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start"""
    logging.info(
        f'Команда /start от пользователя {update.effective_chat.username}'
    )
    keyboard = [
        [
            InlineKeyboardButton(
                constants.KEYBOARD_UPLOAD_FILE,
                callback_data=constants.KEYBOARD_UPLOAD_FILE,
            )
        ],
        [
            InlineKeyboardButton(
                constants.KEYBOARD_PARSE_DATA,
                callback_data=constants.KEYBOARD_PARSE_DATA,
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.START_MESSAGE,
        reply_markup=reply_markup,
    )


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получение excel файла, получение и запись информации в БД"""
    logging.info(
        f'Получение файла от пользователя {update.effective_chat.username}'
    )
    application = BotApplication().get_application()
    file_id = update.message.document.file_id
    new_file = await application.bot.get_file(file_id)
    file_path = constants.FILE_PATH + str(file_id)
    await new_file.download_to_drive(file_path)
    try:
        data_frame = pd.read_excel(file_path, header=None)
    except ValueError as exception:
        logging.info(
            f'Файл от пользователя {update.effective_chat.username} '
            f'не соответвует формату: {exception}'
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=constants.GET_FILE_ERROR_MESSAGE,
            parse_mode=ParseMode.HTML,
        )
        return
    table_new, table_exists, table_not_valid = (
        PrettyTable(["name", "url", "xpath"])
        for _ in range(3)
    )
    table_wight = {"name": 4, "url": 18, "xpath": 18}
    table_new._max_width = table_wight
    table_exists._max_width = table_wight
    table_not_valid._max_width = table_wight
    async with AsyncSessionLocal() as session:
        for value in data_frame.values:
            try:
                parsing_data = ParsingData(
                    name=value[0],
                    url=value[1],
                    xpath=value[2]
                )
                session.add(parsing_data)
                await session.commit()
                table_new.add_row([val[:128] for val in value])
                logging.info(f'{parsing_data} добавлен в БД')
            except IntegrityError:
                await session.rollback()
                table_exists.add_row([val[:128] for val in value])
                logging.info(f'{parsing_data} уже есть в БД')
            except ValueError as exception:
                await session.rollback()
                table_not_valid.add_row([val[:128] for val in value])
                logging.info(f'{value[0]} не добавлен в БД: {exception}')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.GET_FILE_MESSAGE.format(
            table_new=table_new,
            table_exists=table_exists,
            table_not_valid=table_not_valid
        ),
        parse_mode=ParseMode.HTML,
    )


async def parse_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Парсинг сайтов из БД, вывод средней цены товаров"""
    logging.info(
        f'Парсинг сайтов для пользователя {update.effective_chat.username}'
    )
    await context.bot.answer_callback_query(
        update.callback_query.id,
        'Парсим сайты'
    )
    results = await parse_products()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.AVG_PRICE_MESSAGE.format(**results),
        parse_mode=ParseMode.HTML,
    )


async def get_file_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Вспомогательное сообщение по отправке файла"""
    logging.info(
        'get_file_help_message для пользователя'
        f' {update.effective_chat.username}'
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.SEND_FILE_HELP_MESSAGE,
    )
