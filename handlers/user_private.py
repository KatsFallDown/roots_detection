import os
import subprocess
from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ContentType
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from aiogram.fsm.context import FSMContext
from FSM.fsm_user import FsmUser
from utils.utils import send_message_to_user
from keyboards import reply
from data.database import DataBase
import pandas as pd
from aiogram import Bot
from dotenv import find_dotenv, load_dotenv
import re

load_dotenv(find_dotenv())

user_private_router = Router()


@user_private_router.message(Command('menu'))
async def Start(message: types.Message, state: FSMContext):
    db = DataBase()
    await state.clear()
    await message.answer(f"Привет!{message.chat.id}",
                         reply_markup=reply.gen_keyboard_menu(message.from_user.id))

    db.head()

    if db.is_token_exist(message.from_user.id):
        await message.answer("ty uzhe zdes", reply_markup=reply.student_keyboard)
        await state.set_state(FsmUser.student)
    else:
        await state.set_state(FsmUser.reg)
        await message.reply("Введите ваше ФИО")


@user_private_router.message(FsmUser.reg)
async def Reg(message: types.Message, state: FSMContext):
    db = DataBase()
    FIO = message.text
    if db.is_student_exists(FIO):
        db.update_student_token(FIO, message.chat.id)

        command = ['python3', 'scripts\makedir.py', str(message.text.lower().split()[0])]
        subprocess.run(command)

        await message.reply("Регистрация прошла успешно!", reply_markup=reply.student_keyboard)
        await state.set_state(FsmUser.student)
    else:
        await message.reply("Текущий пользователь не найден обратитесь к преподователю")
        # await send_message_to_user(message.bot, 504759266, f"Неопознанный пидорас @{message.chat.username}")
        await send_message_to_user(message.bot, 1141193948, f"Неопознанный пидорас @{message.chat.username}")
        await state.clear()


@user_private_router.message((F.text == "Отправить дз"), FsmUser.student)
async def Homework(message: Message, state: FSMContext):
    await message.answer("Отправь мне дз!")
    await state.set_state(FsmUser.homework)


class PythonFileFilter:
    @staticmethod
    async def __call__(message: types.Message):
        # Проверяем, что сообщение содержит документ
        if message.document and message.document.file_name.endswith('.py'):
            return True
        return False


@user_private_router.message(FsmUser.homework, PythonFileFilter())
async def handle_homework(message: types.Message, bot: Bot, state: FSMContext):
    try:
        if message.document.file_name.endswith('.py'):
            file_info = await bot.get_file(file_id=message.document.file_id)
            file_path = file_info.file_path

            db = DataBase()
            path = os.getcwd()

            file_url = f'https://api.telegram.org/file/bot{0}/{1}'.format(str(os.getenv('TOKEN')), file_path)

            pizduk_name = db.get_name_by_token(int(message.chat.id)).split(' ')[0]
            pattern = r'\b\d{1,2}\b|\d{1,2}(?=\D|$)'
            task_number = re.findall(pattern, message.document.file_name)

            file_name = path + '\homework\{0}\\task_{1}'.format(pizduk_name, task_number[0])
            os.makedirs(file_name, exist_ok=True)
            file_name = os.path.join(file_name, message.document.file_name)
            try:
                await bot.download_file(file_path, file_name)
                await message.reply(f"OK {task_number}")
                db.accept_hw(message.chat.id, int(task_number[0]))
                db.head()
                await state.set_state(FsmUser.student)
            except Exception as e:
                await message.reply(f"File not saved cause {e}")

        else:
            await message.reply("Отправь мне файл с расширением .py")
    except:
        await message.reply("Отправь файл а не текстовое сообщение!")

