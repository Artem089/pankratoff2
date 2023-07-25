# main.py или __init__.py
import asyncio
from .utils import send_message_to_telegram


async def send_telegram_message():
    bot_token = "6373170365:AAFuMgN0GWsHNaWX8l6GiaW-X7zguQFvc1Y"
    chat_id = "-991872617"
    message = "Привет, это сообщение из Python!"
    await send_message_to_telegram(message, bot_token, chat_id)


# Создаем асинхронный event loop и вызываем функцию send_telegram_message
loop = asyncio.get_event_loop()
loop.run_until_complete(send_telegram_message())
