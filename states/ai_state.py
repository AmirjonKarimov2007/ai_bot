from aiogram.dispatcher.filters.state import State, StatesGroup


class ServicesStates(StatesGroup):
    Referat = State()
    Referat_AUTHOR_NAME = State()
    Referat_LANGUAGE = State()
    Referat_NUMBER_OF_PAGE = State()
    Referat_CHECK_RESOURCES = State()
    Mustaqil = State()
    Mustaqil_AUTHOR_NAME= State()
    SUCCESS_SERVICE = State()


    
    Slaydlar = State()
    Insho = State()
    Tabrik = State()
    Bayon = State()


class SERVICE_EDIT(StatesGroup):
    Referat_THEME = State()
    Referat_UNIVER = State()
    Referat_AUTHOR_NAME = State()
    Referat_LANGUAGE = State()
    Referat_PLAN = State()
    Referat_NUMBER_OF_PAGE = State()
    Referat_Plan_edit = State()
    



class PaymentState(StatesGroup):
    PAYMENT_CHECK = State()
    PAYMENT_SUM = State()
    


