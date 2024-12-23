from aiogram import types
from loader import dp
from filters.users import IsUser,IsBlocked
from keyboards.default.menu import *
@dp.message_handler(IsUser())
async def echo(message: types.Message):
    await message.answer(f"<b>Menuni Tanlang:</b>",reply_markup=kb.main())

@dp.message_handler(IsBlocked())
async def echo(message: types.Message):
    await message.answer(f"<b>Siz botimizdan Blocklangansiz</b>")