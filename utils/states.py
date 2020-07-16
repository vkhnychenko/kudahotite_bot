from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    photo = State()
    quantity = State()


class Mailing(StatesGroup):
    text = State()
    confirm = State()