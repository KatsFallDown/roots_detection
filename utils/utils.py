from aiogram import Bot


async def send_message_to_user(bot: Bot, user_id: int, message: str):
    try:
        # Отправка сообщения
        await bot.send_message(user_id, message)

        print(f"Сообщение отправлено пользователю с ID {user_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")