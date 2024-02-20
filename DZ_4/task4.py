import json
import os
from dotenv import load_dotenv

from aiogram import (
    Bot, Dispatcher, executor, types
)

import requests

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        f"Привет @{message.from_user.username}!, "
        f"Нажмите на команду /coffee"
    )


@dp.message_handler(commands=['coffee'])
async def coffee(message: types.Message):

    response = requests.get('https://coffee.alexflipnote.dev/random.json')
    data = response.json()
    data_dict = data
    photo = data_dict['file']

    response = requests.get(photo)
    with open('img_coffee/coffee.jpg', 'wb') as file:
        file.write(response.content)

    photo_file = open('img_coffee/coffee.jpg', 'rb')

    await message.answer_photo(photo=photo_file)

executor.start_polling(dp)
