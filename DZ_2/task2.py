import os
from dotenv import load_dotenv

# Импортируем из aiogram отдельные функции
from aiogram import (
    Bot, Dispatcher, executor, types
)

# Импортируем рандинт
from random import randint

load_dotenv()

bot = Bot(os.getenv("API_TOKEN"))
dp = Dispatcher(bot=bot)


# Создаём команду старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}!")


# Обрабатываем текстовые СМС от пользователя
@dp.message_handler(content_types=['text'])
async def message_text(message: types.Message):
    # Если "рандом" содержится в смс пользователя, то вывести рандом число, а дальше понятно :)
    if 'рандом' in message.text.lower():
        await message.reply(f"<i>Рандомное число:</i> <b>{randint(0, 100)}</b>", parse_mode='html')
    else:
        await message.answer(message.text)


executor.start_polling(dp)
