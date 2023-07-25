# utils.py
from telegram import Bot


async def send_message_to_telegram(message, bot_token, chat_id):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)
