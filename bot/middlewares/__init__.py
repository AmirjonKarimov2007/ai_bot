from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .majburiy_obuna import Asosiy,CheckPhoneNumber

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(Asosiy())
    dp.middleware.setup(CheckPhoneNumber())