from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import os
from aiogram.fsm.context import FSMContext
from utils.utils import send_message_to_user
from FSM.fsm_user import FsmUser
from data.database import DataBase
import pandas as pd
from keyboards.reply import admin_keyboard
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

admins = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]
admin_router = Router()


@admin_router.message((F.text.endswith("root")) & (F.from_user.id.in_(admins)))
async def greet_admin(message: Message, state: FSMContext):
    await state.set_state(FsmUser.admin)
    await message.answer("Приветствую великий админ", reply_markup=admin_keyboard)


@admin_router.message((F.text == "Add student") & (F.from_user.id.in_(admins)))
async def admin_func1(message: Message, state: FSMContext):
    await state.set_state(FsmUser.admin_add)
    await message.delete()
    await message.answer("Отравь ФИО учеников разделенные переходом на новую строку. На первой строке введите номер")


@admin_router.message(FsmUser.admin_add)
async def add_new(message: Message, state: FSMContext):
    db = DataBase()

    data = message.text.lower().split('\n')
    number = int(data[0])
    names = data[1:]
    update_names = []


    if names:
        db.upload_students(names, number)
        stroka = "База данных обновлена: n add {0}".format('\n'.join(update_names))
        await send_message_to_user(message.bot, 504759266, stroka)
        await send_message_to_user(message.bot, 1141193948, stroka)
    await state.set_state(FsmUser.admin)
    # df.to_csv ("data/bd.csv", index = False)

# @admin_router.message ((F.text == "Delete student") & (F.from_user.id.in_(admins)))
