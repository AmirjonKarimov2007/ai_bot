from aiogram.dispatcher.filters.state import State, StatesGroup


class ServicesStates(StatesGroup):
    Referat = State()
    Mustaqil = State()
    Slaydlar = State()
    Insho = State()
    Tabrik = State()
    Bayon = State()