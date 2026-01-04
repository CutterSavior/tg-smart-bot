from telegram.ext import CommandHandler, MessageHandler, filters
from bot.handlers.reload_cmd import reload_cmd
from bot.handlers.message_handler import smart_reply

class TelegramAdapter:
    @staticmethod
    async def register_handlers(app):
        app.add_handler(CommandHandler("reload", reload_cmd))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))