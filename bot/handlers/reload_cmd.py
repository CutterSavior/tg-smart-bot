from telegram import Update
from telegram.ext import ContextTypes
from bot.core.config import SETTINGS
from bot.core.phrase_loader import PhraseLoader
from bot.core.intent_engine import IntentEngine   # 單例
from bot.utils.logger import logger

async def reload_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in SETTINGS.superusers:
        await update.message.reply_text("❌ 您沒有權限")
        return
    try:
        new_phrases = PhraseLoader().load()
        IntentEngine.reload(new_phrases)   # 重新計算索引
        await update.message.reply_text("✅ 詞條與設定已熱更新")
        logger.info(f"User {uid} triggered reload")
    except Exception as e:
        await update.message.reply_text(f"⚠️ 更新失敗：{e}")