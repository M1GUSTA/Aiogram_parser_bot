from aiogram.dispatcher.filters.state import StatesGroup, State


class Parsing(StatesGroup):
    getting_source = State()