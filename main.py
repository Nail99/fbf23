import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
import pandas as pd
from aiogram.utils import executor
import sqlite3

import text
from markups import markup, signed_up, pass_type, yes_no_markup, timetable
from database import Database
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database.db')

choose_city = []
choose_pass = []


class MemberRegistrationStates(StatesGroup):
    NAME = State()
    PHONE = State()
    CITY = State()
    PASS = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text=text.greeting, reply_markup=markup)


@dp.message_handler(commands=['magic'])
async def db_to_excel(message: types.Message):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM members", conn)
    df.to_excel('Участники FBF.xlsx', sheet_name='Sheet1', index=False)

    excel_file = pd.ExcelWriter('Участники FBF.xlsx', engine='xlsxwriter')
    df.to_excel(excel_file, sheet_name='Sheet1', index=False)
    excel_file.save()

    with open('Участники FBF.xlsx', 'rb') as file:
        await message.answer_document(file)


@dp.message_handler(Text(equals='Помощь'))
async def cmd_help(message: types.Message):
    await message.answer(text=text.help_command, parse_mode='HTML')


@dp.message_handler(Text(equals='Цены на пассы'))
async def cmd_price(message: types.Message):
    await message.answer(text=text.price, parse_mode='HTML')


@dp.message_handler(Text(equals='Место проведения'))
async def cmd_address(message: types.Message):
    await message.answer(text=text.address, parse_mode='HTML')


@dp.message_handler(Text(equals='Расписание'))
async def cmd_timetable(message: types.Message):
    await message.answer(text='Выберите день', reply_markup=timetable)


@dp.message_handler(Text(equals='Пятница'))
async def cmd_friday(message: types.Message):
    if db.member_exists(message.from_user.id):
        await message.answer(text=text.timetable_friday, parse_mode='HTML', reply_markup=signed_up)
    else:
        await message.answer(text=text.timetable_friday, parse_mode='HTML', reply_markup=markup)


@dp.message_handler(Text(equals='Суббота'))
async def cmd_saturday(message: types.Message):
    if db.member_exists(message.from_user.id):
        await message.answer(text=text.timetable_saturday, parse_mode='HTML', reply_markup=signed_up)
    else:
        await message.answer(text=text.timetable_saturday, parse_mode='HTML', reply_markup=markup)


@dp.message_handler(Text(equals='Воскресенье'))
async def cmd_saturday(message: types.Message):
    if db.member_exists(message.from_user.id):
        await message.answer(text=text.timetable_sunday, parse_mode='HTML', reply_markup=signed_up)
    else:
        await message.answer(text=text.timetable_sunday, parse_mode='HTML', reply_markup=markup)


@dp.message_handler(Text(equals='Регистрация'))
async def cmd_signup(message: types.Message, state: FSMContext):
    if not db.member_exists(message.from_user.id):
        db.add_member(message.from_user.id)
        db.member_telegram(message.from_user.id, message.from_user.username)

        await message.answer(text=text.signup_message, reply_markup=ReplyKeyboardRemove())
        await message.answer(text=text.name)
        await MemberRegistrationStates.NAME.set()
        await state.update_data(name='', phone='', city='')
    else:
        await message.answer('Вы уже зарегистрированы')


@dp.message_handler(state=MemberRegistrationStates.NAME)
async def member_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    db.set_name(message.from_user.id, name)
    await message.answer(text=text.phone)
    await MemberRegistrationStates.PHONE.set()


@dp.message_handler(state=MemberRegistrationStates.PHONE)
async def member_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone=phone_number)
    db.set_phone(message.from_user.id, phone_number)
    await message.answer(text=text.city)
    await MemberRegistrationStates.CITY.set()


@dp.message_handler(state=MemberRegistrationStates.CITY)
async def member_city(message: types.Message, state: FSMContext):
    city1 = message.text
    choose_city.append(city1)
    await state.update_data(city=city1)
    db.set_city(message.from_user.id, city1)
    await message.answer(text=text.choose_pass, reply_markup=pass_type)
    await MemberRegistrationStates.PASS.set()


@dp.message_handler(state=MemberRegistrationStates.PASS)
async def member_pass(message: types.Message, state: FSMContext):
    pass1 = message.text
    choose_pass.append(pass1)
    db.set_pass(message.from_user.id, pass1)
    await state.finish()
    await message.answer(text=text.resident, reply_markup=yes_no_markup)


@dp.message_handler(Text(equals='Да'))
async def price_yes(message: types.Message):
    await message.answer(text='Ваши данные сохранены 🙌', reply_markup=signed_up)
    await message.answer(text=text.final_price)
    await message.answer(text=text.final_price1)


@dp.message_handler(Text(equals='Нет'))
async def price_no(message: types.Message):
    await message.answer(text='Ваши данные сохранены 🙌', reply_markup=signed_up)
    await message.answer(text=text.final_price)
    await message.answer(text=text.final_price1)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
