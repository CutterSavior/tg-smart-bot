import asyncio
from telegram.ext import Application
from bot.core.config import SETTINGS
from bot.adapters.telegram_adapter import TelegramAdapter

async def main():
    app = Application.builder().token(SETTINGS.bot_token).build()
    await TelegramAdapter.register_handlers(app)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())