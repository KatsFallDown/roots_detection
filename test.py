import asyncio
from dotenv import find_dotenv, load_dotenv
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram import types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from common.bot_menu import private
from handlers.user_private import user_private_router
from handlers.admin import admin_router

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(admin_router)

ALLOWED_UPDATES = ['message', 'edited_message']


async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # не отвечать на все запросы отправленные вне работы бота
    # await bot.delete_my_commands (scope=types.BotCommandScopeAllPrivateChats()) #удалить все команды, так как через BotFather не удалишь то что написал сам
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
