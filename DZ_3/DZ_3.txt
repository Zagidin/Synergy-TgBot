import os
from dotenv import load_dotenv

from aiogram import (
    Bot, Dispatcher, executor, types
)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(
        f"Привет @{message.from_user.username}! Отправь сообщение с вопросом и вариантами "
        f"ответов (2-11 строк)"
    )


@dp.message_handler()
async def process_message(message: types.Message):
    message_lines = message.text.split("\n")

    if len(message_lines) < 3:
        await message.answer("Слишком короткое сообщение для создания опроса.")
    elif len(message_lines) > 11:
        await message.answer("Слишком много строк для создания опроса.")
    else:
        question = message_lines[0]
        answers = message_lines[1:11]

        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for answer in answers:
            keyboard_markup.add(answer)

        poll_options = [types.PollOption(text=answer) for answer in answers]

        anonymous_poll = types.Poll(
            type=types.PollType.QUIZ,
            question=question,
            options=poll_options,
            is_anonymous=True
        )

        await bot.send_poll(
            chat_id=message.chat.id,
            question=question,
            options=answers,
            is_anonymous=True
        )

executor.start_polling(dp)
