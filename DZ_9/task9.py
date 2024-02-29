import os
from idlelib import query

from dotenv import load_dotenv
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()
storage = MemoryStorage()

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)

count = 1


class GameRPG(StatesGroup):
    game1 = State()
    game2 = State()
    game3 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Привет @{message.from_user.username}"
        f"\nЭто текстовая RPG игра 👾\n"
        f"\nЧтобы начать нажмите на /play_game 🤖"
    )


@dp.message_handler(commands=['play_game'])
async def play_game(message: types.Message):
    global count

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            text=f"Забрать первую Priory: {count} 🚘",
            callback_data='play_start'
        )
    )

    await message.answer(
        "Вы играете за ZAGA, которому нужно собрать как можно болшьше Prior 🚘\n"
        "Чтобы быть крутым",
        reply_markup=markup
    )

    await GameRPG.game1.set()


@dp.callback_query_handler(state=GameRPG.game1)
async def callback_query(call, state: FSMContext):
    global count

    if call.data == 'play_start':

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(
            text='Отдать Priory {} 🗿'.format(count),
            callback_data='play_start_1'
        )
        btn2 = types.InlineKeyboardButton(
            text='Сразиться за Priory 🚘💪',
            callback_data='play_start_2'
        )
        markup.add(
            btn1,
            btn2
        )

        await call.message.answer(
            "У вас на пути появился злодей! Что сделать?",
            reply_markup=markup
        )

        await GameRPG.next()


@dp.callback_query_handler(state=GameRPG.game2)
async def callback_query(call, state: FSMContext):
    global count

    if call.data == 'play_start_1':
        count -= 1

        await state.finish()

        await call.message.answer(
            "Ну ты и конечно 🗿 испугался, потерял свою Priory 🚘\n"
            "У тебя теперь: {} Prior 🚘".format(count)
        )
        count += 1

    elif call.data == 'play_start_2':
        count += 200

        await call.message.answer("Ай ХАРОШ!!\nТы забрал у него 200 Prior 🚘, ты в плюсе! 💪💪")

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                text="Отдать на учёбу в Synergy 199 Prior из {}🚘".format(count),
                callback_data='play_start_3_finish'
            )
        )

        await call.message.answer(
            "Выбери что сделать с этими Priorami 🚘",
            reply_markup=markup
        )

        await GameRPG.next()


@dp.callback_query_handler(state=GameRPG.game3)
async def callback_query(call, state: FSMContext):
    global count

    if call.data == 'play_start_3_finish':
        await state.finish()
        count -= 199

        await call.message.answer(
            "Вы теперь обучаетесь в Synergy! 💪\n"
            "У вас {} Priors 🚘 Катайтесь и учитесь отдуши, УДАЧИ!".format(count)
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
