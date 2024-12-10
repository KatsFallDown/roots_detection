from aiogram.fsm.state import StatesGroup, State


class FsmUser(StatesGroup):
    reg = State()
    admin = State()
    admin_add = State()
    admin_remove = State()
    student = State()
    homework = State()
