import os
from dotenv import load_dotenv

from random import randint
from aiogram import (
    Bot, Dispatcher, types
)
from aiogram.utils import executor

load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('☃', callback_data='1')
    btn2 = types.InlineKeyboardButton('☃', callback_data='2')
    btn3 = types.InlineKeyboardButton('☃', callback_data='3')
    btn4 = types.InlineKeyboardButton('☃', callback_data='4')
    btn5 = types.InlineKeyboardButton('☃', callback_data='5')
    markup.row(btn1, btn2, btn3, btn4, btn5)

    await message.reply(
        f"Привет <i>@{message.from_user.username}!</i>\n"
        f"\n<b>Выбери одну из пяти кнопок чтобы выйграть!</b>",
        parse_mode='HTML',
        reply_markup=markup
    )


@dp.callback_query_handler()
async def callback_query(call):
    number = str(randint(1, 5))

    if call.data == number:
        await call.message.answer("УРА ВЫ ПОБЕДА, ВЫ ЗАРАБОТАЛИ 0 РУБ.")
    else:
        await call.message.answer("ПРОВАЛ, КОМПУКТЕРЫ ПОБЕДИЛИ!!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
