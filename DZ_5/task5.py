import os
import requests
import json

from aiogram import (
    Bot, Dispatcher, executor, types
)
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привет @{message.from_user.username}! "         
        f"Нажмите на команду /weather"
    )


@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.InlineKeyboardButton(
        text="Отправить геолокацию 🧭",
        request_location=True
    )
    keyboard.add(btn)
    await message.answer(
        text=f'Пожалуста отправьте геолокацию, нажав на кнопку 😉',
        reply_markup=keyboard
    )


@dp.message_handler(content_types=['location'])
async def request_location(message: types.Message):
    await message.answer("Принято!")
    print(user_location)

executor.start_polling(dp, skip_updates=True)
