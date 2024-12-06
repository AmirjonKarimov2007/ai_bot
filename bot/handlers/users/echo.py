from loader import db,dp,bot
from aiogram import types
from keyboards.default.menu import *
from filters.users import IsUser
@dp.message_handler(IsUser())
async def echo(message: types.Message):
    await message.answer(f"<b>Menuni Tanlang:</b>",reply_markup=kb.main())