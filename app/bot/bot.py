import logging

from telegram.ext import (CallbackQueryHandler, CommandHandler, MessageHandler,
                          filters)

from app.bot import constants, conversation
from app.bot.utils import BotApplication


def main():
    """Запуск бота."""
    application = BotApplication().get_application()
    application.add_handler(
        CommandHandler("start", conversation.start_command)
    )
    application.add_handler(MessageHandler(
        filters.Document.ALL, conversation.get_file)
    )
    application.add_handler(
        CallbackQueryHandler(
            conversation.parse_data,
            pattern=constants.KEYBOARD_PARSE_DATA
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            conversation.get_file_help_message,
            pattern=constants.KEYBOARD_UPLOAD_FILE
        )
    )
    logging.info("Бот запущен")
    application.run_polling()
