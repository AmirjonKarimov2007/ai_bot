from aiogram.dispatcher.filters.state import State, StatesGroup


class ServicesStates(StatesGroup):
    Referat = State()
    Referat_AUTHOR_NAME = State()
    Referat_LANGUAGE = State()
    Referat_NUMBER_OF_PAGE = State()
    Referat_CHECK_RESOURCES = State()
    SUCCESS_SERVICE = State()


    Mustaqil = State()
    Slaydlar = State()
    Insho = State()
    Tabrik = State()
    Bayon = State()

