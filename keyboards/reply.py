from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

admins = [int(admin_id) for admin_id in (os.getenv('ADMINS')).split(',')]


def gen_keyboard_menu(user_id: int):
    kb_list = [
        [
            KeyboardButton(text='Узнать имя'),
            KeyboardButton(text='Узнать что фамилию')], \
        {
            KeyboardButton(text='Узнать отчество'), \
            KeyboardButton(text='Узнать токен')
        }
    ]
    if user_id in admins:
        kb_list.append([KeyboardButton(text='Админ')])

    return ReplyKeyboardMarkup(keyboard=kb_list,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder="press something")


del_keyboard = ReplyKeyboardRemove()

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Add student'),
               KeyboardButton(text='Delete student')],
              {
                  KeyboardButton(text='Backup'),
                  KeyboardButton(text='Drop all'),
                  KeyboardButton(text='Вывести базу')
              }],
    resize_keyboard=True,
    one_time_keyboard=True
)

student_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отправить дз'),
               KeyboardButton(text='Методические пособия')
               ],
              {KeyboardButton(text='Связь с предователем')}],
    resize_keyboard=True,
    one_time_keyboard=True
)