from telegram.ext import ApplicationBuilder

from app.core.config import settings


class BotApplication(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(BotApplication, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.application = (
            ApplicationBuilder()
            .token(settings.telegram_token)
            .concurrent_updates(True)
            .build()
        )

    def get_application(self):
        return self.application
