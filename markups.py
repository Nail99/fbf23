from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_signup = KeyboardButton(text='Регистрация')
btn_help = KeyboardButton(text='Помощь')
btn_price = KeyboardButton(text='Цены на пассы')
btn_schedule = KeyboardButton(text='Расписание')
btn_address = KeyboardButton(text='Место проведения')
markup.add(btn_signup).add(btn_price, btn_address).add(btn_schedule, btn_help)

timetable = ReplyKeyboardMarkup(resize_keyboard=True)
friday = KeyboardButton(text='Пятница')
saturday = KeyboardButton(text='Суббота')
sunday = KeyboardButton(text='Воскресенье')
timetable.add(friday, saturday, sunday)

signed_up = ReplyKeyboardMarkup(resize_keyboard=True)
signed_up.add(btn_price, btn_address).add(btn_schedule, btn_help)

pass_type = ReplyKeyboardMarkup(resize_keyboard=True)
full_pass = KeyboardButton(text='Full Pass')
solo_pass = KeyboardButton(text='Solo Pass')
pass_type.add(full_pass, solo_pass)

yes_no_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yes = KeyboardButton(text='Да')
no = KeyboardButton(text='Нет')
yes_no_markup.add(yes, no)
