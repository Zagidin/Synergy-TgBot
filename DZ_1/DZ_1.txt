import os
from dotenv import load_dotenv

from aiogram import (
    Bot, Dispatcher, executor, types
)

load_dotenv()

bot = Bot(os.getenv("API_TOKEN"))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привет, @{message.from_user.username}!"
    )


# Отправляем тот же смс только повтором
@dp.message_handler(content_types=['text'])
async def echo_message(message: types.Message):
    await message.reply(message.text * 10)


executor.start_polling(dp)
